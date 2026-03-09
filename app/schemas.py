from decimal import Decimal
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from models import TransactionType,TransactionStatus



class AccountBase(BaseModel):
    # Use Field to add validation like max length
    owner_name: str = Field(..., min_length=2, max_length=100, examples=["Alice Smith"])
    currency: str = Field(..., min_length=3, max_length=3, pattern="^[A-Z]{3}$")


class AccountCreate(AccountBase):
    pass


class AccountResponse(AccountBase):
    id: UUID
    balance: Decimal
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TransactionBase(BaseModel):
    amount: Decimal = Field(...,max_digits=12,decimal_places=2,gt=0,examples=["100.50"])
    transaction_type: TransactionType = Field(...,description="Must be deposit, withdrawal, or transfer")
    from_account_id: UUID 
    to_account_id: UUID 

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id:UUID
    status:TransactionStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)