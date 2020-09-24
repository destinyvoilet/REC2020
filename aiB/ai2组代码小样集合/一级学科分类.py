import sqlite3 as db
from fuzzywuzzy import fuzz
import numpy as np
import re

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

if __name__=="__main__":
    rows=readFronSqllite('./db.sqlite3','select firstlevelName from Firstlevel')
    firstlevelName = []
    readLines=83
    lineIndex=0
    while lineIndex<readLines:
        row=rows[lineIndex] # 获取某一行的数据,类型是tuple
        content="".join(row).strip(',') #tuple转字符串
        firstlevelName.append(content)
        lineIndex+=1
    firstlevelName[11] = "外国语言文学"
    firstlevelName[12] = "中国语言文学"
    firstlevelName.append("无")
    print("一级学科数：", len(firstlevelName))
    print(firstlevelName)

    p_firstlevelName = [0]*84
    for id, name in enumerate(firstlevelName):
        p_firstlevelName[id] = name.rstrip("与工程")
    for id, name in enumerate(p_firstlevelName):
        p_firstlevelName[id] = name.strip("与技术")
    for id, name in enumerate(p_firstlevelName):
        p_firstlevelName[id] = name.strip("基础科学")
    p_firstlevelName[78] = "军事后勤与军事装备"
    print("处理后学科:")
    print(p_firstlevelName)

    rows = readFronSqllite('./db.sqlite3', 'select majorName from Majors')
    majorName = set()
    readLines = 163383
    lineIndex = 0
    while lineIndex < readLines:
        row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
        content = "".join(row).strip(',')  # tuple转字符串
        res_content = []
        for word in content:
            if word =="(" or word == "（" or word == "【":break
            res_content.append(word.strip())
        content = "".join(res_content)
        if content != "all":
            majorName.add(content)
        lineIndex += 1
    print("专业数：", len(majorName))
    print(majorName)

    conn = dict()
    score = [0]*84
    for major in majorName:
        for id, firstlevel in enumerate(p_firstlevelName):
            score[id] = fuzz.ratio(major, firstlevel)
        res_id = np.argmax(score)
        if score[res_id] == 0:
            conn[major] = ("无", 0)
        else:
            conn[major] = (p_firstlevelName[res_id], score[res_id])
    print("对应结果和分数：")
    print(conn)


    import pandas as pd
    name=["专业","处理后一级学科","相似度","一级学科"]
    data = []
    for keys in conn.keys():
        data.append([keys, conn[keys][0], conn[keys][1], firstlevelName[p_firstlevelName.index(conn[keys][0])]])
    dataframe = pd.DataFrame(columns=name,data=data)
    dataframe.to_csv("data.csv", encoding="utf-8-sig")
