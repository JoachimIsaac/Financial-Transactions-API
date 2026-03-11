from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import Numeric, select, or_
from typing import List

from .. import models
from ..database import get_db
from ..schemas import TransactionResponse, TransactionCreate
from ..models import TransactionStatus




router = APIRouter()






@router.get("/transactions/{transaction_id}",response_model=TransactionResponse,status_code=200)
def get_transaction(transaction_id: UUID, db: Session = Depends(get_db)):

    current_transaction = db.get(models.Transaction, transaction_id)
    
    if current_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return current_transaction




@router.get("/accounts/{account_id}/transactions",response_model=List[TransactionResponse],status_code=200)
def get_account_transactions(account_id: UUID, db: Session = Depends(get_db)):

    account = db.get(models.Account, account_id)

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")


    stmt = select(models.Transaction).where(
        or_(
            models.Transaction.from_account_id == account_id,
            models.Transaction.to_account_id == account_id,
        )
    )

    current_transactions = db.execute(stmt).scalars().all()

    return current_transactions


@router.post("/transactions/",response_model=TransactionResponse,status_code=201) 
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):

    from_account = db.get(models.Account, transaction.from_account_id)
    to_account = db.get(models.Account, transaction.to_account_id)

    if from_account is None:
        raise HTTPException(status_code=404, detail="From Account not found")
    
    if to_account is None:
        raise HTTPException(status_code=404, detail="To Account not found")

    if from_account.balance - transaction.amount < 0:
         raise HTTPException(status_code=400, detail="Insufficient funds")
    else:
        try:
            from_account.balance -= transaction.amount
            to_account.balance += transaction.amount
            new_transaction = models.Transaction(**transaction.model_dump(),status=TransactionStatus.COMPLETED)

            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)

            return new_transaction
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Transaction failed")


