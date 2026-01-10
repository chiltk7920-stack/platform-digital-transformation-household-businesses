from domain.models.customer import Customer
from domain.models.icustomer_repository import ICustomerRepository
from typing import List, Optional
from datetime import datetime
from infrastructure.databases.mssql import session
from infrastructure.models import DebtRecord, Invoice

class CustomerService:
    def __init__(self, repository: ICustomerRepository):
        self.repository = repository

    def create_customer(self, household_id: int = None, tax_code: str = None,
                        name: str = None, phone: str = None, address: str = None,
                        description: str = None, status: str = None, created_by: str = None) -> Customer:
        now = datetime.utcnow()
        customer = Customer(
            id=None,
            household_id=household_id,
            tax_code=tax_code,
            name=name,
            phone=phone,
            address=address,
            description=description,
            status=status,
            created_by=created_by,
            created_at=now,
            updated_at=now
        )
        return self.repository.add(customer)

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.repository.get_by_id(customer_id)

    def list_customers(self, household_id: int = None) -> List[Customer]:
        if household_id:
            return self.repository.get_by_household_id(household_id)
        return self.repository.list()

    def update_customer(self, customer_id: int, household_id: int = None, tax_code: str = None,
                        name: str = None, phone: str = None, address: str = None,
                        description: str = None, status: str = None, updated_by: str = None) -> Customer:
        now = datetime.utcnow()
        customer = Customer(
            id=customer_id,
            household_id=household_id,
            tax_code=tax_code,
            name=name,
            phone=phone,
            address=address,
            description=description,
            status=status,
            updated_by=updated_by,
            updated_at=now
        )
        return self.repository.update(customer)

    def delete_customer(self, customer_id: int) -> None:
        self.repository.delete(customer_id)

    def get_purchase_history(self, customer_id: int):
        # Return invoices linked to this customer (most recent first)
        return session.query(Invoice).filter_by(customer_id=customer_id).order_by(Invoice.created_at.desc()).all()

    def get_debt(self, customer_id: int):
        records = session.query(DebtRecord).filter_by(customer_id=customer_id).all()
        total_debit = sum([float(r.debit_amount or 0) for r in records])
        total_credit = sum([float(r.credit_amount or 0) for r in records])
        outstanding = total_debit - total_credit
        return {
            'customer_id': customer_id,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'outstanding': outstanding
        }
