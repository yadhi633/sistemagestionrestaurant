# crud/menu_crud.py
from sqlalchemy.orm import Session
from models import Menu, Ingrediente, MenuIngrediente
from sqlalchemy.exc import IntegrityError

def crear_menu(session: Session, nombre: str, descripcion: str, ingredientes_cantidad: list, precio: float):
    """
    ingredientes_cantidad: lista de tuplas (ingrediente_id, cantidad)
    """
    # Verificar si ya existe un menú con ese nombre
    existente = session.query(Menu).filter_by(nombre=nombre).first()
    if existente:
        print("❌ Ya existe un menú con ese nombre.")
        return False

    try:
        menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)
        session.add(menu)
        session.commit()

        for ingrediente_id, cantidad in ingredientes_cantidad:
            ingrediente = session.query(Ingrediente).get(ingrediente_id)
            if not ingrediente:
                print(f"⚠️ Ingrediente ID {ingrediente_id} no existe. Saltando.")
                continue

            relacion = MenuIngrediente(menu_id=menu.id, ingrediente_id=ingrediente_id, cantidad=cantidad)
            session.add(relacion)

        session.commit()
        print("✅ Menú creado con éxito.")
        return True
    except IntegrityError:
        session.rollback()
        print("❌ Error al crear el menú.")
        return False



def listar_menus(session: Session):
    return session.query(Menu).all()

def obtener_ingredientes_de_menu(session: Session, menu_id: int):
    return (
        session.query(MenuIngrediente)
        .filter(MenuIngrediente.menu_id == menu_id)
        .all()
    )

def actualizar_menu(session: Session, menu_id: int, nuevo_nombre: str, nueva_descripcion: str, nuevos_ingredientes: list):
    """
    nuevos_ingredientes: lista de tuplas (ingrediente_id, cantidad)
    """
    menu = session.query(Menu).get(menu_id)
    if not menu:
        print("❌ Menú no encontrado.")
        return

    menu.nombre = nuevo_nombre
    menu.descripcion = nueva_descripcion

    # Eliminar relaciones anteriores
    session.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()

    # Crear nuevas relaciones
    for ingrediente_id, cantidad in nuevos_ingredientes:
        nueva_relacion = MenuIngrediente(menu_id=menu_id, ingrediente_id=ingrediente_id, cantidad=cantidad)
        session.add(nueva_relacion)

    try:
        session.commit()
        print("✅ Menú actualizado.")
    except Exception as e:
        session.rollback()
        print("❌ Error al actualizar menú:", str(e))

def eliminar_menu(session: Session, menu_id: int):
    menu = session.query(Menu).get(menu_id)
    if not menu:
        print("❌ Menú no encontrado.")
        return

    # Primero borrar las relaciones
    session.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
    session.delete(menu)
    session.commit()
    print("🗑️ Menú eliminado.")

def editar_menu(session, menu_id, nombre, descripcion, ingredientes_cantidad, precio):
    menu = session.query(Menu).get(menu_id)
    if not menu:
        print("❌ Menú no encontrado.")
        return False

    try:
        menu.nombre = nombre
        menu.descripcion = descripcion
        menu.precio = precio

        # Eliminar ingredientes actuales
        session.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()

        # Agregar ingredientes nuevos
        for ingrediente_id, cantidad in ingredientes_cantidad:
            nueva_relacion = MenuIngrediente(menu_id=menu_id, ingrediente_id=ingrediente_id, cantidad=cantidad)
            session.add(nueva_relacion)

        session.commit()
        print("✅ Menú editado con éxito.")
        return True
    except Exception as e:
        session.rollback()
        print("❌ Error al editar menú:", e)
        return False
