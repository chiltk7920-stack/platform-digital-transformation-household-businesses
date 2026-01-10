from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class Invoice(Base):
    __tablename__ = 'invoices'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    household_id=Column(Integer, ForeignKey("households.id"),nullable=False)
    seller_id=Column(Integer, ForeignKey("sellers.id"),nullable=True) # Hóa đơn mua
    customer_id=Column(Integer,ForeignKey("customers.id"),nullable=True) # Hóa đơn bán
    invoice_type=Column(String(50),nullable=False) 
    discount_total=Column(Numeric(10),nullable=True)
    vat_total=Column(Numeric(10),nullable=False)
    total_amount=Column(Numeric(10), nullable=False) # (quantity * price) - discount_total + vat_total
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)  # Draft / Confirm / Delete 
    created_by= Column(String(50),nullable=True) # Role Employee, Owner 
    updated_by= Column(String(50),nullable=True) # Role Employee, Owner
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
   
   
