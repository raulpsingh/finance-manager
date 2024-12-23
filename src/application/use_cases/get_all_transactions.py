from src.application.interfaces.manager_repository import ManagerRepository
from src.domain.entities.transaction import Transaction


class GetAllTransactionsUseCase:
    def __init__(self, repository: ManagerRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Transaction]:
        transactions = self.repository.get_all_transactions()
        return transactions
