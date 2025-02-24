
from agent.pdf_parser import parser_pdf

pdf_file = "~/Documents/testCodes/lumen/pdf-extract/src/example_data/invoice-1.pdf"
invocie = parser_pdf(pdf_file)
print(invocie)
