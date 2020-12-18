import csv
from model import  readFronSqllite
import pandas as pd

###将学校评级的文件的学校代码转化为学校名称

names = readFronSqllite('./db.sqlite3', 'select collegeID,collegeName  from Colleges')
#print(names)

newlist=[]

with open('大学内专业评级.csv','r',encoding = 'utf-8') as f:
    reader=csv.reader(f)
    for row in reader:
        print(row)
        for items in names:
            if(int(row[1])==items[0]):
                newlist.append([items[1],row[2],row[3]])

#print(newlist)
pingji=pd.DataFrame(data=newlist)
pingji.to_csv('./大学内专业评级(正式).csv',encoding='utf-8')