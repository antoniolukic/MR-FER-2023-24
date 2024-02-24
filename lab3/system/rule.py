from __future__ import annotations
from typing import List
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet
from lab1.fuzzysets.operations import IBinaryFunction
from lab1.domain.domain_element import DomainElement
from lab3.implication.mamdani import Mamdami


class Rule:

    def __init__(self, antecedent: List[IFuzzySet], consequence: IFuzzySet, description: str):
        self.antecedent = antecedent
        self.consequence = consequence
        self.description = description

    def apply(self, values: List[float], implication: Mamdami, tnorm: IBinaryFunction) -> IFuzzySet:
        mi = 1.0
        for i in range(len(self.antecedent)):
            if self.antecedent[i] is not None:
                # t_norma nad antecedensima, krisp vrijednosti samo 1 ce ostati jedan
                mi = tnorm.value_at(mi, self.antecedent[i].get_value_at(DomainElement.of(int(values[i]))))
        if implication.is_min():
            return self.consequence.cut(mi)
        return self.consequence.scale(mi)

    def get_description(self):
        return self.description
