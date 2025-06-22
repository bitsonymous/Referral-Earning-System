from fastapi import FastAPI
from routers import auth, users, transactions, earnings, websocket

app = FastAPI(title="Referral & Earning System")

# Register route modules
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(earnings.router, prefix="/earnings", tags=["Earnings"])
app.include_router(websocket.router, tags=["WebSocket"])
