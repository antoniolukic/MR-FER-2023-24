from __future__ import annotations
from .domain_element import DomainElement
from abc import ABC


class IDomain(ABC):

    def __eq__(self, other: IDomain) -> bool:
        for e1, e2 in zip(self.iterator(), other.iterator()):
            if e2 != e2:
                return False
        return True

    def get_cardinality(self) -> int:
        pass

    def get_component(self, index: int) -> IDomain:
        pass

    def get_number_of_components(self) -> int:
        pass

    def index_of_element(self, domain_element: DomainElement) -> int:
        pass

    def element_for_index(self, index: int) -> DomainElement:
        pass

    def iterator(self):
        pass
