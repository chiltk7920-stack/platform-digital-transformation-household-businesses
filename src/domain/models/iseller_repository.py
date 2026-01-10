from abc import ABC, abstractmethod
from .seller import Seller
from typing import List, Optional

class ISellerRepository(ABC):
    @abstractmethod
    def add(self, seller: Seller) -> Seller:
        pass

    @abstractmethod
    def get_by_id(self, seller_id: int) -> Optional[Seller]:
        pass

    @abstractmethod
    def list(self) -> List[Seller]:
        pass

    @abstractmethod
    def update(self, seller: Seller) -> Seller:
        pass

    @abstractmethod
    def delete(self, seller_id: int) -> None:
        pass

    @abstractmethod
    def get_by_household_id(self, household_id: int) -> List[Seller]:
        pass
