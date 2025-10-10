from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Numeric, Identity,
    ForeignKey, Enum, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

# --- Enums ---
UserRole = Enum('administrador', 'vendedor', name='user_role')
TipoIngresoEnum = Enum('efectivo', 'transferencia', name='tipo_ingreso_enum')

# --- Usuario ---
class User(Base):
    __tablename__ = "user"

    user_id          = Column(Integer, primary_key=True, index=True)
    correo           = Column(String(255), nullable=False, unique=True, index=True)
    nombre_completo  = Column(String(150), nullable=True)
    contrasena_hash  = Column(String(255), nullable=False)
    role             = Column(UserRole, nullable=False, default='vendedor')
    activo           = Column(Boolean, nullable=False, default=True)
    creado_at        = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    actualizado_at   = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                              onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Inversas explícitas
    productos_creados    = relationship("Product", back_populates="creado_por",       foreign_keys="Product.creado_por_id")
    productos_editados   = relationship("Product", back_populates="actualizado_por",  foreign_keys="Product.actualizado_por_id")
    categorias_creadas   = relationship("Categoria", back_populates="creado_por",     foreign_keys="Categoria.creado_por_id")
    categorias_editadas  = relationship("Categoria", back_populates="actualizado_por",foreign_keys="Categoria.actualizado_por_id")

    # NUEVO: backrefs propios para Stock
    stocks_creados       = relationship("Stock", back_populates="creado_por",         foreign_keys="Stock.creado_por_id")
    stocks_actualizados  = relationship("Stock", back_populates="actualizado_por",    foreign_keys="Stock.actualizado_por_id")

# Índice opcional
Index("ix_user_full_name", User.nombre_completo)

# --- Catálogo: Categoría ---
class Categoria(Base):
    __tablename__ = "categoria"

    categoria_id        = Column(Integer, primary_key=True, index=True)
    nombre              = Column(String(100), nullable=False, unique=True)
    descripcion         = Column(String(255), nullable=True)
    estado              = Column(Boolean, default=True, nullable=False)

    creado_por_id       = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)
    actualizado_por_id  = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)

    fecha_creacion      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    fecha_actualizacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                 onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    productos           = relationship("Product", back_populates="categoria")
    creado_por          = relationship("User", back_populates="categorias_creadas",   foreign_keys=[creado_por_id])
    actualizado_por     = relationship("User", back_populates="categorias_editadas",  foreign_keys=[actualizado_por_id])

    ingresos            = relationship("Ingreso", back_populates="categoria")

# --- Catálogo: Producto ---
class Product(Base):
    __tablename__ = "product"

    producto_id         = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    codigo_barras       = Column(String(64), nullable=False, unique=True, index=True)
    nombre              = Column(String(255), nullable=False)

    categoria_id        = Column(Integer, ForeignKey("categoria.categoria_id", ondelete="SET NULL"), nullable=True)
    descripcion         = Column(String(255), nullable=True)
    precio_venta        = Column(Numeric(10, 2), nullable=False)
    costo               = Column(Numeric(10, 2), nullable=False)

    creado_por_id       = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)
    actualizado_por_id  = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)

    fecha_creacion      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    fecha_actualizacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                 onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    estado              = Column(Boolean, nullable=False, default=True)

    categoria           = relationship("Categoria", back_populates="productos")
    creado_por          = relationship("User", back_populates="productos_creados",   foreign_keys=[creado_por_id])
    actualizado_por     = relationship("User", back_populates="productos_editados",  foreign_keys=[actualizado_por_id])

    # NUEVO: relación con Stock
    stocks              = relationship("Stock", back_populates="producto")

# --- Inventario: Stock ---
class Stock(Base):
    __tablename__ = "stock"

    stock_id            = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)

    # Si NO quieres stocks huérfanos, usa CASCADE y nullable=False
    producto_id         = Column(Integer, ForeignKey("product.producto_id", ondelete="CASCADE"), nullable=False)

    # Si manejas multi-bodega, descomenta y crea la tabla bodega
    # bodega_id           = Column(Integer, ForeignKey("bodega.bodega_id", ondelete="CASCADE"), nullable=True)

    cantidad_actual     = Column(Integer, nullable=False, default=0)
    cantidad_minima     = Column(Integer, nullable=False, default=0)

    actualizado_por_id  = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)
    creado_por_id       = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)

    ultima_actualizacion= Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                 onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relaciones correctas
    producto            = relationship("Product", back_populates="stocks")
    creado_por          = relationship("User", back_populates="stocks_creados",       foreign_keys=[creado_por_id])
    actualizado_por     = relationship("User", back_populates="stocks_actualizados",  foreign_keys=[actualizado_por_id])

    __table_args__ = (
        # Descomenta si tienes bodega_id:
        # UniqueConstraint('producto_id', 'bodega_id', name='uq_stock_producto_bodega'),
    )

# --- Catálogos de movimientos ---
class TipoMovimiento(Base):
    __tablename__ = "tipo_movimiento"

    tipo_movimiento_id  = Column(Integer, primary_key=True, index=True)
    nombre              = Column(String(50), unique=True, nullable=False)   # 'ENTRADA', 'SALIDA', 'AJUSTE'
    descripcion         = Column(String(255), nullable=True)
    activo              = Column(Boolean, default=True, nullable=False)

    movimientos         = relationship("MovimientosStock", back_populates="tipo_movimiento")

class RefMovimiento(Base):
    __tablename__ = "ref_movimiento"

    ref_movimiento_id   = Column(Integer, primary_key=True, index=True)
    nombre              = Column(String(50), unique=True, nullable=False)   # 'Compra', 'Venta', etc.
    descripcion         = Column(String(255), nullable=True)
    activo              = Column(Boolean, default=True, nullable=False)

    movimientos         = relationship("MovimientosStock", back_populates="ref_movimiento")

# --- Historial de movimientos ---
class MovimientosStock(Base):
    __tablename__ = "movimientos_stock"

    movimiento_id       = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)

    stock_id            = Column(Integer, ForeignKey("stock.stock_id", ondelete="CASCADE"), nullable=False)
    producto_id         = Column(Integer, ForeignKey("product.producto_id", ondelete="CASCADE"), nullable=False)

    tipo_movimiento_id  = Column(Integer, ForeignKey("tipo_movimiento.tipo_movimiento_id"), nullable=False)
    ref_movimiento_id   = Column(Integer, ForeignKey("ref_movimiento.ref_movimiento_id"), nullable=False)

    cantidad            = Column(Integer, nullable=False)
    referencia_doc      = Column(String(64), nullable=True)   # factura/OC/etc
    nota                = Column(String(255), nullable=True)

    realizado_por_id    = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)
    fecha_creacion      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relaciones
    stock               = relationship("Stock", backref="movimientos")
    producto            = relationship("Product", lazy="joined")
    tipo_movimiento     = relationship("TipoMovimiento", back_populates="movimientos")
    ref_movimiento      = relationship("RefMovimiento", back_populates="movimientos")
    realizado_por       = relationship("User", backref="movimientos_stock")

    __table_args__ = (
        CheckConstraint('cantidad > 0', name='ck_mov_cantidad_pos'),
    )

# --- Ingresos ---
class Ingreso(Base):
    __tablename__ = "ingreso"

    ingreso_id       = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    monto            = Column(Numeric(10, 2), nullable=False)
    categoria_id     = Column(Integer, ForeignKey("categoria.categoria_id", ondelete="SET NULL"), nullable=True)
    fecha            = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    notas            = Column(String(255), nullable=True)
    cliente          = Column(String(150), nullable=True)
    tipo_ingreso     = Column(TipoIngresoEnum, nullable=False, index=True)

    categoria        = relationship("Categoria", back_populates="ingresos")

    __table_args__ = (
        CheckConstraint('monto >= 0', name='ck_ingreso_monto_no_negativo'),
    )
