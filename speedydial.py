#!/usr/bin/python3
from bs4 import BeautifulSoup
import itertools
import csv
import sqlite3

def parsexml():
  print(response.readline()) #Throw away first line
  t = BeautifulSoup(response.readline())
  a=[]
  for i in t.row.parent.children:
    b = []
    for j in i.children:
      b.append(j.text)
    a.append(b)
  return(a)

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE enduser (pkid TEXT, firstname TEXT, lastname TEXT, userid TEXT)')
c.execute('CREATE TABLE personalphonebook (pkid TEXT, fkenduser TEXT, fkpersonaladdressbook TEXT, tkpersonalphonenumber TEXT, phonenumber TEXT, personalfastdialindex TEXT)')
c.execute('CREATE TABLE personaladdressbook (pkid TEXT, fkenduser TEXT, firstname TEXT, lastname TEXT, email TEXT, nickname TEXT, fkenduser_contact TEXT)')
c.execute('CREATE TABLE speeddial (pkid TEXT, device TEXT, speeddialindex TEXT, speeddialnumber TEXT, label TEXT, labelascii TEXT, fkpersonalphonebook TEXT)')
c.execute('CREATE TABLE device (pkid TEXT, name TEXT, description TEXT)')

conn.commit()

response = open("getspeeddial.response","r")
#####enduser
for i in parsexml():
  c.execute('INSERT INTO enduser values (?,?,?,?)',i)

#####personalphonebook
for i in parsexml():
  c.execute('INSERT INTO personalphonebook values (?,?,?,?,?,?)',i)

#####personaladdressbook
for i in parsexml():
  c.execute('INSERT INTO personaladdressbook values (?,?,?,?,?,?,?)',i)

#####speeddial
for i in parsexml():
  c.execute('INSERT INTO speeddial values (?,?,?,?,?,?,?)',i)

#####device
for i in parsexml():
  c.execute('INSERT INTO device values (?,?,?)',i)

conn.commit()

c.execute("select device.name from device inner join ")


######  old code, to delete after beign rewritten in sql
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
