#!/usr/bin/python3
from bs4 import BeautifulSoup
import itertools
import csv

response = open("getspeeddial.response","r")

print(response.readline())
t = BeautifulSoup(response.readline())

a=[]

for i in t.row.parent.children:
	b = []
	for j in i.children:
		b.append(j.text)
	a.append(b)

groups = []
uniquekeys = []
data = sorted(a, key=lambda x : x[1])
for k, g in itertools.groupby(data, lambda x : x[1]):
    groups.append(list(g))      # Store group iterator as a list
    uniquekeys.append(k)

for i in uniquekeys:
    for j in range(0, len(data)):
       try:
           null=data[j].index(i)
       except ValueError:
           pass

count = 0
for i in uniquekeys:
  print(i)
  out = "out/"+i
  csvfile = open(out, "w")
  spamwriter = csv.writer(csvfile)
  for j in groups[count]:
    print(j)
    spamwriter.writerow(j)
  csvfile.close()
  count= count+1
