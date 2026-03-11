from fastapi import FastAPI
from app.routers import accounts, transactions
from app.database import Base, engine
from app import models


app = FastAPI()


Base.metadata.create_all(engine)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}