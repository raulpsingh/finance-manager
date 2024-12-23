from src.application.interfaces.manager_repository import ManagerRepository


class GetBalanceUseCase:
    def __init__(self, repository: ManagerRepository) -> None:
        self.repository = repository

    def execute(self) -> float:
        balance = self.repository.get_balance()
        return balance
