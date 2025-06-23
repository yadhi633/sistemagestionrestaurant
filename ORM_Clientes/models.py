# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    pedidos = relationship("Pedido", back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, default=0)
    unidad_medida = Column(String, nullable=False)

    menus = relationship("MenuIngrediente", back_populates="ingrediente")

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False, default=2500)

    ingredientes = relationship("MenuIngrediente", back_populates="menu")
    pedidos = relationship("PedidoDetalle", back_populates="menu")

class MenuIngrediente(Base):
    __tablename__ = 'menu_ingredientes'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id'))
    cantidad = Column(Float, nullable=False)

    menu = relationship("Menu", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="menus", lazy='joined')


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float, default=0)

    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship("PedidoDetalle", back_populates="pedido")

class PedidoDetalle(Base):
    __tablename__ = 'pedido_detalles'

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    cantidad = Column(Integer, default=1)

    pedido = relationship("Pedido", back_populates="detalles")
    menu = relationship("Menu", back_populates="pedidos")
