from sympy.core.relational import Relational
from sympy import true
from sympy import Piecewise
from sympy.logic.boolalg import BooleanFunction, BooleanAtom
import inspect

class ChoiceList(list):
    def choose(self, predicate):
        if not self:
            raise ValueError("Cannot choose from empty list")
        cls = type(self[0])
        sig = inspect.signature(cls.__init__)
        params = list(sig.parameters.keys())[1:]

        pw_args = {}
        for name in params:
            clauses = []
            for obj in self:
                val  = getattr(obj, name)
                cond = predicate(obj)
                if not isinstance(cond, (Relational, BooleanFunction, BooleanAtom)):
                    raise TypeError(f"predicate must return a Sympy Relational, got {type(cond)}")
                clauses.append((val, cond))

            clauses.append((getattr(self[-1], name), true))
            pw_args[name] = Piecewise(*clauses, evaluate=False)

        return cls(**pw_args)


