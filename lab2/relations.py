from __future__ import annotations
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet
from lab1.fuzzysets.mutable_fuzzy_set import MutableFuzzySet
from lab1.domain.domain_element import DomainElement
from lab1.domain.domain import Domain
import itertools
import numpy as np


class Relations:

    def __init__(self):
        pass

    @staticmethod
    def is_symmetric(relation: IFuzzySet) -> bool:
        if not Relations.is_u_times_u_relation(relation):
            return False
        domain = relation.get_domain()
        for i in domain.iterator():
            rev = DomainElement.of(i.get_component_value(1), i.get_component_value(0))
            if abs(relation.get_value_at(i) - relation.get_value_at(rev)) >= 1e-9:
                return False
        return True

    @staticmethod
    def is_reflexive(relation: IFuzzySet) -> bool:
        if not Relations.is_u_times_u_relation(relation):
            return False
        domain = relation.get_domain()
        for i in domain.iterator():
            if abs(i.get_component_value(0) - i.get_component_value(1)) <= 1e-9 \
                    and abs(relation.get_value_at(i) - 1) >= 1e-9:
                return False
        return True

    @staticmethod
    def is_max_min_transitive(relation: IFuzzySet) -> bool:
        if not Relations.is_u_times_u_relation(relation):
            return False
        domain = relation.get_domain()
        maximum, minimum = -1, 2
        for i in domain.iterator():
            value = relation.get_value_at(i)
            x, z = i.get_component_value(0), i.get_component_value(1)
            maximum = -1
            for j in domain.iterator():
                if x == j.get_component_value(0):
                    y = j.get_component_value(1)
                    minimum = 2
                    for k in domain.iterator():
                        if y == k.get_component_value(0) and z == k.get_component_value(1):
                            minimum = min(relation.get_value_at(j), relation.get_value_at(k))
                            break
                maximum = max(maximum, minimum)
            if maximum != -1 and minimum != 2 and value < maximum:
                return False
        return True

    @staticmethod
    def composition_of_binary_relations(relation1: IFuzzySet, relation2: IFuzzySet) -> IFuzzySet:
        domain1 = relation1.get_domain()
        domain2 = relation2.get_domain()
        v1 = domain1.get_component(1)
        v2 = domain2.get_component(0)
        if not v1 == v2:
            raise Exception("domains are not compatible")

        matrix1 = np.zeros((domain1.get_component(0).get_cardinality(), domain1.get_component(1).get_cardinality()))
        matrix2 = np.zeros((domain2.get_component(0).get_cardinality(), domain2.get_component(1).get_cardinality()))
        composed = np.zeros((domain1.get_component(0).get_cardinality(), domain2.get_component(1).get_cardinality()))

        for i in relation1.iterator():
            matrix1[i[0].get_component_value(0) - 1][i[0].get_component_value(1) - 1] = i[1]
        for i in relation2.iterator():
            matrix2[i[0].get_component_value(0) - 1][i[0].get_component_value(1) - 1] = i[1]

        for i in range(matrix1.shape[0]):
            for j in range(matrix2.shape[1]):
                max_val = float('-inf')
                for k in range(matrix1.shape[1]):
                    max_val = max(max_val, min(matrix1[i, k], matrix2[k, j]))
                composed[i, j] = max_val

        new_relation = MutableFuzzySet(Domain.combine(domain1.get_component(0), domain2.get_component(1)))
        for i in range(len(composed)):
            for j in range(len(composed[0])):
                new_relation.set(DomainElement.of(i + 1, j + 1), composed[i][j])

        return new_relation

    @staticmethod
    def is_fuzzy_equivalence(relation: IFuzzySet) -> bool:
        if Relations.is_reflexive(relation) and\
           Relations.is_symmetric(relation) and\
           Relations.is_max_min_transitive(relation):
            return True
        return False

    @staticmethod
    def is_u_times_u_relation(relation: IFuzzySet) -> bool:
        domain = relation.get_domain()
        if domain.get_number_of_components() != 2:
            return False
        # a1, b1 = domain.get_component(0).get_first(), domain.get_component(0).get_last()
        # a2, b2 = domain.get_component(1).get_first(), domain.get_component(1).get_last()
        # if not (a1 == a2 and b1 == b2):
        #    return False
        # return True
        first, pf = domain.get_component(0).iterator(), domain.get_component(0).iterator()
        second, ps = domain.get_component(1).iterator(), domain.get_component(1).iterator()
        if domain.get_component(0).get_cardinality() != domain.get_component(1).get_cardinality():
            return False
        for i, j in zip(first, second):
            if i != j:
                return False
        cartesian = list(itertools.product(pf, ps))
        if len(cartesian) != domain.get_cardinality():
            return False
        for i, value in enumerate(cartesian):
            dom = (domain.element_for_index(i).get_component_value(0), domain.element_for_index(i).get_component_value(1))
            cart = (value[0].get_component_value(0), value[1].get_component_value(0))
            if dom != cart:
                return False
        return True
