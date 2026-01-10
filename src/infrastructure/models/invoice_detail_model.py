from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class InvoiceDetail(Base):
    __tablename__ = 'invoice_details'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    invoice_id=Column(Integer, ForeignKey("invoices.id"),nullable=False) # chi tiết hóa đơn 
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False) # Sản phẩm
    unit_id=Column(Integer,ForeignKey("units.id"),nullable=False) # đơn vị
    vat=Column(Integer,nullable=False) # % vat
    discount=Column(Integer, nullable=True) # % discount
    price=Column(Numeric(10), nullable=True)
    description = Column(String(255), nullable=True)
    quantity=Column(Integer,nullable=False)
    status = Column(String(50), nullable=False)  # Draft / Confirm / Delete 
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
