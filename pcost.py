def portfolio_cost(filePath):
    totalCost = 0
    with open(filePath, 'r') as f:
        for line in f:
            data = line.split()
            try:
                num = int(data[1])
                cost = float(data[2])
                totalCost += num * cost
            except ValueError as e:
                print(f"Could't parse: {line}")
                print(f"Reason: {e}")
    print(totalCost)


if __name__ == "__main__":
    portfolio_cost('Data/portfolio.dat')
