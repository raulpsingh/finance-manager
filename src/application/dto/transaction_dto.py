from dataclasses import dataclass

from src.domain.entities.transaction import Transaction


@dataclass
class TransactionDTO:
    transaction_id: int
    amount: float
    purpose: str
    category: str
    date: str

    @staticmethod
    def from_transaction(transaction: Transaction) -> "TransactionDTO":
        return TransactionDTO(
            transaction_id=transaction.transaction_id,
            amount=transaction.amount,
            purpose=transaction.purpose.value,
            category=transaction.category.value if transaction.category else "Без категории",  # type: ignore
            date=transaction.timestamp
        )

    def __repr__(self) -> str:
        return f"{self.transaction_id} - {self.amount} - {self.purpose} - {self.category} - {self.date}"
