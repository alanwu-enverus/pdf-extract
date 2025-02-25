
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm_model.bedrock import get_bedrock_embeddings, get_chat_bedrock_llm
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import PydanticToolsParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage

from schema.invoice_schema import *

def parser_pdf(file_path: str):
    loader = PyPDFLoader(
        file_path=file_path,
    )
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=get_bedrock_embeddings())

    retriever = vectorstore.as_retriever()

    parser_pydnatic = PydanticToolsParser(tools=[Invoice])
    
    llm = get_chat_bedrock_llm()
    llm.bind_tools(tools=[Invoice], tool_choice="Invoice") 
    
    system_prompt = (  
        "You are an assistant for extract data"
        "Use the following pieces of context to convert the provided format"
        "only return the extracted data in the format"
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "convert to {doctype}")
        ],
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    parser = rag_chain 
    
    # human_message = HumanMessage( content="convert to invoice")
    results = parser.invoke({"input": {"doctype":"convert to invoice"}}) | parser_pydnatic
    # results = parser.invoke({"doctype":"convert to invoice"})
    invoice = results["answer"]
    return invoice
