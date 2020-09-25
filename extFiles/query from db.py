import sqlite3 as db
import json


def readFronSqllite(db_path, exectCmd, args=None):
    conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
    cursor = conn.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
    conn.row_factory = db.Row  # 可访问列信息
    if not args:
        cursor.execute(exectCmd)
    else:
        cursor.execute(exectCmd, args)
    # 该例程执行一个 SQL 语句
    rows = cursor.fetchall()  # 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
    return rows
    # print(rows[0][2]) # 选择某一列数据


# 解析ARPA 单帧信息
def readfromAppaFrame(ARPAFrame):
    subARPA = ARPAFrame.split(',')
    # print(subARPA)


def query_college(Province, Year, Category, College):
    rows = readFronSqllite("db.sqlite3",
                           "select majorName,Rankings.year,minScore,rank "#可直接增加rank选项
                           "from Majors,Colleges,Category,Provinces,Rankings "
                           "where Majors.categoryID_id==Category.categoryID "
                           "and Majors.collegeID_id==Colleges.collegeID "
                           "and Rankings.year==Majors.year "
                           "and Majors.categoryID_id==Rankings.categoryID_id "
                           "and Majors.provinceID_id==Rankings.provinceID_id "
                           "and Rankings.score==Majors.minScore "
                           "and Majors.year>=?-3 "
                           "and Majors.ProvinceID_id==ProvinceID "
                           "and categoryname==? "
                           "and collegeName==? "
                           "and provinceName==?",
                           (Year, Category, College, Province)
                           )
    readLines = len(rows)
    print(f'本次查询共{readLines}条数据')
    #print(readLines)
    lineIndex = 0
    res = {}
    while lineIndex < readLines:
        row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
        #content = ','.join(str(v) for v in row)
        #res[lineIndex] = row[0]
        #res[lineIndex]
        temp1={}
        temp1[row[2]]=row[3]
        temp2={}
        temp2[row[1]]=temp1
        res[row[0]]=temp2
        lineIndex += 1


        # print(content)
    res=json.dumps(res, ensure_ascii=False)
    return res

def query_score(Year,Province,Category,Score,Wave):
    "查询某分数在某年上下波动10分的去向"
    rows = readFronSqllite("db.sqlite3",
                           "select collegeName,majorName,Rankings.year,minScore,rank "
                           "from Majors,Colleges,Category,Provinces,Rankings "
                           "where Majors.categoryID_id==Category.categoryID "
                           "and Majors.collegeID_id==Colleges.collegeID "
                           "and Majors.year==? "
                           "and Majors.ProvinceID_id==ProvinceID "
                           "and Rankings.year==Majors.year "
                           "and Majors.categoryID_id==Rankings.categoryID_id "
                            "and Rankings.score==Majors.minScore "
                           "and Majors.provinceID_id==Rankings.provinceID_id "
                           "and categoryname==? "
                           "and minScore>=?-? "
                           "and minScore<=?+? "
                           "and provinceName==?",
                           (Year, Category, Score, Wave,Score,Wave,Province)
                           )
    readLines = len(rows)
    print(f'本次查询共{readLines}条数据')
    lineIndex = 0
    res = {}
    while lineIndex < readLines:
        row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
        #content = ','.join(str(v) for v in row)
        temp1={}
        temp2={}
        temp3={}
        temp1[row[3]]=row[4]
        temp2[row[2]]=temp1
        temp3[row[1]]=temp2
        res[row[0]] = temp3
        lineIndex += 1
    res = json.dumps(res, ensure_ascii=False)

    return res

def query_rank(Year,Province,Category):
    "查询一分一段表"
    rows = readFronSqllite("db.sqlite3",
                           "select score,rank,year "
                           "from Rankings,Provinces,Category "
                           "where Rankings.categoryID_id==categoryID  "
                           "and Rankings.provinceID_id==provinceID "
                           "and Rankings.year=? "
                           "and provinceName==? "
                           "and categoryname==?",
                           (Year,Province,Category)
                           )


    readLines = len(rows)
    print(f'本次查询共{readLines}条数据')
    lineIndex = 0
    res = {}
    while lineIndex < readLines:
        row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
        #content = ','.join(str(v) for v in row)
        temp1 = {}
        temp1[row[1]] = row[2]
        res[row[0]] = temp1
        #res[lineIndex] = row
        lineIndex += 1
    res = json.dumps(res, ensure_ascii=False)

    return res


def main(College=None,Category=None,Year=None,Province=None,Score=None,Wave=10):#Wave 表示上下波动的分数范围
    if College!=None:
        if  Province!=None  and Year!=None:
            print(f"查询{College}{Year}年以往三年在{Province}地的录取结果为：")
            print('格式为:专业名称，年份，分数，对应排名的json文件')
            res=query_college(Province,Year,Category,College)
            print(res)
            print(
                "###################################################################################################################################################################")
            return res
    elif Score!=None:
        if Category != None and Province != None  and Year != None:
            print(f"查询{Category}{Score}分于{Year}年在{Province}地的录取结果(分数为{Score}上下波动{Wave}分")
            print('格式为:大学名称，专业名称，年份，分数，对应排名的json文件')
            res=query_score(Year,Province,Category,Score,Wave)
            print(res)
            print(
                "#############################################################################################################################################################################")
            return res
    elif Category!=None and Province!=None and Year!=None:
        print(f"查询{Year}年{Province}{Category}一分一段表")
        print('格式为:分数,排名,年份的json文件')
        res=query_rank(Year,Province,Category)
        print(res)
        print("##############################################################################################################################################################################")
        return res



    return


if __name__ == "__main__":
    # rows = readFronSqllite("db.sqlite3", "select CollegeName from Colleges where project985==1")
    # rows=readFronSqllite("db.sqlite3","select ")
    # readLines = len(rows)
    # lineIndex = 0
    # while lineIndex < readLines:
    #   row = rows[lineIndex]  # 获取某一行的数据,类型是tuple
    #   content = ','.join(str(v) for v in row)
    #   print(content)
    #  readfromAppaFrame(content)  # 解析ARPA数据
    #  lineIndex += 1
    # print(lineIndex)
    main(None,'理科',2018,'山西',None)
    main("山东大学","理科",2018,'山西',625,5)
    main(Category="理科",Year=2018,Province='山西',Score=625,Wave=5)

