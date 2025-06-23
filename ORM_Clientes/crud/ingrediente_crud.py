# crud/ingrediente_crud.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import Ingrediente

def crear_ingrediente(session: Session, nombre: str, tipo: str, cantidad: float, unidad: str):
    try:
        ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad_medida=unidad)
        session.add(ingrediente)
        session.commit()
        print("✅ Ingrediente creado.")
    except IntegrityError:
        session.rollback()
        print("❌ Ya existe un ingrediente con ese nombre.")

def listar_ingredientes(session: Session):
    return session.query(Ingrediente).all()

def actualizar_ingrediente(session: Session, ingrediente_id: int, nombre: str, tipo: str, cantidad: float, unidad: str):
    ingrediente = session.query(Ingrediente).get(ingrediente_id)
    if ingrediente:
        ingrediente.nombre = nombre
        ingrediente.tipo = tipo
        ingrediente.cantidad = cantidad
        ingrediente.unidad_medida = unidad
        try:
            session.commit()
            print("✅ Ingrediente actualizado.")
        except IntegrityError:
            session.rollback()
            print("❌ Ya existe otro ingrediente con ese nombre.")
    else:
        print("❌ Ingrediente no encontrado.")

def eliminar_ingrediente(session: Session, ingrediente_id: int):
    ingrediente = session.query(Ingrediente).get(ingrediente_id)
    if ingrediente:
        session.delete(ingrediente)
        session.commit()
        print("🗑️ Ingrediente eliminado.")
    else:
        print("❌ Ingrediente no encontrado.")
