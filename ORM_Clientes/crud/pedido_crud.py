# crud/pedido_crud.py
from sqlalchemy.orm import Session
from models import Pedido, PedidoDetalle, Menu, Ingrediente, MenuIngrediente
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def crear_pedido(session: Session, cliente_id: int, items: list) -> int:
    """
    Crea un pedido nuevo para un cliente.

    :param session: Sesión activa de SQLAlchemy
    :param cliente_id: ID del cliente que realiza el pedido
    :param items: Lista de tuplas (menu_id, cantidad)
    :return: ID del pedido creado
    """
    try:
        total = 0
        pedido = Pedido(cliente_id=cliente_id)
        session.add(pedido)
        session.flush()  # Para obtener el ID del pedido sin hacer commit aún

        for menu_id, cantidad in items:
            menu = session.query(Menu).get(menu_id)
            if not menu:
                continue

            # Agregar detalle
            detalle = PedidoDetalle(pedido_id=pedido.id, menu_id=menu_id, cantidad=cantidad)
            session.add(detalle)

            # Calcular total
            total += menu.precio * cantidad

            # Descontar ingredientes
            for rel in menu.ingredientes:
                cantidad_usada = rel.cantidad * cantidad
                rel.ingrediente.cantidad -= cantidad_usada
                print(f"🧾 Restando {cantidad_usada} de {rel.ingrediente.nombre}")

        pedido.total = total
        session.commit()
        print(f"✅ Pedido creado con ID {pedido.id} y total ${total:.0f}")
        return pedido.id

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error al crear el pedido: {e}")
        return -1

def listar_pedidos(session: Session):
    return session.query(Pedido).order_by(Pedido.fecha.desc()).all()

def obtener_pedidos_por_cliente(session: Session, cliente_id: int):
    return session.query(Pedido).filter_by(cliente_id=cliente_id).order_by(Pedido.fecha.desc()).all()

def obtener_detalle_pedido(session: Session, pedido_id: int):
    return session.query(PedidoDetalle).filter_by(pedido_id=pedido_id).all()

def verificar_stock_suficiente(session, items):
    """
    Verifica si hay stock suficiente para los ingredientes necesarios en los menús pedidos.
    :param session: sesión activa de SQLAlchemy
    :param items: lista de tuplas (menu_id, cantidad)
    :return: (bool, mensaje) -> True si hay stock, False si falta algo
    """
    from models import MenuIngrediente, Ingrediente

    faltantes = []

    for menu_id, cantidad_menu in items:
        ingredientes_menu = session.query(MenuIngrediente).filter_by(menu_id=menu_id).all()
        for mi in ingredientes_menu:
            total_requerido = mi.cantidad * cantidad_menu
            stock_actual = session.query(Ingrediente).get(mi.ingrediente_id).cantidad

            if stock_actual < total_requerido:
                faltantes.append(
                    f"- {mi.ingrediente.nombre} (necesario: {total_requerido}, disponible: {stock_actual})"
                )

    if faltantes:
        mensaje = "❌ Stock insuficiente para los siguientes ingredientes:\n" + "\n".join(faltantes)
        return False, mensaje

    return True, ""