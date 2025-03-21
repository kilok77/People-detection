from fastapi import Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db

def get_database_session() -> Session:
    db = get_db()
    try:
        yield db
    finally:
        db.close()