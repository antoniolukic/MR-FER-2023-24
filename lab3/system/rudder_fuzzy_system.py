from __future__ import annotations
from lab1.fuzzysets.operations import IBinaryFunction
from lab3.implication.implication import Implication
from lab3.defuzzify.defuzzifier import Defuzzifier
from lab3.system.rule import Rule
from lab3.system.fuzzy_system import FuzzySystem
from lab3.system.constants import Constants


class RudderFuzzySystem(FuzzySystem):

    def __init__(self, implication: Implication, tnorm: IBinaryFunction, snorm: IBinaryFunction,
                 defuzzifier: Defuzzifier):
        super().__init__(implication, tnorm, snorm, defuzzifier)
        # L, D, LK, DK, V, S
        r1 = Rule([Constants.close_to_shore, None, Constants.close_to_shore, None, None, None],
                  Constants.turn_right_sharp,
                  "Ako je L blizu obale i LK blizu obale onda okreni kormilo udesno.")
        r2 = Rule([None, None, Constants.close_to_shore, None, None, None],
                  Constants.turn_right_light,
                  "Ako je L blizu obale i LK blizu obale onda okreni kormilo udesno.")
        r3 = Rule([None, Constants.close_to_shore, None, Constants.close_to_shore, None, None],
                  Constants.turn_left_sharp,
                  "Ako je D blizu obale i DK blizu obale onda okreni kormilo ulijevo.")
        r4 = Rule([None, None, None, Constants.close_to_shore, None, None],
                  Constants.turn_left_light,
                  "Ako je D blizu obale i DK blizu obale onda okreni kormilo ulijevo.")

        self.add_rules(r1, r2, r3, r4)
