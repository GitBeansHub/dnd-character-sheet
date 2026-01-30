path = "sheetroot/counters.csv"

with open(path, "r") as f:
    for line in f:
        partition=line.split(',')
        for i, item in enumerate(partition):
            partition[i] = item.strip()
        print(partition)

