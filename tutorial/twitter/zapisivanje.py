import csv
data = [
    {'a':1,'b':2,'c':3},
    {'a':4,'b':5,'c':6},
    {'a':7,'b':8,'c':9},
]

keys = data[0].keys()
with open('test.csv','w') as output_file:
    dict_writer = csv.DictWriter(output_file,keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)

with open('latest.csv','r') as file:
    reader = csv.DictReader(file, delimiter=',')
    lista=[]
    for row in reader:
        lista.append(row)


for i in lista:
    print(i)