from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    value: str | None

    def __post_init__(self):
        allowed_values = ["supermarket", 'restaurant', None]
        if self.value not in allowed_values:
            raise ValueError(f"Недопустимая категория: {self.value}")
