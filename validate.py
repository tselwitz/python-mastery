# validator.py
import inspect
from functools import wraps
import decimal


class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.signature = inspect.signature(func)
        self.annotation = dict(func.__annotations__)
        self.retcheck = self.annotations.pop('return', None)

    def __call__(self, *args, **kwargs):
        bound = self.signature.bind(*args, **kwargs)
        for name, val in self.annotation.items():
            val.check(bound.arguments[name])
        result = self.func(*args, **kwargs)
        if self.retcheck:
            self.retcheck.check(result)
        return result


def isvalidator(item):
    return isinstance(item, type) and issubclass(item, Validator)


def validated(func):
    sig = inspect.signature(func)

    # Gather the function annotations
    annotations = {name: val for name, val in func.__annotations__.items()
                   if isvalidator(val)}

    # Get the return annotation (if any)
    retcheck = annotations.pop('return', None)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        errors = []

        # Enforce argument checks
        for name, validator in annotations.items():
            try:
                validator.check(bound.arguments[name])
            except Exception as e:
                errors.append(f'  {name}: {e}')

        if errors:
            raise TypeError('Bad Arguments\n' + '\n'.join(errors))

        result = func(*args, **kwargs)

        # Enforce return check (if any)
        if retcheck:
            try:
                retcheck.check(result)
            except Exception as e:
                raise TypeError(f'Bad return: {e}') from None
        return result

    return wrapper


def enforce(**annotations):
    retcheck = annotations.pop("return_", None)

    def decorate(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            errors = []

            # Enforce argument checks
            for name, validator in annotations.items():
                try:
                    validator.check(bound.arguments[name])
                except Exception as e:
                    errors.append(f'  {name}: {e}')

            if errors:
                raise TypeError('Bad Arguments\n' + '\n'.join(errors))

            result = func(*args, **kwargs)

            # Enforce return check (if any)
            if retcheck:
                try:
                    retcheck.check(result)
                except Exception as e:
                    raise TypeError(f'Bad return: {e}') from None
            return result
        return wrapper
    return decorate


class Validator:
    validators = {}

    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)

    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls


class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        else:
            return super().check(value)


class Positive(Validator):
    expected_types = [float, int]

    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


_typed_classes = [
    ('Integer', int),
    ('Float', float),
    ('Complex', complex),
    ('Decimal', decimal.Decimal),
    ('List', list),
    ('Bool', bool),
    ('String', str)]

# globals is only within this package!
globals().update((name, type(name, (Typed,), {'expected_type': ty}))
                 for name, ty in _typed_classes)


class Stock:
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return "Stock('%s', %d, %.2f)" % (self.name, self.shares, self.price)

    def __eq__(self, other):
        return isinstance(other, Stock) and ((self.name, self.shares, self.price) ==
                                             (other.name, other.shares, other.price))

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        PositiveInteger.check(value)
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        PositiveFloat.check(value)
        self._price = value

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, shares):
        self.shares -= shares


if __name__ == "__main__":
    # # ValidatedFunction
    @validated
    def add(x: Integer, y: Integer) -> Integer:
        return x + y

    @validated
    def pow(x: Integer, y: Integer) -> Integer:
        return x ** y
    print(add(2, 3))
    print(pow(2, 3))

    @enforce(x=Integer, y=Integer, return_=Integer)
    def sub(x, y):
        return x - y
    print(sub(1, 1))

    # class Stock:
    #     def __init__(self, name, shares, price):
    #         self.name = name
    #         self.shares = shares
    #         self.price = price

    #     @property
    #     def cost(self):
    #         return self.shares * self.price

    #     def sell(self, nshares: Integer):
    #         self.shares -= nshares
    #     sell = ValidatedFunction(sell)
    # s = Stock("a", 12, 12.1)
    # s.sell(10)
