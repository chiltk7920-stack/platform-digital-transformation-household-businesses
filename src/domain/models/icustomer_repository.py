from abc import ABC, abstractmethod
from .customer import Customer
from typing import List, Optional

class ICustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def list(self) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> None:
        pass

    @abstractmethod
    def get_by_household_id(self, household_id: int) -> List[Customer]:
        pass
