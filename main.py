import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from src.db import create_db_and_tables
from src.models.users import fastapi_users, auth_backend
from src.routers import api_unauthorized_endpoints, api_authorized_endpoints
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import UserRead, UserCreate, UserUpdate

from src.services.log import CustomizeLogger

logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("log_config.json")
app = FastAPI(logger=CustomizeLogger.make_logger(config_path=config_path))

# Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Including routers
app.include_router(api_unauthorized_endpoints.router, tags=["api"])
app.include_router(api_authorized_endpoints.router, tags=["api"])
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# App healthcheck
@app.get("/")
def fallthrough():
    return {
        "status": "All systems operational",
        "code": 200,
        "timestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }


@app.on_event("startup")
async def on_startup():
    # TO DO : Change to Alembic
    await create_db_and_tables()
