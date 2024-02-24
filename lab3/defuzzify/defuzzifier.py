from __future__ import annotations
from abc import ABC
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet


class Defuzzifier(ABC):

    def defuzzify(self, i_fuzzyset: IFuzzySet) -> float:
        pass
