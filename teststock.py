import unittest
import stock


class TestStock(unittest.TestCase):
    def test_create(self):
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_create_with_kwargs(self):
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_cost(self):
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        self.assertEqual(s.cost, 49010)

    def test_sell(self):
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        s.sell(1)
        self.assertEqual(s.shares, 99)

    def test_from_row(self):
        s = stock.Stock.from_row(['GOOG', 100, 490.1])
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_repr(self):
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        self.assertEqual(repr(s), "Stock('GOOG', 100, 490.1)")

    def test_eq(self):
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        t = stock.Stock(name='GOOG', shares=100, price=490.1)
        self.assertTrue(s == t)

    # Tests for failure conditions
    def test_shares_badtype(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
            s.shares = '50'

    def test_shares_badvalue(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(ValueError):
            s.shares = -50

    def test_price_badtype(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
            s.price = '45.23'

    def test_price_badvalue(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(ValueError):
            s.price = -45.23

    def test_bad_attribute(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(AttributeError):
            s.share = 100


if __name__ == '__main__':
    unittest.main()
