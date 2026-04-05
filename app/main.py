from fastapi import FastAPI
from app.db.session import engine, Base
# Import ALL your routers here
from app.api.v1.endpoints import transactions, analytics, auth 

# This creates the tables in MySQL based on your models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance System Backend")

# Register each router ONCE with the correct prefix
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Finance System API is running"}