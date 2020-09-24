import csv
import os
import matplotlib.pyplot as plt
import re
import random
import numpy as np
import sqlite3 as db
from model import Clustering,get_dataset,criterion,readFronSqllite

def get_dic(path='./db.sqlite3'):
    sql = 'select * from Provinces'
    rows = readFronSqllite(path, sql)
    Dic = {}
    for row in rows:
        Dic[row[0]]=row[1]
    return Dic

def get_college_name(path='./db.sqlite3'):
    sql = 'select collegeID,collegeName from Colleges'
    rows = readFronSqllite(path, sql)
    Dic = {}
    for row in rows:
        Dic[row[0]]=row[1]
    return Dic

def clusterFromData(dataset):
    clusterList = []
    for data in dataset:
        if len(data)>5:  # 剔除不合规则的数据
            pointdata = data[1:]
            clusterCenter,belong = Clustering(pointdata, 5)
            clusterCenter.sort()
            clusterCenter.append(data[0])  # 加入标签
            for i in range(5,0,-1):
                clusterCenter[i] = clusterCenter[i-1]
            clusterCenter[0] = data[0]
            clusterList.append(clusterCenter)
    return clusterList



rows = readFronSqllite('./db.sqlite3', 'select provinceID_id,categoryID_id,collegeID_id,avg(minScore) from Majors group by provinceID_id,collegeID_id,categoryID_id')
College_dataset = []
for row in rows:
    College_dataset.append(list(row))
Dic = get_college_name(path='./db.sqlite3')
for d in College_dataset:
    d[2] = Dic.get(d[2])

Score_dataset = get_dataset()

rows = readFronSqllite('./db.sqlite3', 'select provinceID_id,collegeID_id,categoryID_id,year,majorName,minScore  from Majors')
Major_dataset = []
for row in rows:
    Major_dataset.append(list(row))

#for item in Score_dataset:
    #print(item)
#print(Score_dataset)#分段聚类输入数据（功能1）
#print(College_dataset)#大学推荐输入数据（功能1延展）
#print(Major_dataset)#学校专业评级输入数据（功能2）

#Score_dataset形式：[  [ (provinceID,year，categoryID),[分数，人数], [分数，人数]...,[分数，人数] ] , [], []   ]
#College_dataset:[[1, 1, '北京大学', 653.6666666666666],
'''
 [1, 2, '北京大学', 681.0],
 [1, 1, '中国人民大学', 635.0704225352113],
 [1, 2, '中国人民大学', 654.8169014084507],
 [1, 1, '清华大学', 654.6666666666666],
 [1, 2, '清华大学', 675.8333333333334],
 [1, 1, '北京交通大学', 616.0],
 [1, 2, '北京交通大学', 616.25],
 [1, 1, '北京航空航天大学', 629.5],
'''
#Major_dataset:省份编号，大学编号，科目，年份，专业名称，分数

center = clusterFromData(Score_dataset)
cen=[]
newcen=[]
for i in range(len(center)):
    cen.append([])
    for j in range(1,6):
        cen[i].append(center[i][j])
for i in range(len(center)):
    cen[i].sort(reverse=True)

newcen1=[]
s=0
for j in range(1,35):
    for m in range(1,3):

        sum1=[]
        sum2=[]
        sum3=[]
        sum4=[]
        sum0=[]
        for i in range(len(center)):
            if int(list(center[i][0])[0])==j and int(list(center[i][0])[2])==m:
                sum0.append(cen[i][0])
                sum1.append(cen[i][1])
                sum2.append(cen[i][2])
                sum3.append(cen[i][3])
                sum4.append(cen[i][4])
        if(sum0!=[]):
            newcen1.append([])
            newcen1[s].append(j)
            newcen1[s].append(m)
            newcen1[s].append(sum(sum0)/len(sum0))
            newcen1[s].append(sum(sum1)/len(sum1))
            newcen1[s].append(sum(sum2)/len(sum2))
            newcen1[s].append(sum(sum3)/len(sum3))
            newcen1[s].append(sum(sum4)/len(sum4))
            s=s+1

rows = readFronSqllite('./db.sqlite3', 'select provinceID_id,categoryID_id,collegeID_id,avg(minScore) from Majors group by provinceID_id,collegeID_id,categoryID_id')
datasetCOLLEGE = []
for row in rows:
    datasetCOLLEGE.append(list(row))
Dic = get_college_name(path='./db.sqlite3')
for d in datasetCOLLEGE:
    d[2] = Dic.get(d[2])


'''
center:
[[(1, 2017, 1), 531.0, 559.5, 587.475, 606.085, 630.483],
 [(1, 2017, 2), 494.659, 519.076, 546.571, 579.28, 622.482],
 [(1, 2018, 1), 554.018, 570.369, 588.07, 608.215, 633.879],
 [(1, 2018, 2), 476.807, 506.469, 539.436, 613.66, 649.874],
 [(2, 2017, 1), 356.69, 412.626, 467.281, 522.585, 585.314],
 [(2, 2017, 2), 399.2, 457.135, 511.088, 567.299, 629.507],
'''
from django.http import HttpResponse
from django.shortcuts import render
app_name = 'aiB'
# Create your views here.
def helloworld(request):
    return HttpResponse('Hello World! by aiB group')