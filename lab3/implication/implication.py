from __future__ import annotations
from abc import ABC


class Implication(ABC):

    def apply(self, a: float, b: float) -> float:
        pass

    def has_local_semantics(self):
        pass
