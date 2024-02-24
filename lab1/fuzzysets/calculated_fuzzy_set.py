from __future__ import annotations
from lab1.domain.i_domain import IDomain
from lab1.domain.domain_element import DomainElement
from .i_fuzzy_set import IFuzzySet


class CalculatedFuzzySet(IFuzzySet):
    def __init__(self, i_domain: IDomain, init_unary_function: InitUnaryFunction):
        self.i_domain = i_domain
        self.init_unary_function = init_unary_function

    def get_domain(self):
        return self.i_domain

    def get_value_at(self, domain_element: DomainElement) -> float:
        return self.init_unary_function.value_at(self.i_domain.index_of_element(domain_element))

    def iterator(self):
        values = []
        for e in self.i_domain.iterator():
            values.append(self.get_value_at(e))
        return zip(self.i_domain.iterator(), iter(values))

    def cut(self, min_value: float):
        class MinimizedFuzzySet(CalculatedFuzzySet):
            def __init__(self, i_domain: IDomain, init_unary_function: InitUnaryFunction, min_value: float):
                super().__init__(i_domain, init_unary_function)
                self.min_value = min_value

            def get_value_at(self, domain_element: DomainElement) -> float:
                index = self.get_domain().index_of_element(domain_element)
                if index != -1:
                    return min(self.init_unary_function.value_at(index), self.min_value)
                return -1

        return MinimizedFuzzySet(self.i_domain, self.init_unary_function, min_value)

    def scale(self, factor):
        class ScaledFuzzySet(CalculatedFuzzySet):
            def __init__(self, i_domain: IDomain, init_unary_function: InitUnaryFunction, factor: float):
                super().__init__(i_domain, init_unary_function)
                self.factor = factor

            def get_value_at(self, domain_element: DomainElement) -> float:
                index = self.get_domain().index_of_element(domain_element)
                if index != -1:
                    return self.init_unary_function.value_at(index) * self.factor
                return -1

        return ScaledFuzzySet(self.i_domain, self.init_unary_function, factor)


class InitUnaryFunction:
    def value_at(self, index: int) -> float:
        pass
