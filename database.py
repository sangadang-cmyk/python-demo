from datetime import datetime
import os
import struct
import pyodbc
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
credential = DefaultAzureCredential()

def get_connection():
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("utf-16-le")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={os.getenv('DB_HOST')},1433;"
        f"Database={os.getenv('DB_NAME')};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, attrs_before={1256: token_struct})

engine = create_engine("mssql+pyodbc://", creator=get_connection, echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, onupdate=datetime.now)