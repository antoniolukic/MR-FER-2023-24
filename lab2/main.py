from __future__ import annotations
from lab1.domain.domain import Domain
from lab1.domain.domain_element import DomainElement
from lab1.domain.i_domain import IDomain
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet
from lab1.fuzzysets.mutable_fuzzy_set import MutableFuzzySet
from relations import Relations


def demo1():
    u = Domain.int_range(1, 6)
    u2 = Domain.combine(u, u)

    r1 = MutableFuzzySet(u2)
    r1.set(DomainElement.of(1, 1), 1)
    r1.set(DomainElement.of(2, 2), 1)
    r1.set(DomainElement.of(3, 3), 1)
    r1.set(DomainElement.of(4, 4), 1)
    r1.set(DomainElement.of(5, 5), 1)
    r1.set(DomainElement.of(3, 1), 0.5)
    r1.set(DomainElement.of(1, 3), 0.5)

    r2 = MutableFuzzySet(u2)
    r2.set(DomainElement.of(1, 1), 1)
    r2.set(DomainElement.of(2, 2), 1)
    r2.set(DomainElement.of(3, 3), 1)
    r2.set(DomainElement.of(4, 4), 1)
    r2.set(DomainElement.of(5, 5), 1)
    r2.set(DomainElement.of(3, 1), 0.5)
    r2.set(DomainElement.of(1, 3), 0.1)

    r3 = MutableFuzzySet(u2)
    r3.set(DomainElement.of(1, 1), 1)
    r3.set(DomainElement.of(2, 2), 1)
    r3.set(DomainElement.of(3, 3), 0.3)
    r3.set(DomainElement.of(4, 4), 1)
    r3.set(DomainElement.of(5, 5), 1)
    r3.set(DomainElement.of(1, 2), 0.6)
    r3.set(DomainElement.of(2, 1), 0.6)
    r3.set(DomainElement.of(2, 3), 0.7)
    r3.set(DomainElement.of(3, 2), 0.7)
    r3.set(DomainElement.of(3, 1), 0.5)
    r3.set(DomainElement.of(1, 3), 0.5)

    r4 = MutableFuzzySet(u2)
    r4.set(DomainElement.of(1, 1), 1)
    r4.set(DomainElement.of(2, 2), 1)
    r4.set(DomainElement.of(3, 3), 1)
    r4.set(DomainElement.of(4, 4), 1)
    r4.set(DomainElement.of(5, 5), 1)
    r4.set(DomainElement.of(1, 2), 0.4)
    r4.set(DomainElement.of(2, 1), 0.4)
    r4.set(DomainElement.of(2, 3), 0.5)
    r4.set(DomainElement.of(3, 2), 0.5)
    r4.set(DomainElement.of(1, 3), 0.4)
    r4.set(DomainElement.of(3, 1), 0.4)

    test1 = Relations.is_u_times_u_relation(r1)
    print("r1 je definiran nad UxU?: " + str(test1))

    test2 = Relations.is_symmetric(r1)
    print("r1 je simetrična?: " + str(test2))

    test3 = Relations.is_symmetric(r2)
    print("r2 je simetrična?: " + str(test3))

    test4 = Relations.is_reflexive(r1)
    print("r1 je refleksivna?: " + str(test4))

    test5 = Relations.is_reflexive(r3)
    print("r3 je refleksivna?: " + str(test5))

    test6 = Relations.is_max_min_transitive(r3)
    print("r3 je max-min tranzitivna?: " + str(test6))

    test7 = Relations.is_max_min_transitive(r4)
    print("r4 je max-min tranzitivna?: " + str(test7))


def demo2():
    u1 = Domain.int_range(1, 5)
    u2 = Domain.int_range(1, 4)
    u3 = Domain.int_range(1, 5)

    r1 = MutableFuzzySet(Domain.combine(u1, u2))
    r1.set(DomainElement.of(1, 1), 0.3)
    r1.set(DomainElement.of(1, 2), 1)
    r1.set(DomainElement.of(3, 3), 0.5)
    r1.set(DomainElement.of(4, 3), 0.5)

    r2 = MutableFuzzySet(Domain.combine(u2, u3))
    r2.set(DomainElement.of(1, 1), 1)
    r2.set(DomainElement.of(2, 1), 0.5)
    r2.set(DomainElement.of(2, 2), 0.7)
    r2.set(DomainElement.of(3, 3), 1)
    r2.set(DomainElement.of(3, 4), 0.4)

    r1r2 = Relations.composition_of_binary_relations(r1, r2)
    for e in r1r2.get_domain().iterator():
        print("mu(" + str(e) + ")=" + str(r1r2.get_value_at(e)))


def demo3():
    u = Domain.int_range(1, 5)

    r = MutableFuzzySet(Domain.combine(u, u))
    r.set(DomainElement.of(1, 1), 1)
    r.set(DomainElement.of(2, 2), 1)
    r.set(DomainElement.of(3, 3), 1)
    r.set(DomainElement.of(4, 4), 1)
    r.set(DomainElement.of(1, 2), 0.3)
    r.set(DomainElement.of(2, 1), 0.3)
    r.set(DomainElement.of(2, 3), 0.5)
    r.set(DomainElement.of(3, 2), 0.5)
    r.set(DomainElement.of(3, 4), 0.2)
    r.set(DomainElement.of(4, 3), 0.2)

    r2 = r

    print("Početna relacija je neizrazita relacija ekvivalencije?: " + str(Relations.is_fuzzy_equivalence(r2)))
    print()

    for i in range(1, 4):
        r2 = Relations.composition_of_binary_relations(r2, r)

        print("Broj odrađenih kompozicija: " + str(i) + ". Relacija je:")

        for e in r2.get_domain().iterator():
            print("mu(" + str(e) + ")=" + str(r2.get_value_at(e)))

        print("Ova relacija je neizrazita relacija ekvivalencije? " + str(Relations.is_fuzzy_equivalence(r2)))
        print()


demo1()
# demo2()
# demo3()
