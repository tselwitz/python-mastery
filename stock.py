# stock.py
from decimal import Decimal
from reader import read_csv_as_instances


class Stock:
    __slots__ = ('name', '_shares', '_price')
    _types = (str, int, float)

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
        if not isinstance(value, self._types[1]):
            raise TypeError(f'Expected {self._types[1].__name__}')
        if value < 0:
            raise ValueError('shares must be >= 0')
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f'Expected {self._types[2].__name__}')
        if value < 0:
            raise ValueError('price must be >= 0')
        self._price = value

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, shares):
        self.shares -= shares


class DStock(Stock):
    _types = (str, int, Decimal)


def print_portfolio(portfolio):
    print('%10s %10s %10s' % ("name", "shares", "price"))
    print('-'*33)
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))


if __name__ == "__main__":
    filename = "Data/portfolio.csv"
    portfolio = read_csv_as_instances(filename, DStock)
    print_portfolio(portfolio)
    print(repr(portfolio))
