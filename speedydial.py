#!/usr/bin/python3

#Copyright (C) 2013  Federico Tabbò

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from bs4 import BeautifulSoup
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
  out = "output/speeddial/out/"+i[0]+".csv"
  csvfile = open(out, "w")
  csvwriter = csv.writer(csvfile)
  for j in c.fetchall():
    print(j)
    csvwriter.writerow(j)
  csvfile.close()

c.execute("select enduser.userid, enduser.pkid from enduser inner join personaladdressbook on personaladdressbook.fkenduser=enduser.pkid group by enduser.userid, enduser.pkid")
enduserwithcontacts = c.fetchall()

for i in enduserwithcontacts:
  c.execute("select pab.firstname, pab.lastname, pab.nickname, ppb.phonenumber, ppb.tkpersonalphonenumber, pab.email from personalphonebook as ppb inner join personaladdressbook as pab on ppb.fkpersonaladdressbook=pab.pkid WHERE pab.fkenduser = ?",(i[1],))
  out = "output/contacts/out/"+i[0]+".csv"
  csvfile = open(out, "w")
  csvwriter = csv.writer(csvfile)
  for j in c.fetchall():
    print(j)
    csvwriter.writerow(j)
  csvfile.close()







