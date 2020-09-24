# -*- coding: utf-8 -*-


import csv
import os
import matplotlib.pyplot as plt
import re
import random
import numpy as np
import sqlite3 as db
from django.db import models


######part1 从数据库中读取数据


def readFronSqllite(db_path,exectCmd):
    conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
    cursor=conn.cursor()        # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
    conn.row_factory=db.Row     # 可访问列信息
    cursor.execute(exectCmd)    #该例程执行一个 SQL 语句
    rows=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
    return rows

def readfromAppaFrame(ARPAFrame):
    subARPA=ARPAFrame.split(',')
    return subARPA

def get_dataset(path='./db.sqlite3'):
    dataset = []
    for provinceID in [i + 1 for i in range(34)]:
        for year in [i + 2017 for i in range(3)]:
            for categoryID in range(1,4):
                sql = 'select score,rank from Rankings where provinceID_id=%s and year=%s and categoryID_id=%s' % (provinceID, year,categoryID)
                rows = readFronSqllite(path, sql)
                data = []
                data.append((provinceID, year,categoryID))
                for row in rows:
                    data.append(list(row))
                for i in range(len(data) - 2):
                    data[-(1 + i)][-1] = data[-(1 + i)][-1] - data[-(2 + i)][-1]
                dataset.append(data)
    return dataset


def distance(x, y): #求距离
    return abs(x-y)

def Clustering(data, k):
    #data:分数列表[[分数1， 人数1],...,[分数n， 人数n]] ， k：超参量，簇的数目
    cluster = [] #创建簇中心集合的数组
    belong = []  #记录每一个分数隶属于哪一个中心
    for _ in range(k): #按照k值在cluster中创建代表簇中心数
        cluster.append(data[random.randint(0, len(data)-1)][0])
    for _ in range(len(data)):
        belong.append(-1)  #定义初始值-1表示尚未归属
    while True:
        change = False #标志簇中心是否发生变化
        for index, d in enumerate(data):
            dis = []  #距离列表
            for c in cluster:
                dis.append( distance(d[0], c) )
            if belong[index] != dis.index(min(dis)):
                change = True
                belong[index] = dis.index(min(dis))
        if change == False:
            break
        for index, c in enumerate(cluster):
            sum = 0
            num = 0
            for i, b in enumerate(belong):
                if index == b:
                    sum = sum + (data[i][0] * data[i][1])
                    num = num + data[i][1]
            if num == 0:
                c = 0
            else:
                c = sum/num
                cluster[index] = c
    return cluster,belong

def criterion(data, cluster, belong):
    #data::分数列表[[分数1， 人数1],...,[分数n， 人数n]]
    #cluster:聚类中心数组，长度为k
    #belong:分数隶属中心列表
    k = len(cluster)  # 获取聚类数
    WSS = 0  # WSS:Within cluster sum of squares,表示各个点到cluster中心距离的绝对值,代表误差
    for i in range(0,k):
        for index, b in enumerate(belong):
            if b == i:
                WSS += distance(cluster[i], data[index][0])
    return WSS;


