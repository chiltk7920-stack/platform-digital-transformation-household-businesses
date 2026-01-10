from domain.models.iseller_repository import ISellerRepository
from domain.models.seller import Seller
from typing import List, Optional
from infrastructure.models import Seller as SellerModel
from infrastructure.databases.mssql import session

class SellerRepository(ISellerRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, seller: Seller) -> SellerModel:
        try:
            model = SellerModel(
                household_id=seller.household_id,
                tax_code=seller.tax_code,
                name=seller.name,
                phone=seller.phone,
                address=seller.address,
                description=seller.description,
                status=seller.status,
                created_by=seller.created_by,
                updated_by=seller.updated_by,
                created_at=seller.created_at,
                updated_at=seller.updated_at
            )
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating seller: {str(e)}')

    def get_by_id(self, seller_id: int) -> Optional[SellerModel]:
        return self.session.query(SellerModel).filter_by(id=seller_id).first()

    def list(self) -> List[SellerModel]:
        return self.session.query(SellerModel).all()

    def update(self, seller: Seller) -> SellerModel:
        try:
            model = self.session.query(SellerModel).filter_by(id=seller.id).first()
            if not model:
                raise ValueError('Seller not found')

            if seller.household_id is not None:
                model.household_id = seller.household_id
            if seller.tax_code is not None:
                model.tax_code = seller.tax_code
            if seller.name is not None:
                model.name = seller.name
            if seller.phone is not None:
                model.phone = seller.phone
            if seller.address is not None:
                model.address = seller.address
            if seller.description is not None:
                model.description = seller.description
            if seller.status is not None:
                model.status = seller.status
            if seller.updated_by is not None:
                model.updated_by = seller.updated_by
            if seller.updated_at is not None:
                model.updated_at = seller.updated_at

            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating seller: {str(e)}')

    def delete(self, seller_id: int) -> None:
        try:
            model = self.session.query(SellerModel).filter_by(id=seller_id).first()
            if model:
                self.session.delete(model)
                self.session.commit()
            else:
                raise ValueError('Seller not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting seller: {str(e)}')

    def get_by_household_id(self, household_id: int) -> List[SellerModel]:
        return self.session.query(SellerModel).filter_by(household_id=household_id).all()
