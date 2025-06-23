from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Menu, PedidoDetalle, Pedido, Cliente

def obtener_top_menus(session: Session, limite=5):
    """
    Retorna los menús más pedidos junto con su cantidad total.
    """
    resultados = (
        session.query(Menu.nombre, func.sum(PedidoDetalle.cantidad).label("total"))
        .join(PedidoDetalle.menu)
        .group_by(Menu.id)
        .order_by(func.sum(PedidoDetalle.cantidad).desc())
        .limit(limite)
        .all()
    )
    return resultados


def obtener_pedidos_por_cliente(session: Session):
    """
    Retorna el número de pedidos realizados por cada cliente.
    """
    resultados = (
        session.query(Cliente.nombre, func.count(Pedido.id))
        .join(Pedido.cliente)
        .group_by(Cliente.id)
        .order_by(func.count(Pedido.id).desc())
        .all()
    )
    return resultados


def obtener_gasto_total_por_cliente(session: Session):
    """
    Retorna el gasto total acumulado por cliente.
    """
    resultados = (
        session.query(Cliente.nombre, func.sum(Pedido.total))
        .join(Pedido.cliente)
        .group_by(Cliente.id)
        .order_by(func.sum(Pedido.total).desc())
        .all()
    )
    return resultados
