#!/usr/bin/python3
from bs4 import BeautifulSoup
import itertools
import csv

response = open("getspeeddial.response","r")

print(response.readline()) #Throw away first line
t = BeautifulSoup(response.readline())

a=[]

for i in t.row.parent.children:
	b = []
	for j in i.children:
		b.append(j.text)
	a.append(b)

groups = []
devicename = []
data = sorted(a, key=lambda x : x[0])
for k, g in itertools.groupby(data, lambda x : x[0]):
    groups.append(list(g))      # Store group iterator as a list
    devicename.append(k)

for i in devicename:
    for j in range(0, len(data)):
       try:
           null=data[j].index(i)
       except ValueError:
           pass

count = 0
for i in devicename:
  print(i)
  out = "out/"+i
  csvfile = open(out+".csv", "w")
  spamwriter = csv.writer(csvfile)
  for j in groups[count]:
    print(j[1:])
    spamwriter.writerow(j[2:])  #Throw away device name and description, we do not need them here
  csvfile.close()
  count= count+1
