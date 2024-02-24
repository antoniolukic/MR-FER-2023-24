from __future__ import annotations
from .i_domain import IDomain
from .domain_element import DomainElement


class SimpleDomain(IDomain):

    def __init__(self, first: int, last: int):
        super().__init__()
        self.first = first
        self.last = last
        self.domain_elements = [DomainElement.of(element) for element in (list(range(self.first, self.last)))]

    def __eq__(self, other: SimpleDomain):
        if self.get_first() != other.get_first() or self.get_last() != other.get_last():
            return False
        return True

    def get_cardinality(self) -> int:
        return self.last - self.first

    def get_component(self, index: int) -> IDomain:
        return self

    def get_number_of_components(self) -> int:
        return 1

    def iterator(self):
        return iter(self.domain_elements)

    def get_first(self):
        return self.first

    def get_last(self):
        return self.last

    def index_of_element(self, domain_element: DomainElement) -> int:
        return self.domain_elements.index(domain_element)

    def element_for_index(self, index: int) -> DomainElement:
        if index >= self.last - self.first:
            raise Exception("invalid index")
        return self.domain_elements[index]
