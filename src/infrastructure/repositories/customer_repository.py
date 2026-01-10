from domain.models.icustomer_repository import ICustomerRepository
from domain.models.customer import Customer
from typing import List, Optional
from infrastructure.models import Customer as CustomerModel
from infrastructure.databases.mssql import session

class CustomerRepository(ICustomerRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, customer: Customer) -> CustomerModel:
        try:
            model = CustomerModel(
                household_id=customer.household_id,
                tax_code=customer.tax_code,
                name=customer.name,
                phone=customer.phone,
                address=customer.address,
                description=customer.description,
                status=customer.status,
                created_by=customer.created_by,
                updated_by=customer.updated_by,
                created_at=customer.created_at,
                updated_at=customer.updated_at
            )
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating customer: {str(e)}')

    def get_by_id(self, customer_id: int) -> Optional[CustomerModel]:
        return self.session.query(CustomerModel).filter_by(id=customer_id).first()

    def list(self) -> List[CustomerModel]:
        return self.session.query(CustomerModel).all()

    def update(self, customer: Customer) -> CustomerModel:
        try:
            model = self.session.query(CustomerModel).filter_by(id=customer.id).first()
            if not model:
                raise ValueError('Customer not found')

            if customer.household_id is not None:
                model.household_id = customer.household_id
            if customer.tax_code is not None:
                model.tax_code = customer.tax_code
            if customer.name is not None:
                model.name = customer.name
            if customer.phone is not None:
                model.phone = customer.phone
            if customer.address is not None:
                model.address = customer.address
            if customer.description is not None:
                model.description = customer.description
            if customer.status is not None:
                model.status = customer.status
            if customer.updated_by is not None:
                model.updated_by = customer.updated_by
            if customer.updated_at is not None:
                model.updated_at = customer.updated_at

            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating customer: {str(e)}')

    def delete(self, customer_id: int) -> None:
        try:
            model = self.session.query(CustomerModel).filter_by(id=customer_id).first()
            if model:
                self.session.delete(model)
                self.session.commit()
            else:
                raise ValueError('Customer not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting customer: {str(e)}')

    def get_by_household_id(self, household_id: int) -> List[CustomerModel]:
        return self.session.query(CustomerModel).filter_by(household_id=household_id).all()
