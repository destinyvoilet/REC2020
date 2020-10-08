import pandas as pd
import numpy as np
import sqlite3 as db
import csv

conn = {}
with open('data.csv', 'r', encoding="UTF-8-sig") as f:
    reader = csv.reader(f)
    print(type(reader))
    firstline = True
    for row in reader:
        if firstline == True:
            firstline = False
            continue
        else:
            conn[row[1]] = row[4]

print(conn)

def readFronSqllite(db_path,exectCmd):
    conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
    cursor=conn.cursor()        # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
    conn.row_factory=db.Row     # 可访问列信息
    cursor.execute(exectCmd)    #该例程执行一个 SQL 语句
    rows=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
    return rows
    #print(rows[0][2]) # 选择某一列数据

# 解析ARPA 单帧信息
def readfromAppaFrame(ARPAFrame):
    subARPA=ARPAFrame.split(',')
    #print(subARPA)

rows=readFronSqllite('./db.sqlite3','select id,majorName,year,minScore,firstlevelIDs,categoryID_id,collegeID_id,provinceID_id from Majors')
data = []
readLines=163383
lineIndex=0
while lineIndex<readLines:
    row=rows[lineIndex] # 获取某一行的数据,类型是tuple
    #print(row)
    #content="".join(row).strip(',') #tuple转字符串
    data.append(list(row))
    lineIndex+=1

rows=readFronSqllite('./db.sqlite3','select firstlevelID, firstlevelName from Firstlevel')
firstlevelconn = {}
readLines=83
lineIndex=0
while lineIndex<readLines:
    row=rows[lineIndex] # 获取某一行的数据,类型是tuple
    #print(row)
    #content="".join(row).strip(',') #tuple转字符串
    firstlevelconn[row[1]] = row[0]
    lineIndex+=1

data_new = []
for line in data:
    major = line[1]
    content = []
    for word in major:
        if word == "(" or word == "（" or word == "【": break
        content.append(word.strip())
    p_major = "".join(content)

    if p_major == "all":
        firstlevel = "无"
    else:
        firstlevel = conn[p_major]
    if firstlevel == "无":
        id = "None"
    else:
        id = firstlevelconn[firstlevel]
    line[4] = id
    data_new.append(line)

name=["id","majorName","year","minScore","firstlevelIDs","categoryID_id","collegeID_id","provinceID_id"]
dataframe = pd.DataFrame(columns=name,data=data_new)
dataframe.to_csv("res.csv", encoding="utf-8-sig")

