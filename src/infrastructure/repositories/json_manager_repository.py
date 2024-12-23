import json
import os

from src.application.interfaces.manager_repository import ManagerRepository
from src.domain.entities.transaction import Transaction
from src.domain.value_objects.category import Category
from src.domain.value_objects.purpose import Purpose


class JsonManagerRepository(ManagerRepository):

    def __init__(self, data_file: str) -> None:
        self._data_file = data_file
        self._ensure_file_exists()
        self.transactions = self._load_transactions()

    def _ensure_file_exists(self):
        if not os.path.exists(self._data_file):
            with open(self._data_file, 'w', encoding='utf-8') as file:
                json.dump([], file)

    def _load_transactions(self) -> list[Transaction]:
        try:
            with open(self._data_file, "r", encoding="utf-8") as file:
                return [
                    Transaction(
                        transaction_id=transaction["transaction_id"],
                        amount=transaction['amount'],
                        purpose=Purpose(transaction["purpose"]),
                        timestamp=transaction['timestamp'],
                        category=Category(transaction["category"])
                    ) for transaction in json.load(file)
                ]
        except FileNotFoundError:
            with open(self._data_file, "w", encoding="utf-8") as file:
                json.dump([], file)
            return []

    def _save_transactions(self) -> None:

        with open(self._data_file, "w", encoding="utf-8") as file:
            json.dump([
                {
                    "transaction_id": transaction.transaction_id,
                    'amount': transaction.amount,
                    "purpose": transaction.purpose.value,
                    "timestamp": transaction.timestamp,
                    "category": transaction.category.value  # type: ignore
                } for transaction in self.transactions
            ], file, indent=4, ensure_ascii=False)

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        self._save_transactions()

    def get_balance(self) -> float:
        balance = 0.0
        for transaction in self.transactions:
            if transaction.purpose.value == "INCOME":
                balance += transaction.amount
            elif transaction.purpose.value == "OUTCOME":
                balance -= transaction.amount
        return balance

    def get_all_transactions(self) -> list[Transaction]:
        return self.transactions

    def get_transactions_by_category(self) -> list[Transaction]:
        pass

    def get_transaction_by_dates(self) -> list[Transaction]:
        pass
