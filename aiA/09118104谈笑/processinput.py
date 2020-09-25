import torch.nn as nn
import numpy as np
import heapq
import torch
from torch.nn import functional as F
import csv

# 省份归一化之后的经纬度
province_longitude_latitude = {'吉林': [0.9743589743589743, 0.92], '黑龙江': [1.0, 1.0],
                               '辽宁': [0.9230769230769231, 0.84], '内蒙古': [0.6153846153846154, 0.8],
                               '新疆': [0.0, 0.92], '青海': [0.358974358974359, 0.64],
                               '北京': [0.7435897435897436, 0.76], '天津': [0.7692307692307693, 0.76],
                               '上海': [0.8717948717948718, 0.44], '重庆': [0.48717948717948717, 0.36],
                               '河北': [0.6923076923076923, 0.72], '河南': [0.6666666666666666, 0.56],
                               '陕西': [0.5384615384615384, 0.56], '江苏': [0.7948717948717948, 0.48],
                               '山东': [0.7692307692307693, 0.64], '山西': [0.6410256410256411, 0.68],
                               '甘肃': [0.41025641025641024, 0.64], '宁夏': [0.48717948717948717, 0.72],
                               '四川': [0.4358974358974359, 0.4], '西藏': [0.10256410256410256, 0.36],
                               '安徽': [0.7692307692307693, 0.44], '浙江': [0.8461538461538461, 0.4],
                               '湖北': [0.6923076923076923, 0.4], '湖南': [0.6410256410256411, 0.32],
                               '福建': [0.8205128205128205, 0.24], '江西': [0.717948717948718, 0.32],
                               '贵州': [0.48717948717948717, 0.24], '云南': [0.38461538461538464, 0.2],
                               '广东': [0.6666666666666666, 0.12], '广西': [0.5384615384615384, 0.08],
                               '香港': [0.6923076923076923, 0.08], '澳门': [0.6666666666666666, 0.08],
                               '海南': [0.5897435897435898, 0.0], '台湾': [0.8717948717948718, 0.2]}

provinces = list(province_longitude_latitude.keys())

# 读取大学数据
with open('colleges.csv', encoding='gbk') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

# 修改大学数据格式
schools = rows[1:]
for college in schools:
    college[1] = float(college[1])
    college[2] = float(college[2])
    college[3] = float(college[3])

# # X 为当前学生数据 (经度，纬度，排名），为示范数据
# X_np = np.array([0.4, 0.2, 0.1])  # np.ndarray格式
# X = torch.from_numpy(X_np)  # torch.Tensor格式


stu_province = str(input("请输入你的省份信息（例如：江苏）："))

while stu_province not in provinces:
    print("你输入的省份不正确！")
    stu_province = str(input("请重新输入你的省份信息："))


stu_rank = int(input("请输入你在省内的高考排名："))

while stu_rank <= 0:
    print("你输入的排名不正确！")
    stu_rank = int(input("请重新输入你在省内的高考排名："))

if stu_province != '上海' or '浙江':
    stu_major = str(input("请输入你的选科（文科、理科）："))

    while stu_major != '文科' and stu_major != '理科':
        print("你输入的选科信息不正确！")
        stu_major = str(input("请重新输入你的选科："))
else:
    stu_major = 'all'


#  读取省排名数据
with open('province_rank_info.csv') as f2:
    reader2 = csv.reader(f2)
    rows2 = [row2 for row2 in reader2]

province_rank_info = rows2[1:]

count = 0
for ele in province_rank_info:
    count += 1
    if stu_province == ele[0] and stu_major == ele[1]:
        max_rank = int(ele[2])
        min_rank = int(ele[3])
        break


if count == len(province_rank_info):
    print("数据有误！")
    exit()

normalized_rank = (stu_rank - min_rank) / (max_rank - min_rank)
X_np = np.array([province_longitude_latitude[stu_province][0],
                 province_longitude_latitude[stu_province][1],
                  normalized_rank])

X = torch.from_numpy(X_np)