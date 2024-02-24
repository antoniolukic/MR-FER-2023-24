from __future__ import annotations
from typing import List
from .i_domain import IDomain
from .simple_domain import SimpleDomain
from .domain_element import DomainElement
import itertools


class CompositeDomain(IDomain):

    def __init__(self, domains: List[SimpleDomain]):
        super().__init__()
        self.domains = domains

        lists = [(domain.get_first(), domain.get_last()) for domain in domains]
        lists = [list(range(t[0], t[1])) for t in lists]
        self.domain_elements = list(itertools.product(*lists))
        self.domain_elements = [DomainElement.of(*element) for element in self.domain_elements]

    def iterator(self):
        return iter(self.domain_elements)

    def get_cardinality(self) -> int:
        card = 1
        for i in self.domains:
            card *= i.get_cardinality()
        return card

    def get_component(self, index: int) -> IDomain:
        return self.domains[index]

    def get_number_of_components(self) -> int:
        return len(self.domains)

    def index_of_element(self, domain_element: DomainElement) -> int:
        return self.domain_elements.index(domain_element)

    def element_for_index(self, index: int) -> DomainElement:
        if index >= len(self.domain_elements):
            raise Exception("invalid index")
        return self.domain_elements[index]
