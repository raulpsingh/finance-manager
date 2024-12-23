from abc import ABC, abstractmethod

from src.domain.entities.transaction import Transaction


class ManagerRepository(ABC):

    @abstractmethod
    def add_transaction(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass

    @abstractmethod
    def get_transactions_by_category(self) -> list[Transaction]:
        pass

    @abstractmethod
    def get_transaction_by_dates(self) -> list[Transaction]:
        pass

    @abstractmethod
    def get_all_transactions(self) -> list[Transaction]:
        pass
