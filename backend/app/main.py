from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from .config import settings
from .routes import auth, users, rewards, marketplace, wallet, payments, admin

app = FastAPI(
    title="reX API", 
    version="0.1.0",
    description="Reward Exchange API - Consolidate, exchange, and monetize digital rewards"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
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
    return {"message": "Welcome to reX API", "version": "0.1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "reX API"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
