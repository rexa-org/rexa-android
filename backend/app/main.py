from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from .config import settings
from .routes import auth, users, rewards, marketplace, wallet, payments, admin

app = FastAPI(title="reX API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
# Uncomment for production
# app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
app.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Welcome to reX API"}
