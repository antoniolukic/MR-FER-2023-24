from __future__ import annotations
import sys

sys.path.append(r'C:your_path')
from lab1.domain.domain import Domain
from lab1.domain.domain_element import DomainElement
from lab1.fuzzysets.mutable_fuzzy_set import MutableFuzzySet
from lab1.fuzzysets.operations import Operations
from system.rudder_fuzzy_system import RudderFuzzySystem
from system.accelerator_fuzzy_system import AcceleratorFuzzySystem
from defuzzify.coa_defuzzifier import COAdefuzzifier
from implication.mamdani import Mamdami

coa_defuzzifier = COAdefuzzifier()

implication = Mamdami(True)  # definiran stroj temeljan na minimumu
tnorm = Operations.zadeh_and()
snorm = Operations.zadeh_or()

rudder_fuzzy_system = RudderFuzzySystem(implication, tnorm, snorm, coa_defuzzifier)
accelerator_fuzzy_system = AcceleratorFuzzySystem(implication, tnorm, snorm, coa_defuzzifier)
# ovisno o lokalnoj semantici norme (to je definirano u implikaciji)

while True:
    lnIn = input()
    if lnIn == "KRAJ":
        break
    inputs = [int(x) for x in lnIn.split(' ')]
    gas = accelerator_fuzzy_system.conclude(*inputs)
    turn = rudder_fuzzy_system.conclude(*inputs)
    print(gas, turn)
    sys.stdout.flush()

#inputs = [15, 100, 30, 120, 130, 1]

#print("kormilo:", rudder_fuzzy_system.conclude(*inputs))
#print("gas:", accelerator_fuzzy_system.conclude(*inputs))
