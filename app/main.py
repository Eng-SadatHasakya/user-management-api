import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .database import engine, Base
from .routers import user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="User Management API",
    description="""
## A production-grade REST API

### Features:
- ✅ JWT Authentication
- ✅ Role-Based Access Control (Admin / User)
- ✅ Refresh Tokens
- ✅ Rate Limiting
- ✅ Audit Logging
    """,
    version="1.0.0",
    contact={
        "name": "Eng. Sadat Hasakya",
        "email": "hersacemusasadat@gmail.com",
        "url": "https://github.com/hersacemusasadat"
    },
    license_info={
        "name": "MIT"
    }
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(user.router)

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def landing():
    with open("app/landing.html", "r", encoding="utf-8") as f:
        return f.read()