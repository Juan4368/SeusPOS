from sqlalchemy.orm import Session

from infrastructure.database.models import Product


class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_producto_by_barcode_by_name(self, nombre: str | None, barcode: str | None) -> list[Product]:
        query = self.db.query(Product)

        if nombre:
            query = query.filter(Product.nombre.ilike(f"%{nombre}%"))
        if barcode:
            query = query.filter(Product.codigo_barras == barcode)

        return query.all()