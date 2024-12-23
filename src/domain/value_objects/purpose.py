from dataclasses import dataclass


@dataclass(frozen=True)
class Purpose:
    value: str

    def __post_init__(self):
        allowed_values = ["INCOME", "OUTCOME"]
        if self.value not in allowed_values:
            raise ValueError(f"Недопустимая цель: {self.value}")
