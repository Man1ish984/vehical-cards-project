from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cards_db_ka8q_user:oJ8c77zdqnrsrgAPT7TlQSoqTAvXLiBt@localhost/cards_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
