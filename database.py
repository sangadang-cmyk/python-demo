from datetime import datetime
import os
import struct
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from sqlalchemy import URL, Column, DateTime, create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

credential = DefaultAzureCredential()

connection_url = URL.create(
    "mssql+pyodbc",
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

@event.listens_for(engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("utf-16-le")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
    cparams["attrs_before"] = {1256: token_struct}

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, onupdate=datetime.now)
    pass
