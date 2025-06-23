# main.py
from database import Base, engine
import models

# Crear todas las tablas
Base.metadata.create_all(bind=engine)
print("Base de datos inicializada.")
