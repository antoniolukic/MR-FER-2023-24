from __future__ import annotations
from lab1.fuzzysets.operations import IBinaryFunction
from lab3.implication.implication import Implication
from lab3.defuzzify.defuzzifier import Defuzzifier
from lab3.system.rule import Rule
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet
from lab1.fuzzysets.operations import Operations
from typing import List


class FuzzySystem:

    def __init__(self, implication: Implication, tnorm: IBinaryFunction, snorm: IBinaryFunction,
                 defuzzifier: Defuzzifier):
        self.implication = implication
        self.tnorm = tnorm
        self.snorm = snorm
        self.defuzzifier = defuzzifier
        self.rules = []

    def add_rules(self, *rules: Rule):
        for rule in rules:
            self.rules.append(rule)

    def get_rules(self) -> List[Rule]:
        return self.rules

    def fuzzified_conclusion(self, *values: float) -> IFuzzySet:
        consequences = [rule.apply(values, self.implication, self.tnorm) for rule in self.rules]
        result = consequences[0]
        for i in range(1, len(consequences)):
            if self.implication.has_local_semantics():
                result = Operations.binary_operation(result, consequences[i], self.snorm)
            else:
                result = Operations.binary_operation(result, consequences[i], self.tnorm)
        return result

    def conclude(self, *values: float) -> float:
        return self.defuzzifier.defuzzify(self.fuzzified_conclusion(*values))
