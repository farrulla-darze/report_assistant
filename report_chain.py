from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatOpenAI
from langchain import hub
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
import getpass
import os
load_dotenv()


openai_key = "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"
embeddings = OpenAIEmbeddings(openai_api_key=openai_key)

loader = TextLoader("./pages_content.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

#embeddings = OpenAIEmbeddings(openai_key=openai_key)
sen_trans_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Vector Database
qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    #path="/tmp/local_qdrant",
    location=":memory:",
    collection_name="report_collection",
)


# Vector Database as a retriever
retriever = qdrant.as_retriever()
#print(retriever)

# Generation
llm = ChatOpenAI(openai_api_key=openai_key ,model_name="gpt-3.5-turbo", temperature=0)

prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

query = "What is the impact of climate change on the economy?"
print(f"Question: {query}")
print("\n Answer:")
for chunk in rag_chain.stream(query):
    print(chunk, end="", flush=True)
