from __future__ import annotations
from lab1.fuzzysets.operations import IBinaryFunction
from lab3.implication.implication import Implication
from lab3.defuzzify.defuzzifier import Defuzzifier
from lab3.system.rule import Rule
from lab3.system.fuzzy_system import FuzzySystem
from lab3.system.constants import Constants


class AcceleratorFuzzySystem(FuzzySystem):

    def __init__(self, implication: Implication, tnorm: IBinaryFunction, snorm: IBinaryFunction,
                 defuzzifier: Defuzzifier):
        super().__init__(implication, tnorm, snorm, defuzzifier)
        # L, D, LK, DK, V, S
        r1 = Rule([Constants.very_close_to_shore, None, Constants.very_close_to_shore, None, Constants.high_velocity, None],
                  Constants.deaccelerate,
                  "Ako je L blizu obale i LK blizu obale i brz si onda uspori.")
        r2 = Rule([None, Constants.very_close_to_shore, None, Constants.very_close_to_shore, Constants.high_velocity, None],
                  Constants.deaccelerate,
                  "Ako je D blizu obale i DK blizu obale i brz si onda uspori.")
        r3 = Rule([None, None, None, None, Constants.low_velocity, Constants.direction],
                  Constants.accelerate,
                  "Ako je si spor i je S dobar smjer ubrzaj.")
        r4 = Rule([None, None, Constants.far_to_shore, Constants.far_to_shore, Constants.medium_velocity, None],
                  Constants.accelerate,
                  "Ako je L blizu obale i D blizu obale i srednje si brzine onda ubrzaj.")
        r5 = Rule([Constants.very_close_to_shore, None, Constants.very_close_to_shore, None, Constants.low_velocity, None],
                  Constants.accelerate,
                  "Ako je L blizu obale i D blizu obale i spor si onda ubrzaj.")
        r6 = Rule([None, Constants.very_close_to_shore, None, Constants.very_close_to_shore, Constants.low_velocity, None],
                  Constants.accelerate,
                  "Ako je L blizu obale i D blizu obale ubrzaj.")

        self.add_rules(r1, r2, r3, r4, r5, r6)
