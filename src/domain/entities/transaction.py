from dataclasses import dataclass
from typing import Optional

from src.domain.value_objects.category import Category
from src.domain.value_objects.purpose import Purpose


@dataclass
class Transaction:
    transaction_id: int
    amount: float
    purpose: Purpose
    timestamp: str
    category: Optional[Category]
