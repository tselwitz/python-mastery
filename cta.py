# readrides.py

import csv
import sys
from collections import namedtuple, defaultdict, Counter
import tracemalloc


class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class RowSlots:
    __slots__ = ['route', 'date', 'daytype', 'rides']

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


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


def read_rides_as_dictionary(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {"route": route, "date": date,
                      "daytype": daytype, "rides": rides}
            records.append(record)
    return records


def read_rides_as_class(filename):
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


def read_rides_as_named_tuple(filename):
    records = []
    Row = namedtuple("Row", ['route', 'date', 'daytype', 'rides'])
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            records.append(Row(route, date, daytype, rides))
    return records


def read_rides_as_class_w_slots(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = RowSlots(route, date, daytype, rides)
            records.append(record)
    return records


def num_routes(data):
    # Q: How many bus routes exist in Chicago?
    return len({d['route'] for d in data})


def riders_by_route_by_day(data, route, date):
    # Q: How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?
    tracemalloc.start()

    # # As a list
    record = [d for d in data if d["route"] == route and d["date"] == date]
    answer = record[0]["rides"]

    # As a generator
    # record = (d for d in data if d["route"] == route and d["date"] == date)
    # answer = ''
    # for row in record:
    #     answer = row

    # In this case, using the just a list is more memory efficient.
    print('Memory Use: Current %d, Peak %d' %
          tracemalloc.get_traced_memory())
    return answer


def total_rides_by_route(data):
    # Q: What is the total number of rides taken on each bus route?
    totals = {d["route"]: 0 for d in data}
    for d in data:
        totals[d["route"]] += d["rides"]
    return totals


def greatest_difference(data, year1, year2):
    # Q: What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?

    # Attempt 1. This solution works, but it's a lot less elegant.
    # increase = {d["route"]: 0 for d in data}
    # for d in data:
    #     if year1 in d["date"]:
    #         increase[d["route"]] -= d["rides"]
    #     if year2 in d["date"]:
    #         increase[d["route"]] += d["rides"]
    # return sorted(increase.items(), key=lambda x: x[1])[-5:]

    rides_by_year = defaultdict(Counter)
    for d in data:
        year = d["date"].split("/")[2]
        # rides_by_year[year] is a Counter([route: rides])
        rides_by_year[year][d["route"]] += d["rides"]

    return (rides_by_year[year2] - rides_by_year[year1]).most_common(5)


if __name__ == '__main__':
    filename = 'Data/ctabus.csv'
    rows = read_rides_as_dictionary(filename)
    print(f"Total number of routes: {num_routes(rows)}")
    print(
        f"Total number of riders for 22 on 02/02/11: {riders_by_route_by_day(rows, '22', '02/02/2011')}")
    print(f"Total number of rides by route: {total_rides_by_route(rows)}")
    print(
        f"Top 5 greatest increases in riders from 2001 to 2011: {greatest_difference(rows, '2001', '2011')}")

    # # Memory task. Note that slots classes were the most efficient.
    # tracemalloc.start()
    # if sys.argv[1] == "tuple":
    #     rows = read_rides_as_tuples(filename)
    # elif sys.argv[1] == "dict":
    #     rows = read_rides_as_dictionary(filename)
    # elif sys.argv[1] == "class":
    #     rows = read_rides_as_class(filename)
    # elif sys.argv[1] == "sclass":
    #     rows = read_rides_as_class_w_slots(filename)
    # elif sys.argv[1] == "nt":
    #     rows = read_rides_as_named_tuple(filename)
    # print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
