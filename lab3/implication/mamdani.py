from __future__ import annotations
from .implication import Implication
from lab1.fuzzysets.operations import Operations


class Mamdami(Implication):

    def __init__(self, minimum):
        self.minimum = minimum
        if minimum:
            self.function = Operations.zadeh_and()
        else:
            self.function = Operations.product()

    def apply(self, a: float, b: float) -> float:
        return self.function.value_at(a, b)

    def has_local_semantics(self):
        return True

    def is_min(self):
        return self.minimum
