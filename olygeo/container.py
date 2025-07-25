from abc import abstractmethod, ABC

from sympy import Symbol
import sympy as sp
from .point import ProPoint
from multimethod import multimethod
import inspect

class ProContainer(ABC):
    _unfixed_counter = 0

    _fields   = ()
    _defaults = {}

    def __init__(self, *args, **kwargs):
        values = {}
        if args:
            if len(args) > len(self._fields):
                raise TypeError(f"{self.__class__.__name__} takes at most "
                                f"{len(self._fields)} positional args ({len(args)} given)")
            for name, val in zip(self._fields, args):
                values[name] = val

        for name, val in kwargs.items():
            if name not in self._fields:
                raise TypeError(f"{self.__class__.__name__}.__init__() "
                                f"got an unexpected keyword argument '{name}'")
            if name in values:
                raise TypeError(f"{self.__class__.__name__}.__init__() "
                                f"got multiple values for argument '{name}'")
            values[name] = val

        for name in self._fields:
            if name not in values:
                if name in self._defaults:
                    values[name] = self._defaults[name]
                else:
                    raise TypeError(f"{self.__class__.__name__}.__init__() "
                                    f"missing required argument '{name}'")

        for name in self._fields:
            setattr(self, name, sp.sympify(values[name]))


    @classmethod
    def unfixed(cls):
        name = f"{cls.__name__}_{cls._unfixed_counter}"
        cls._unfixed_counter += 1

        sig    = inspect.signature(cls.__init__)
        params = list(sig.parameters.values())[1:]
        args   = []
        for i, p in enumerate(params):
            ann = p.annotation
            if inspect.isclass(ann) and issubclass(ann, ProContainer):
                args.append(ann.unfixed())
            else:
                args.append(Symbol(f"{name}_{i}"))

        return cls(*args)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return all(
            getattr(self, field) == getattr(other, field)
            for field in self._fields
        )

    def __hash__(self):
        return hash(tuple(getattr(self, field) for field in self._fields))


    @multimethod
    def intersection(self, other: "ProContainer"):
        raise TypeError(f"Cannot intersect {type(self).__name__} with {type(other).__name__}")

    @abstractmethod
    def is_eq(self, other, log=False):
        pass

    @abstractmethod
    def is_ne(self, other, log=False):
        pass

    @abstractmethod
    def contains(self, p: ProPoint, log=False):
        pass