# -*- coding: utf-8 -*-
import pandas as pd
from py2neo import Graph, Node, Relationship
import os
import json

# 读取数据
provinceinfo = pd.read_csv("省份.csv", encoding='gbk')    # 省份信息:ID，省份名称
collegeinfo = pd.read_csv("college.csv", encoding='gbk')    # 大学信息:省份ID，省份名称，大学名称，985，211，top，大学ID
scorefiles = os.listdir('json_csv')     # 一分一档表信息
scoreLine = dict()      # 省份分数线信息:一本线、二本线、专科线...

with open('各省分数线.json', encoding='utf-8')as f:
    scoreLine = json.load(f)

# 连接到Neo4j数据库
# ******改成自己的数据库信息******
graph = Graph("http://localhost:7474",
              username="neo4j",
              password="******")  #++++++++++改成自己的密码++++++++++
graph.delete_all()  # 删除原来全部的节点和关系

# 创建34个省份节点
provinceNode = []   # 存储创建好的34个省份节点，用于后续创建关系
for i in range(provinceinfo.shape[0]):
    provinceNode.append(Node('省份', ID=int(provinceinfo.iloc[i][0]), Name=str(provinceinfo.iloc[i][1])))
    graph.create(provinceNode[i])

# 创建学校节点
collegeNode = []    # 存储创建好的学校节点，用于后续创建关系
for i in range(collegeinfo.shape[0]):
    collegeNode.append(Node('学校', ID=int(collegeinfo.iloc[i][6]),
                       Name=str(collegeinfo.iloc[i][2]), _985_=int(collegeinfo.iloc[i][3]),
                       _211_=int(collegeinfo.iloc[i][4]), top=int(collegeinfo.iloc[i][5]),
                       ProvinceID=int(collegeinfo.iloc[i][0])))
    graph.create(collegeNode[i])

# 创建分数信息节点
scoreNode = []  # 存储创建好的学校节点，用于后续创建关系
for fileName in scorefiles:
    if not os.path.isdir(fileName):  # 判断是否是文件夹，不是文件夹才打开
        scoreinfo = pd.read_csv('json_csv' + '/' + fileName, encoding='utf-8')    # 加载csv文件数据

        # 属性:值
        provinceID = int(scoreinfo.iloc[0][3])
        year = int(scoreinfo.iloc[0][4])
        category = str(scoreinfo.iloc[0][5])
        scoreLineClass = []     # 分数线类别:一本线、二本线、专科线...
        scoreLineValue = []     # 分数线取值(与上面的列表对应)
        score = []              # 一分一段表的分数
        cumulateNumber = []     # score对应的累计人数

        # 省份分数线（一本线、二本线、专科线...）
        scoreLineClass = list(scoreLine[provinceinfo.iloc[provinceID-1][1]][str(year)][category].keys())
        scoreLineValue = list(scoreLine[provinceinfo.iloc[provinceID-1][1]][str(year)][category].values())

        # 分数list、累计人数list
        for i in range(scoreinfo.shape[0]):
            score.append(int(scoreinfo.iloc[i][1]))
            cumulateNumber.append((int(scoreinfo.iloc[i][2])))

        scoreNode.append(Node('分数信息', provinceID=provinceID, year=year,
                              category=category, score=score, cumulateNumber=cumulateNumber,
                              scoreLineClass=scoreLineClass, scoreLineValue=scoreLineValue))
        graph.create(scoreNode[-1])

# 创建学校和节点之间的关系
for i in range(provinceinfo.shape[0]):
    for j in range(collegeinfo.shape[0]):
        if(collegeinfo.iloc[j][0] == provinceinfo.iloc[i][0]):  # 学校属性.省份ID == 省份属性.ID
            graph.create(Relationship(provinceNode[i], 'have', collegeNode[j]))
            graph.create(Relationship(collegeNode[j], 'located', provinceNode[i]))

# 创建分数信息与省份的关系
for i in range(len(scoreNode)):
    for j in range(provinceinfo.shape[0]):
        if(scoreNode[i]['provinceID'] == provinceinfo.iloc[j][0]):
            graph.create(Relationship(scoreNode[i], 'score_province', provinceNode[j]))
            graph.create(Relationship(provinceNode[j], 'province_score', scoreNode[i]))



