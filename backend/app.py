import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db

app = FastAPI()

db.bind(
    provider='postgres', 
    user=os.environ['POSTGRES_USER'], 
    password=os.environ['POSTGRES_PASSWORD'], 
    host='db',
    database='cashflow'
)
db.generate_mapping(create_tables=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def healthcheck():
    return "I am alive!"