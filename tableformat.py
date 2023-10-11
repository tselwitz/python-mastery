from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [fmt % d for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


class MyFormatter:
    # Errors because not an instance of TableFormatter
    def headings(self, headers): pass
    def row(self, rowdata): pass


class NewFormatter(TableFormatter):
    # Errors because of "TypeError: Can't instantiate abstract class NewFormatter with abstract methods headings"
    def headers(self, headings):
        pass

    def row(self, rowdata):
        pass


def create_formatter(type, column_formats=None, upper_headers=False):
    if type == "text":
        formatter_cls = TextTableFormatter
    elif type == "csv":
        formatter_cls = CSVTableFormatter
    elif type == "html":
        formatter_cls = HTMLTableFormatter
    elif type == "haha":
        formatter_cls = MyFormatter
    elif type == "abstract":
        formatter_cls = NewFormatter
    elif type == "port":
        formatter_cls = PortfolioFormatter
    else:
        raise RuntimeError('Unknown format %s' % type)
    if column_formats:
        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats
    if upper_headers:
        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass
    return formatter_cls()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))

    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join('%s' % h for h in headers))

    def row(self, rowdata):
        print(','.join('%s' % d for d in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr>", end=" ")
        print(' '.join('<th>%s</th>' % h for h in headers), end=" </tr>\n")

    def row(self, rowdata):
        print("<tr>", end=" ")
        print(','.join('<td>%s</td>' % d for d in rowdata), end=" </tr>\n")


class PortfolioFormatter(UpperHeadersMixin, TextTableFormatter):
    formats = ['%s', '%d', '%0.2f']


def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError()
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)


if __name__ == "__main__":
    import orig_stock
    import reader
    portfolio = reader.read_csv_as_instances(
        'Data/portfolio.csv', orig_stock.Stock)
    formatter = create_formatter("text", column_formats=[
                                 "%s", "%d", "%0.2f"], upper_headers=True)
    print_table(portfolio, ['name', 'shares', 'price'], formatter)
