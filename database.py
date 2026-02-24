from datetime import datetime
import os
from dotenv import load_dotenv

from sqlalchemy import URL, Column, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

connection_url = URL.create(
    "mssql+pyodbc",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=1433,
    database=os.getenv("DB_NAME"),
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(connection_url, echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, onupdate=datetime.now)
    pass
