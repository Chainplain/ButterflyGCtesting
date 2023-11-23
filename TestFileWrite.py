import csv

File_name = "just4test.csv"
Record = [1,2,3,4]
with open(File_name, 'w',newline='') as file:
    writer = csv.writer(file)
    for i in range(3):
        writer.writerow(Record)

with open(File_name,  'a', newline='') as file:
    writer = csv.writer(file)
    for i in range(3):
        writer.writerow(Record)