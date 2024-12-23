from datetime import datetime

from src.application.interfaces.manager_repository import ManagerRepository
from src.domain.entities.transaction import Transaction
from src.domain.value_objects.category import Category
from src.domain.value_objects.purpose import Purpose


class AddTransactionUseCase:

    def __init__(self, repository: ManagerRepository) -> None:
        self.repository = repository

    def execute(self, amount: str, purpose: Purpose, category: Category | None) -> None:
        all_transactions = self.repository.get_all_transactions()
        transaction_id = max(
            (int(transaction.transaction_id) for transaction in all_transactions),
            default=0
        ) + 1
        if not amount.isdigit():
            raise ValueError("Неверная сумма")
        transaction = Transaction(transaction_id=transaction_id, amount=float(amount), purpose=purpose,
                                  category=category, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # type: ignore
        self.repository.add_transaction(transaction)
