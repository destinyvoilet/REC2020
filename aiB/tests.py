import csv
import os
import matplotlib.pyplot as plt
import re
import random
import numpy as np
import sqlite3 as db
from models import Clustering,get_dataset,criterion
from django.test import TestCase

dataset = get_dataset()
testdata=[]
for item in dataset:
    if(item[0]==(4,2018,2)):
        for items in item:
            testdata.append(items)
testdata.remove((4,2018,2))

#获取最佳聚类数
maxk = 9 #所测试的最大聚类数
WSSarray = []  # 对聚类数为1,2,...maxk，分别存储其误差值，WSSarray的长度为maxk
for i in range(1,maxk+1):
    cluster, belong = Clustering(testdata, i)
    WSS = criterion(testdata,cluster,belong)
    WSSarray.append(WSS)
# print("不同聚类数对应的误差值所组成的数组为:",WSS)  # 输出误差数组

WSSDelta = list(np.ones(maxk))  # 获得误差数组的增量差，选择增量差最大的点对应的聚类数作为合适的聚类数
WSSDelta[0] = 0
maxDelta = -1
indexDelta = 0
for i in range(1,maxk):
    WSSDelta[i] = WSSarray[i-1] - WSSarray[i]
    if WSSDelta[i]>maxDelta:
        maxDelta = WSSDelta[i]
        indexDelta = i+1  # 较好的聚类数
# print("最大的误差差值为:",maxDelta)  # 输出最大误差
# print("误差差值对应的数组为:",SSEDelta)  # 输出误差差值
#print(WSSDelta)
#print("最佳聚类数为:",indexDelta)#输出最佳聚类数

x = list(range(1,maxk+1))
plt.figure()
plt.plot(x, WSSarray)
plt.show()


###此处选取最佳聚类数有两点需要改进或者思考：（1）距离度量的范数（2）拐点的确定
#根据差值，最大拐点往往是k=2，但是从图示可以看出，k=5也可以作为一个较好的拐点进行聚类


x = [d[0] for d in testdata]
y = [d[1] for d in testdata]

###
print('分数列表：',x)

belong1 = Clustering(testdata,2)
print(belong1)

belong2 = Clustering(testdata,5)
print(belong2)


colorlist=[]
for items in belong2[1]:
    if(items==0):
        colorlist.append('grey')
    if(items==1):
        colorlist.append('gold')
    if(items==2):
        colorlist.append('turquoise')
    if(items==3):
        colorlist.append('plum')
    if(items==4):
        colorlist.append('lawngreen')

plt.figure()
plt.xlabel('分数')
plt.ylabel('人数')
plt.bar(x, y, color=colorlist, alpha=0.8)
plt.show()

#最后print出聚类边界和每一个分数的标签，并画出一个分段聚类彩色图(以k=5为例)
#2020.9.18