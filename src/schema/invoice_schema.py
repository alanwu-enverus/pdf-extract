from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import date

class Address(BaseModel):
    streetName: Optional[str] = Field(None, description="Street name")
    additionalStreetName: Optional[str] = Field(None, description="Additional street name")
    cityName: Optional[str] = Field(None, description="City name")
    postalZone: Optional[str] = Field(None, description="Postal code")
    countrySubentity: Optional[str] = Field(None, description="State/province")
    country: Optional[str] = Field(None, description="Country code (e.g., US, CA)")

class PartyLegalEntity(BaseModel):
    registrationName: Optional[str] = Field(None, description="Legal registration name")
    companyID: Optional[str] = Field(None, description="Company registration ID")

class PartyTaxScheme(BaseModel):
    taxSchemeID: Optional[str] = Field(None, description="Tax scheme ID (e.g., VAT)")
    companyID: Optional[str] = Field(None, description="Tax registration ID")

class Party(BaseModel):
    partyLegalEntity: Optional[PartyLegalEntity] = None
    postalAddress: Optional[Address] = None
    partyTaxScheme: Optional[List[PartyTaxScheme]] = None

class SupplierParty(BaseModel):
    party: Optional[Party] = None

class CustomerParty(BaseModel):
    party: Optional[Party] = None

class TaxSubtotal(BaseModel):
    taxableAmount: Optional[float] = Field(None, description="Amount subject to tax")
    taxAmount: Optional[float] = Field(None, description="Tax amount")
    percent: Optional[float] = Field(None, description="Tax percentage")

class TaxCategory(BaseModel):
    id: Optional[str] = Field(None, description="Tax category ID")
    percent: Optional[float] = Field(None, description="Tax percentage")
    taxScheme: Optional[str] = Field(None, description="Tax scheme ID")
    taxSubtotal: Optional[List[TaxSubtotal]] = None

class TaxTotal(BaseModel):
    taxAmount: Optional[float] = Field(None, description="Total tax amount")
    taxSubtotal: Optional[List[TaxSubtotal]] = None

class Price(BaseModel):
    priceAmount: Optional[float] = Field(None, description="Unit price amount")
    baseQuantity: Optional[float] = Field(None, description="Base quantity for the price")

class Item(BaseModel):
    name: Optional[str] = Field(None, description="Item name")
    description: Optional[str] = Field(None, description="Item description")

class LineItem(BaseModel):
    id: Optional[int] = Field(None, description="Line item ID")
    quantity: Optional[float] = Field(None, description="Quantity of items")
    lineExtensionAmount: Optional[float] = Field(None, description="Total amount for the line")
    item: Optional[Item] = None
    price: Optional[Price] = None
    taxCategory: Optional[List[TaxCategory]] = None

class PaymentMeans(BaseModel):
    id: Optional[str] = Field(None, description="Payment means ID (e.g., Credit transfer)")
    paymentDueDate: Optional[date] = Field(None, description="Payment due date")

class Invoice(BaseModel):
    """Call to convert to invoice"""
    id: Optional[str] = Field(None, description="Invoice ID")
    issueDate: Optional[date] = Field(None, description="Invoice issue date")
    dueDate: Optional[date] = Field(None, description="Invoice due date")
    invoiceTypeCode: Optional[str] = Field(None, description="Invoice type code (e.g., 380 for commercial invoice)")
    documentCurrencyCode: Optional[str] = Field(None, description="Currency code (e.g., USD, EUR)")
    accountingSupplierParty: Optional[SupplierParty] = None
    accountingCustomerParty: Optional[CustomerParty] = None
    taxTotal: Optional[TaxTotal] = None
    legalMonetaryTotal: Optional[float] = Field(None, description="Total amount of the invoice")
    invoiceLine: Optional[List[LineItem]] = None
    paymentMeans: Optional[List[PaymentMeans]] = None