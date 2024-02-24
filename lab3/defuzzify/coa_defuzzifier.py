from __future__ import annotations
from .defuzzifier import Defuzzifier
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet


class COAdefuzzifier(Defuzzifier):

    def defuzzify(self, i_fuzzyset: IFuzzySet) -> float:
        nominator = 0
        denominator = 0
        for domain, membership in i_fuzzyset.iterator():
            nominator += membership * domain.get_component_value(0)
            denominator += membership

        if abs(denominator) <= 1e-9:
            return 0
        return int(nominator / denominator)
