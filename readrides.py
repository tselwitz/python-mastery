# readrides.py

import collections.abc as collections
import csv


def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                'route': route,
                'date': date,
                'daytype': daytype,
                'rides': rides
            }
            records.append(record)
    return records


class Row:
    # Uncomment to see effect of slots
    # __slots__ = ('route', 'date', 'daytype', 'rides')
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

# Uncomment to use a namedtuple instead
# from collections import namedtuple
# Row = namedtuple('Row',('route','date','daytype','rides'))


def read_rides_as_instances(filename):
    '''
    Read the bus ride data as a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records


class RideData(collections.Sequence):
    def __init__(self):
        # Each value is a list with all of the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            return {'route': self.routes[index],
                    'date': self.dates[index],
                    'daytype': self.daytypes[index],
                    'rides': self.numrides[index]}
        elif isinstance(index, slice):
            if index.start is None:
                start = 1
            elif isinstance(index.start, int) and index.start < 0:
                start = len(self.routes) + index.start
            else:
                start = index.start
            if index.stop is None:
                stop = len(self.routes)
            elif isinstance(index.stop, int) and index.stop < 0:
                stop = len(self.routes) + index.stop
            else:
                stop = index.stop
            return [{'route': self.routes[index],
                     'date': self.dates[index],
                     'daytype': self.daytypes[index],
                     'rides': self.numrides[index]} for index in range(start, stop)]
        else:
            return NotImplemented

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])

    def __getitems__(self, index):
        return


if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    read_rides = read_rides_as_tuples  # Change to as_dicts, as_instances, etc.
    rides = read_rides_as_dicts("Data/ctabus.csv")

    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
    print(rides[-1:-1])
