from __future__ import annotations
from .defuzzifier import Defuzzifier
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet


class MOMdefuzzifier(Defuzzifier):

    def defuzzify(self, i_fuzzyset: IFuzzySet) -> float:
        sum = 0
        counter = 0
        for domain, membership in i_fuzzyset.iterator():
            xi = domain.get_component_value(0)
            if 1 - membership <= 1e-6:
                sum += xi
                counter += 1

        if not counter:
            return 0
        return int(sum / counter)
