from __future__ import annotations
from typing import Tuple


class DomainElement:

    def __init__(self, values: Tuple) -> None:
        self.values = values

    def get_number_of_components(self) -> int:
        return len(self.values)

    def get_component_value(self, index: int) -> int:
        return self.values[index]

    def hash_code(self) -> int:
        return hash(self.values)

    def __eq__(self, other: DomainElement):
        for i, j in zip(self.values, other.values):
            if i != j:
                return False
        return True

    def __str__(self) -> str:
        return str(self.values)

    @staticmethod
    def of(*args: int) -> DomainElement:
        return DomainElement(tuple(args))
