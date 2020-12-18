import sqlite3 as db
import pandas as pd

def readFronSqllite(db_path,exectCmd):
    conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
    cursor=conn.cursor()        # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
    conn.row_factory=db.Row     # 可访问列信息
    cursor.execute(exectCmd)    #该例程执行一个 SQL 语句
    rows=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
    return rows
    #print(rows[0][2]) # 选择某一列数据

rows = readFronSqllite('./db.sqlite3', 'select provinceID_id,collegeID_id,categoryID_id,year,majorName,minScore  from Majors')
dataset2 = []
for row in rows:
    dataset2.append(list(row))
#print(dataset2)
name=['省','大学','文理','年','专业','分']

LIST=pd.DataFrame(columns=name,data=dataset2)
LIST.to_csv('majorScore')
#省份编号，大学编号，科目，年份，专业名称，分数