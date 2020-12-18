#!/usr/bin/env Python
# coding=utf-8
import numpy as np   
import pandas as pd
import random
import os
import csv
import json



#Year = [2017,2018,2019]

category = ["文科","理科", "all"]

result = open("清北.csv","w",encoding="utf-8-sig",newline='')
writer=csv.writer(result)
writer.writerow(["rank","province","category","college"])

csv_data = pd.read_csv('清北人数.csv',delimiter="\t")  # 读取数据
print(csv_data)

Pro = ['湖南','广东','广西','海南','重庆','四川',
    '贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆',
    '北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江',
    '安徽','福建','江西','山东','河南','湖北']
TW = [20,5,9,9,5,10,5,10,3,25,20,10,5,30,31,11,12,5,3,20,20,32,35,16,20,30,30,
      20,5,125,20]
TL = [172,84,45,17,39,168,54,28,8,100,43,25,20,83,152,53,132,176,42,82,50,57,73,
      130,80,84,60,85,  34,88,99]
PW = [70,30,18,8,5,60,27,30,6,56,37,15,20,20,42,21,54,28,10,70,32,39,45,60,90
      ,50,40,40,24,164,68]
PL = [71,100,55,20,33,100,54,31,8,55,37,14,20,30,263,58,90,141,42,72,34,40,56
      ,93,120,60,45,43,84,95,79]


l=len(TW)
print(len(Pro),len(TW),len(TL),len(PW),len(TL))
zj_t,sh_t=0,0
zj_p,sh_p=0,0

for i in range(l):
    c = "文科"
    u = "清华大学"
    if Pro[i] == '浙江' :
        zj_t+=TW[i]
    elif Pro[i] == '上海':
        sh_t+=TW[i]
    else:
        for _ in range(TW[i]):
            random_rank = random.randint(1, TW[i])
            #random_rank= TW[i] - random_score % TW[i] +1
            writer.writerow([random_rank, Pro[i], c, u])
        
for i in range(l):
    c = "文科"
    u = "北京大学"
    if Pro[i] == '浙江' :
        zj_p+=PW[i]
    elif Pro[i] == '上海':
        sh_p+=PW[i]
    else:
        for _ in range(PW[i]):
            random_rank = random.randint(1, PW[i])
            #random_rank= PW[i] - random_score % PW[i] +1
            writer.writerow([random_rank, Pro[i], c, u])
        
        
for i in range(l):
    c = "理科"
    u = "清华大学"
    if Pro[i] == '浙江' :
        zj_t+=TL[i]
    elif Pro[i] == '上海':
        sh_t+=TL[i]
    else:
        for _ in range(TL[i]):
            random_rank = random.randint(1, TL[i])
            #random_rank= TL[i] - random_score % TL[i] +1
            writer.writerow([random_rank, Pro[i], c, u])
        
        
        
for i in range(l):
    c = "理科"
    u = "北京大学"
    if Pro[i] == '浙江' :
        zj_p+=PL[i]
    elif Pro[i] == '上海':
        sh_p+=PL[i]
    else:
        for _ in range(PL[i]):
            random_rank = random.randint(1, PL[i])
            #random_rank= PL[i] - random_score % PL[i] +1
            writer.writerow([random_rank, Pro[i], c, u])      
        

sh = 209
zj = 310

for _ in range(sh_p):
    num = sh_p
    c = "all"
    u = "北京大学"
    random_rank = random.randint(1, num)
    #random_rank= PL[i] - random_score % PL[i] +1
    writer.writerow([random_rank, '上海', c, u])
        
for _ in range(sh_t):
    num = sh_t
    c = "all"
    u = "清华大学"
    random_rank = random.randint(1, num)
    #random_rank= PL[i] - random_score % PL[i] +1
    writer.writerow([random_rank, '上海', c, u])
    
for _ in range(zj_p):
    num = zj_p
    c = "all"
    u = "北京大学"
    random_rank = random.randint(1, num)
    #random_rank= PL[i] - random_score % PL[i] +1
    writer.writerow([random_rank, '浙江', c, u])
    
for _ in range(zj_p):
    num = zj_t
    c = "all"
    u = "清华大学"
    random_rank = random.randint(1, num)
    #random_rank= PL[i] - random_score % PL[i] +1
    writer.writerow([random_rank, '浙江', c, u])