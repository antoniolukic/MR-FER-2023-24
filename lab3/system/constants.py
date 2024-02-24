from __future__ import annotations
from lab1.domain.domain import Domain
from lab1.domain.domain_element import DomainElement
from lab1.fuzzysets.calculated_fuzzy_set import CalculatedFuzzySet
from lab1.fuzzysets.mutable_fuzzy_set import MutableFuzzySet
from lab1.fuzzysets.standard_fuzzy_sets import StandardFuzzySets


class Constants:

    distances_domain = Domain.int_range(0, 1301)
    velocity_domain = Domain.int_range(0, 200)
    acceleration_domain = Domain.int_range(-50, 51)
    angles_domain = Domain.int_range(-90, 91)
    direction_domain = Domain.int_range(0, 2)

    accelerate = CalculatedFuzzySet(acceleration_domain, StandardFuzzySets.gamma_function(50, 100))

    deaccelerate = CalculatedFuzzySet(acceleration_domain, StandardFuzzySets.l_function(0, 50))

    turn_left_sharp = CalculatedFuzzySet(angles_domain, StandardFuzzySets.gamma_function(150, 170))

    turn_left_light = CalculatedFuzzySet(angles_domain, StandardFuzzySets.gamma_function(110, 180))

    turn_right_sharp = CalculatedFuzzySet(angles_domain, StandardFuzzySets.l_function(10, 40))
    
    turn_right_light = CalculatedFuzzySet(angles_domain, StandardFuzzySets.l_function(0, 70))

    close_to_shore = CalculatedFuzzySet(distances_domain, StandardFuzzySets.l_function(50, 80))

    very_close_to_shore = CalculatedFuzzySet(distances_domain, StandardFuzzySets.l_function(15, 35))

    far_to_shore = CalculatedFuzzySet(distances_domain, StandardFuzzySets.gamma_function(60, 80))

    low_velocity = CalculatedFuzzySet(velocity_domain, StandardFuzzySets.l_function(20, 60))

    medium_velocity = CalculatedFuzzySet(velocity_domain, StandardFuzzySets.lambda_function(60, 70, 80))

    high_velocity = CalculatedFuzzySet(velocity_domain, StandardFuzzySets.gamma_function(60, 100))

    direction = MutableFuzzySet(direction_domain)
    direction.set(DomainElement.of(1), 1.0)
