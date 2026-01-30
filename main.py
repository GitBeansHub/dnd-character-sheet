path = "sheetroot/counters.csv"
import csv

data = []
with open(path, "r") as f:
    reader = csv.reader(f)
    data = list(reader)


