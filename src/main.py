
from agent.pdf_parser_agent import parser_pdf
import json

pdf_file = "~/Documents/testCodes/lumen/pdf-extract/src/example_data/invoice-1.pdf"
invoice = parser_pdf(pdf_file)
print(json.dumps(invoice, indent=2))
