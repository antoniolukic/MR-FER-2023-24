from __future__ import annotations
from lab1.domain.i_domain import IDomain
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet


class Debug:
    @staticmethod
    def print_domain(domain: IDomain, heading_text: str):
        if heading_text is not None:
            print(heading_text)
        for e in domain.iterator():
            print("Element domene: " + str(e))
        print("Kardinalitet domene je: " + str(domain.get_cardinality()))
        print()

    @staticmethod
    def print_fuzzyset(fuzzy_set: IFuzzySet, heading_text: str):
        if heading_text is not None:
            print(heading_text)
        for d, mem in fuzzy_set.iterator():
            print("d{0}={1:.5f}".format(d, mem))
        print()
