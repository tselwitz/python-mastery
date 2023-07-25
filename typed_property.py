# typedproperty.py

class typedproperty:
    expected_type = object

    def __set_name__(self, cls, name):
        self.name = name
        self.private_name = "_" + name

    @property
    def value(self):
        return getattr(self, self.private_name)

    def __set__(self, instance, val):
        if not isinstance(val, self.expected_type):
            raise TypeError(f'Expected {self.expected_type}')
        return setattr(self, self.private_name, val)

    def __repr__(self) -> str:
        return str(self.value)


class String(typedproperty):
    expected_type = str


class Float(typedproperty):
    expected_type = float


class Integer(typedproperty):
    expected_type = int


# Example
if __name__ == '__main__':
    class Stock:
        name = String()
        shares = Integer()
        price = Float()

        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price
    s = Stock("GOOG", 123, 123.1)
    print(s.name)
    print(s.shares)
    print(s.price)
