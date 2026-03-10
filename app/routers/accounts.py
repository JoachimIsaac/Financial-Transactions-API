from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from .. import models
from ..database import get_db
from ..schemas import AccountCreate, AccountResponse


router = APIRouter()



@router.post("/accounts",response_model=AccountResponse,status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    

    new_account = models.Account(**account.model_dump())

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


@router.get("/accounts/{account_id}",response_model=AccountResponse,status_code=200)
def get_account(account_id: UUID, db: Session = Depends(get_db)):

    current_account = db.get(models.Account, account_id)
    
    if current_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return current_account
