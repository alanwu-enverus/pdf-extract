from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class BaseInvoice(BaseModel):
    """Call to extract base invoice information"""
    invoiceNumber: Optional[str] = Field(None, description="Invoice ID")
    invoiceDate: Optional[date] = Field(None, description="Invoice issue date")
    customerName: Optional[str] = Field(None, description="Buyer name")
    totalAmount: Optional[float] = Field(None, description="Total amount of the invoice")
