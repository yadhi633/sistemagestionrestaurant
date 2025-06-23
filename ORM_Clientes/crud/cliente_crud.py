# crud/cliente_crud.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import Cliente

def crear_cliente(session: Session, nombre: str, email: str):
    try:
        cliente = Cliente(nombre=nombre, email=email)
        session.add(cliente)
        session.commit()
        print("✅ Cliente creado correctamente.")
    except IntegrityError:
        session.rollback()
        print("❌ Error: el email ya existe.")

def listar_clientes(session: Session):
    clientes = session.query(Cliente).all()
    if not clientes:
        print("⚠️ No hay clientes registrados.")
    else:
        print("📋 Lista de clientes:")
        for c in clientes:
            print(f"{c.id} | {c.nombre} | {c.email}")
    return clientes 

def actualizar_cliente(session: Session, cliente_id: int, nuevo_nombre: str, nuevo_email: str):
    cliente = session.query(Cliente).get(cliente_id)
    if cliente:
        cliente.nombre = nuevo_nombre
        cliente.email = nuevo_email
        try:
            session.commit()
            print("✅ Cliente actualizado.")
        except IntegrityError:
            session.rollback()
            print("❌ Error: el nuevo email ya existe.")
    else:
        print("❌ Cliente no encontrado.")

def eliminar_cliente(session: Session, cliente_id: int):
    cliente = session.query(Cliente).get(cliente_id)
    if cliente:
        session.delete(cliente)
        session.commit()
        print("🗑️ Cliente eliminado.")
    else:
        print("❌ Cliente no encontrado.")
