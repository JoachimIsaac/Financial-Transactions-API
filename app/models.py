
import enum
import uuid
from sqlalchemy import  Column, String, Enum, Numeric, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from database import Base



class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED= "completed"
    FAILED = "failed"

class TransactionType(enum.Enum):
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_name = Column(String(50))
    balance = Column(Numeric(precision=12, scale=2),default=0)
    currency = Column(String(3),nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Account(id='{self.id}',owner_name='{self.owner_name}', balance='{self.balance}',currency='{self.currency}',created_at='{self.created_at}')>"



class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_account_id = Column(PG_UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    to_account_id = Column(PG_UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    amount = Column(Numeric(precision=12, scale=2))
    status = Column(Enum(TransactionStatus), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return (
            f"<Transaction(id='{self.id}', amount='{self.amount}', "
            f"status='{self.status.value}', type='{self.transaction_type.value}', "
            f"created_at='{self.created_at}')>"
        )