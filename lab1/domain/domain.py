from __future__ import annotations
from .i_domain import IDomain
from .domain_element import DomainElement
from .simple_domain import SimpleDomain
from .composite_domain import CompositeDomain


class Domain(IDomain):

    def __init__(self):
        pass

    @staticmethod
    def int_range(a: int, b: int):
        return SimpleDomain(a, b)

    @staticmethod
    def combine(domain1: SimpleDomain, domain2: SimpleDomain) -> IDomain:
        return CompositeDomain([domain1, domain2])

    def index_of_element(self, domain_element: DomainElement) -> int:
        pass

    def element_for_index(self, index: int) -> DomainElement:
        pass
