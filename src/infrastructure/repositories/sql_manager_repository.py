import sqlite3

from src.application.interfaces.manager_repository import ManagerRepository
from src.domain.entities.transaction import Transaction
from src.domain.value_objects.category import Category
from src.domain.value_objects.purpose import Purpose


class SqlManagerRepository(ManagerRepository):

    def __init__(self, database_file: str) -> None:
        self._database_file = database_file
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Создаёт таблицу transactions, если её нет."""
        with sqlite3.connect(self._database_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    amount REAL NOT NULL,
                    purpose TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    category TEXT
                )
                """
            )

    def _execute_query(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Выполняет запрос к базе данных и возвращает результат."""
        with sqlite3.connect(self._database_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()

    def _fetch_transactions(self) -> list[sqlite3.Row]:
        """Извлекает все транзакции из базы данных."""
        return self._execute_query("SELECT * FROM transactions")

    def _insert_transaction(self, transaction: Transaction):
        """Добавляет транзакцию в базу данных."""
        self._execute_query(
            """
            INSERT INTO transactions (transaction_id, amount, purpose, timestamp, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                transaction.transaction_id,
                transaction.amount,
                transaction.purpose.value,
                transaction.timestamp,
                transaction.category.value if transaction.category else None,
            ),
        )

    def _row_to_transaction(self, row: sqlite3.Row) -> Transaction:
        """Преобразует строку из базы данных в объект Transaction."""
        return Transaction(
            transaction_id=row["transaction_id"],
            amount=row["amount"],
            purpose=Purpose(row["purpose"]),
            timestamp=row["timestamp"],
            category=Category(row["category"]) if row["category"] else None,
        )

    def add_transaction(self, transaction: Transaction) -> None:
        """Добавляет транзакцию в репозиторий."""
        self._insert_transaction(transaction)

    def get_balance(self) -> float:
        """Возвращает текущий баланс."""
        balance = 0.0
        transactions = self._fetch_transactions()
        for row in transactions:
            purpose = row["purpose"]
            amount = row["amount"]
            if purpose == "INCOME":
                balance += amount
            elif purpose == "OUTCOME":
                balance -= amount
        return balance

    def get_all_transactions(self) -> list[Transaction]:
        """Возвращает список всех транзакций."""
        rows = self._fetch_transactions()
        return [self._row_to_transaction(row) for row in rows]

    def get_transactions_by_category(self) -> list[Transaction]:
        pass

    def get_transaction_by_dates(self) -> list[Transaction]:
        pass
