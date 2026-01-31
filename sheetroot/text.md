path = "sheetroot/counters.csv"
import csv
data=[]
with open(path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    data=list(reader)
print(data)
