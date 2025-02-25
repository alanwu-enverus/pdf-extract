from llm_model.bedrock import get_chat_bedrock_llm
from schema.oi_invoice_schema import Invoice
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader

def parser_pdf(file_path: str):
    parser = JsonOutputParser()
    
    prompt = PromptTemplate(
        template="Extract the information as specified.\n{format_instructions}\n{context}\n",
        input_variables=["context"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    loader = PyPDFLoader(file_path=file_path)
    pages = loader.load()
    
    llm = get_chat_bedrock_llm()

    chain = prompt | llm | parser

    response = chain.invoke({
        "context": pages
    })
    
    return response
