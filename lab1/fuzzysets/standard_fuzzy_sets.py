from __future__ import annotations
from .calculated_fuzzy_set import InitUnaryFunction


class StandardFuzzySets:

    def __init__(self):
        pass

    @staticmethod
    def l_function(alfa: int, beta: int) -> InitUnaryFunction:
        class LFunction(InitUnaryFunction):
            def value_at(self, index: int) -> float:
                if index < alfa:
                    return 1.0
                elif alfa <= index < beta:
                    return (beta - index) / (beta - alfa)
                elif index >= beta:
                    return 0.0
        return LFunction()

    @staticmethod
    def gamma_function(alfa: int, beta: int) -> InitUnaryFunction:
        class GammaFunction(InitUnaryFunction):
            def value_at(self, index: int) -> float:
                if index < alfa:
                    return 0.0
                elif alfa <= index < beta:
                    return (index - alfa) / (beta - alfa)
                elif index >= beta:
                    return 1.0
        return GammaFunction()

    @staticmethod
    def lambda_function(alfa: int, beta: int, gamma: int) -> InitUnaryFunction:
        class LambdaFunction(InitUnaryFunction):
            def value_at(self, index: int) -> float:
                if index < alfa:
                    return 0.0
                elif alfa <= index < beta:
                    return (index - alfa) / (beta - alfa)
                elif beta <= index < gamma:
                    return (gamma - index) / (gamma - beta)
                elif index >= gamma:
                    return 0.0
        return LambdaFunction()
