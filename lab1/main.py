from domain.domain import Domain
from lab1.debug import Debug
from domain.domain_element import DomainElement
from fuzzysets.mutable_fuzzy_set import MutableFuzzySet
from fuzzysets.calculated_fuzzy_set import CalculatedFuzzySet
from fuzzysets.standard_fuzzy_sets import StandardFuzzySets
from fuzzysets.operations import Operations


def demo1():
    d1 = Domain.int_range(0, 5)
    Debug.print_domain(d1, "Elementi domene d1:")

    d2 = Domain.int_range(0, 3)
    Debug.print_domain(d2, "Elementi domene d2:")

    d3 = Domain.combine(d1, d2)
    Debug.print_domain(d3, "Elementi domene d3:")

    print(d3.element_for_index(0))
    print(d3.element_for_index(5))
    print(d3.element_for_index(14))
    print(d3.index_of_element(DomainElement.of(4, 1)))


def demo2():
    d1 = Domain.int_range(0, 11)
    set1 = MutableFuzzySet(d1)
    set1.set(DomainElement.of(0), 1.0)
    set1.set(DomainElement.of(1), 0.8)
    set1.set(DomainElement.of(2), 0.6)
    set1.set(DomainElement.of(3), 0.4)
    set1.set(DomainElement.of(4), 0.2)
    Debug.print_fuzzyset(set1, "Set1:")

    d2 = Domain.int_range(-5, 6)
    set2 = CalculatedFuzzySet(d2, StandardFuzzySets.lambda_function(
        d2.index_of_element(DomainElement.of(-4)),
        d2.index_of_element(DomainElement.of(0)),
        d2.index_of_element(DomainElement.of(4))
    ))
    Debug.print_fuzzyset(set2, "Set2:")


def demo3():
    d = Domain.int_range(0, 11)
    set1 = MutableFuzzySet(d)
    set1.set(DomainElement.of(0), 1)
    set1.set(DomainElement.of(1), 0.8)
    set1.set(DomainElement.of(2), 0.6)
    set1.set(DomainElement.of(3), 0.4)
    set1.set(DomainElement.of(4), 0.2)
    Debug.print_fuzzyset(set1, "Set1:")

    notset1 = Operations.unary_operation(set1, Operations.zadeh_not())
    Debug.print_fuzzyset(notset1, "notSet1:")

    union = Operations.binary_operation(set1, notset1, Operations.zadeh_or())
    Debug.print_fuzzyset(union, "Set1 union notSet1:")

    hinters = Operations.binary_operation(set1, notset1, Operations.hamacher_t_norm(1.0))
    Debug.print_fuzzyset(hinters, "Set1 intersection with notSet1 using parameterised Hamacher T norm with parameter "
                                  "1.0:")


# demo1()
# demo2()
# demo3()
