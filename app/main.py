from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import auth, register, users, organisations
from . import models


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(register.router)
app.include_router(organisations.router)


@app.get("/")
async def hello():
    return {"message": "HNG internship Stage-2"}
