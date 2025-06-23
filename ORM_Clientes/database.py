# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usaremos SQLite (archivo local llamado restaurante.db)
DATABASE_URL = "sqlite:///restaurante.db"

# Crear motor y sesión
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Base para todos los modelos ORM
Base = declarative_base()
