# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 15:48:25 2020

@author: 21318
"""
import csv

def belong_to():
    majors=[]
    f = open('major.csv','r',encoding='UTF-8')
    reader = csv.reader(f)
    for i in reader:
        majors.append(i)
    f.close()
    w = open('belong_to.csv','a',encoding='UTF-8')
    writer = csv.writer(f)
    writer.writerow([':START_ID','belong to',':END_ID',':TYPE'])
    for i in majors:
        row = []
        row.append(i[0])
        row.append('belong to')
        row.append(i[8])
        row.append('BELONG TO')
        writer.writerow(row)
    w.close()
def has():
    majors=[]
    f = open('major.csv','r',encoding='UTF-8')
    reader = csv.reader(f)
    for i in reader:
        majors.append(i)
    f.close()
    w = open('has.csv','a',encoding='UTF-8')
    writer = csv.writer(f)
    writer.writerow([':START_ID','has',':END_ID',':TYPE'])
    for i in majors:
        row = []
        row.append(i[0])
        row.append('has')
        row.append(i[1])
        row.append('HAS')
        writer.writerow(row)
    w.close()
def located_in():
    colleges=[]
    f = open('college_improved.csv','r',encoding='UTF-8')
    reader = csv.reader(f)
    for i in reader:
        colleges.append(i)
    f.close()
    w = open('located_in.csv','a',encoding='UTF-8')
    writer = csv.writer(f)
    writer.writerow([':START_ID','located_in',':END_ID',':TYPE'])
    for i in colleges:
        row = []
        row.append(i[0])
        row.append('located in')
        row.append(i[1])
        row.append('LOCATED IN')
        writer.writerow(row)
    w.close()

if __name__ == '__main__':
    belong_to()
    has()
    located_in()