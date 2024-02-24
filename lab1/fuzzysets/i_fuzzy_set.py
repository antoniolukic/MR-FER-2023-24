from __future__ import annotations
from abc import ABC
from lab1.domain.i_domain import IDomain
from lab1.domain.domain_element import DomainElement


class IFuzzySet(ABC):

    def get_domain(self) -> IDomain:
        pass

    def get_value_at(self, domain_element: DomainElement) -> float:
        pass

    def iterator(self):
        pass

    def cut(self, mi: float):
        pass

    def scale(self, mi):
        pass
