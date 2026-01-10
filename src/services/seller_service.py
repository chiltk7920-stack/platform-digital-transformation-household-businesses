from domain.models.seller import Seller
from domain.models.iseller_repository import ISellerRepository
from typing import List, Optional
from datetime import datetime

class SellerService:
    def __init__(self, repository: ISellerRepository):
        self.repository = repository

    def create_seller(self, household_id: int = None, tax_code: str = None,
                      name: str = None, phone: str = None, address: str = None,
                      description: str = None, status: str = None, created_by: str = None) -> Seller:
        now = datetime.utcnow()
        seller = Seller(
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
        return self.repository.add(seller)

    def get_seller(self, seller_id: int) -> Optional[Seller]:
        return self.repository.get_by_id(seller_id)

    def list_sellers(self, household_id: int = None) -> List[Seller]:
        if household_id:
            return self.repository.get_by_household_id(household_id)
        return self.repository.list()

    def update_seller(self, seller_id: int, household_id: int = None, tax_code: str = None,
                      name: str = None, phone: str = None, address: str = None,
                      description: str = None, status: str = None, updated_by: str = None) -> Seller:
        now = datetime.utcnow()
        seller = Seller(
            id=seller_id,
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
        return self.repository.update(seller)

    def delete_seller(self, seller_id: int) -> None:
        self.repository.delete(seller_id)
