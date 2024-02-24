from __future__ import annotations
from lab1.domain.i_domain import IDomain
from lab1.domain.domain_element import DomainElement
from .i_fuzzy_set import IFuzzySet


class MutableFuzzySet(IFuzzySet):

    def __init__(self, i_domain: IDomain):
        self.i_domain = i_domain
        self.memberships = []
        for i in self.i_domain.iterator():
            self.memberships.append(0)

    def get_domain(self) -> IDomain:
        return self.i_domain

    def get_value_at(self, domain_element: DomainElement) -> float:
        return self.memberships[self.i_domain.index_of_element(domain_element)]

    def set(self, domain_element: DomainElement, value: float) -> None:
        if value < 0 or value > 1:
            raise Exception("invalid membership value")
        self.memberships[self.i_domain.index_of_element(domain_element)] = value

    def iterator(self):
        return zip(self.i_domain.iterator(), iter(self.memberships))

    def cut(self, min_value: float):
        class MinimizedFuzzySet(MutableFuzzySet):
            def __init__(self, i_domain: IDomain, min_value: float):
                super().__init__(i_domain)
                self.min_value = min_value

            def get_value_at(self, domain_element: DomainElement) -> float:
                index = self.get_domain().index_of_element(domain_element)
                value = self.memberships[index]
                if index != -1:
                    return min(value, self.min_value)
                return -1

        return MinimizedFuzzySet(self.i_domain, min_value)

    def scale(self, factor):
        class ScaledFuzzySet(MutableFuzzySet):
            def __init__(self, i_domain: IDomain, factor: float):
                super().__init__(i_domain)
                self.factor = factor

            def get_value_at(self, domain_element: DomainElement) -> float:
                index = self.get_domain().index_of_element(domain_element)
                value = self.memberships[index]
                if index != -1:
                    return value * self.factor
                return -1

        return ScaledFuzzySet(self.i_domain, factor)
