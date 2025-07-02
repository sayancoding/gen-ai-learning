import bs4
import os

from dotenv import load_dotenv
load_dotenv()

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain_core.runnables import RunnableMap,RunnablePassthrough
from langchain_core.output_parsers.string import StrOutputParser

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature = 0.7)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

pdf_loader = PyPDFLoader("./data/resume.pdf")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=500)
splits = text_splitter.split_documents(pdf_loader.load())
# print(f"Chunking documents => {splits}")

vs = FAISS.from_documents(splits,embeddings)
vs.save_local('faiss_index')
retriever = vs.as_retriever()

prompt = hub.pull('rlm/rag-prompt')

def format_docs(docs):
  return "\n".join(doc.page_content for doc in docs)

rag_chain = (
  RunnableMap({"context": retriever , "question": RunnablePassthrough()})
    # | format_docs
    | prompt
    | llm
    | StrOutputParser())


while True:
  ques = input("\nAsk something ? \n")
  if(ques == 'exit'): 
    break
  ans = rag_chain.invoke(ques)
  print(f"\nBot => {ans}\n")


