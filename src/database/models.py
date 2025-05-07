from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, func, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone


Base = declarative_base() # Asocia la metadata de toda la BD


class TipoCafe(Base):
    __tablename__ = 'tipos_cafe'
    # Atributos
    cafe_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True, nullable=False)
    min_agua = Column(Integer, nullable=False)
    max_agua = Column(Integer, nullable=False)
    descripcion = Column(String(50), nullable=False)
    ## Relaciones bidireccionales (consultas)
    recetas = relationship("Receta", back_populates="tipo_cafe") # Uno a muchos
    pedidos = relationship("Pedido", back_populates="tipo_cafe") # Uno a muchos


class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    # Atributos
    ingrediente_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_ingrediente = Column(String(20), nullable=False)
    unidad_medida = Column(String(10), nullable=False)
    ## Relaciones bidireccionales (consultas)
    recetas = relationship("Receta", back_populates="ingrediente") # uno a muchos
    inventario = relationship("Inventario", back_populates="ingrediente", uselist=False) # Uno a uno


class Pedido(Base):
    __tablename__ = 'pedidos'
    # Atributos
    pedido_id = Column(Integer, primary_key=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey('tipos_cafe.cafe_id'), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.now(timezone.utc))
    cantidad_azucar = Column(Integer, nullable=True, default=0)
    cantidad_agua = Column(Integer, nullable=False)
    ## Relaciones bidireccionales (consultas)
    tipo_cafe = relationship("TipoCafe", back_populates="pedidos") # Muchos a uno


class Receta(Base):
    __tablename__ = 'recetas'
    # Atributos
    receta_id = Column(Integer, primary_key=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey('tipos_cafe.cafe_id'), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.ingrediente_id'), nullable=False)
    cantidad = Column(Integer, nullable=True)
    es_agua = Column(Boolean, nullable=False)
    ## Relaciones bidireccionales (consultas)
    ingrediente = relationship("Ingrediente", back_populates="recetas") # Muchos a uno
    tipo_cafe = relationship("TipoCafe", back_populates="recetas") # Muchos a uno
    # Constraint -> Una receta no puede tener dos ingredientes iguales
    __table_args__ = (UniqueConstraint('cafe_id', 'ingrediente_id', name="unique_receta_ingrediente"),)


class Inventario(Base):
    __tablename__ = 'inventario'
    # Atributos
    inventario_id = Column(Integer, primary_key=True, autoincrement=True)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.ingrediente_id'), nullable=False)
    capacidad_maxima = Column(Integer, nullable=False, default=1)
    cantidad_minima = Column(Integer, nullable=False, default=1)
    cantidad_actual = Column(Integer, nullable=False, default=0)
    ## Relaciones bidireccionales (consultas)
    ingrediente = relationship('Ingrediente', back_populates="inventario") # Uno a uno
    # Constraint -> calidad de los datos en capacidades y cantidades
    __table_args__ = (
        CheckConstraint('cantidad_actual >= 0', name='check_cantidad_actual_no_negativo'),
        CheckConstraint('capacidad_maxima >= 1', name='check_capacidad_maxima_positiva'),
        CheckConstraint('capacidad_maxima >= cantidad_minima', name='check_capacidad_maxima_mi_minima'), # capacidad_maxima_mayor_o_igual_a_cantidad_minima
        CheckConstraint('cantidad_minima >= 1', name='check_cantidad_minima_positiva')
    )


