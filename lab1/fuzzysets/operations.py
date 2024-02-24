from __future__ import annotations
from lab1.fuzzysets.i_fuzzy_set import IFuzzySet
from lab1.fuzzysets.mutable_fuzzy_set import MutableFuzzySet


class Operations:

    def __init__(self):
        pass

    @staticmethod
    def unary_operation(i_fuzzyset: IFuzzySet, i_unary_function: IUnaryFunction) -> IFuzzySet:
        new_set = MutableFuzzySet(i_fuzzyset.get_domain())
        for e, mem in i_fuzzyset.iterator():
            new_set.set(e, i_unary_function.value_at(mem))
        return new_set

    @staticmethod
    def binary_operation(first_fuzzy: IFuzzySet, second_fuzzy: IFuzzySet, i_binary_function: IBinaryFunction) -> IFuzzySet:
        if not first_fuzzy.get_domain() == second_fuzzy.get_domain():
            raise Exception("different domains")
        new_set = MutableFuzzySet(first_fuzzy.get_domain())
        iterator1 = first_fuzzy.iterator()
        iterator2 = second_fuzzy.iterator()

        for (e1, mem1), (e2, mem2) in zip(iterator1, iterator2):
            new_set.set(e1, i_binary_function.value_at(mem1, mem2))
        return new_set

    @staticmethod
    def zadeh_not() -> IUnaryFunction:
        class ZadehNot(IUnaryFunction):
            def value_at(self, index: float) -> float:
                return 1 - index
        return ZadehNot()

    @staticmethod
    def zadeh_and() -> IBinaryFunction:
        class ZadehAnd(IBinaryFunction):
            def value_at(self, first: float, second: float) -> float:
                return min(first, second)
        return ZadehAnd()

    @staticmethod
    def zadeh_or() -> IBinaryFunction:
        class ZadehOr(IBinaryFunction):
            def value_at(self, first: float, second: float) -> float:
                return max(first, second)
        return ZadehOr()

    @staticmethod
    def product() -> IBinaryFunction:
        class Product(IBinaryFunction):
            def value_at(self, first: float, second: float) -> float:
                return first * second
        return Product()

    @staticmethod
    def hamacher_t_norm(v: float) -> IBinaryFunction:
        if v < 0:
            raise Exception("invalid v")

        class HamacherTNorm(IBinaryFunction):
            def value_at(self, a: float, b: float) -> float:
                return a * b / (v + (1 - v) * (a + b - a * b))
        return HamacherTNorm()

    @staticmethod
    def hamacher_s_norm(v: float) -> IBinaryFunction:
        if v < 0:
            raise Exception("invalid v")

        class HamacherSNorm(IBinaryFunction):
            def value_at(self, a: float, b: float) -> float:
                return (a + b - (2 - v) * a * b) / (1 - (1 - v) * a * b)
        return HamacherSNorm()


class IBinaryFunction:
    def value_at(self, first: float, second: float) -> float:
        pass


class IUnaryFunction:
    def value_at(self, index: int) -> float:
        pass
