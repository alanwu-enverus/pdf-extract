import os
import boto3
from botocore.config import Config
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


aws_region = os.getenv("AWS_REGION", "us-east-1")
bedrock_config = Config(
    connect_timeout=120, read_timeout=120, retries={"max_attempts": 0}
)
session = boto3.Session(profile_name="ba-dev")
bedrock_rt = session.client(
    "bedrock-runtime", region_name=aws_region, config=bedrock_config
)
model_kwargs = {
    "max_tokens": 512,
    "temperature": 0.0,
}
llm = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    config=bedrock_config,
    region_name=aws_region,
    verbose=True,
    credentials_profile_name="ba-dev",
    client=bedrock_rt,
    model_kwargs=model_kwargs,
)

bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0", client=bedrock_rt
)

loader = PyPDFLoader(
    file_path="~/Documents/testCodes/lumen/pdf-extract/src/example_data/invoice-3.pdf"
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=bedrock_embeddings)

retriever = vectorstore.as_retriever()

 
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

questions = [
    "What is the invoice number?",
    "What is the total amount?",
    "What is the due date?",
    "What is the billing address?",
    "What is the shipping address?",
    "What is the invoice date?",
    "how many items are in the invoice?",
]


for question in questions:
    
    print(f"\033[95m Question: {question}")
    results = rag_chain.invoke({"input": question})
    print('\033[92m' + results['answer'])

