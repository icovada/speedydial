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
c.execute('CREATE TABLE speeddial (pkid TEXT, fkdevice TEXT, speeddialindex TEXT, speeddialnumber TEXT, label TEXT, labelascii TEXT, fkpersonalphonebook TEXT)')
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

c.execute("select device.name, device.pkid from device inner join speeddial on device.pkid=speeddial.fkdevice group by speeddial.fkdevice") #Get devices with speeddials

devicelist = c.fetchall()

for i in devicelist:
  c.execute("select speeddialindex, speeddialnumber, label, labelascii from speeddial WHERE fkdevice = (?)",(i[1],))
  print(i)
  out = "out/"+i[0]+".csv"
  csvfile = open(out, "w")
  spamwriter = csv.writer(csvfile)
  for j in c.fetchall():
    print(j)
    spamwriter.writerow(j)
  csvfile.close()
