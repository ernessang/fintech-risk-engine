from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float
    country: str
    merchant: str
    tokenized: bool
