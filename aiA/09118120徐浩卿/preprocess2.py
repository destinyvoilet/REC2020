import torch
import pandas as pd
import numpy as np
import heapq
import os
from models import Model1, Model2, UniversityDataset

data_humanities = pd.read_csv('./aiA/09118120徐浩卿/raw_humanities.csv')
data_science = pd.read_csv('./aiA/09118120徐浩卿/raw_science.csv')
data_all = pd.read_csv('./aiA/09118120徐浩卿/raw_all.csv')
data_university = pd.read_csv('./aiA/09118120徐浩卿/colle_shrink.csv')

model1_human = Model1().double()
model1_human.load_state_dict(torch.load('./aiA/09118120徐浩卿/humanities.mod1'))
model1_human.eval()
ideal_colle = model1_human(torch.tensor(data_humanities[['stu_rank','stu_long','stu_lati']].values))

model2_data_humanities = pd.DataFrame(columns=['uni_rank','long_diff','lati_diff','label'])

for i in range(len(data_humanities)):
    student = data_humanities.iloc[i]
    colle = ideal_colle.iloc[i]

    distances = []  # 用于存储每所可选大学与预测大学的距离
    better_schools = []
    for school in data_university:
        distances.append(torch.dist(torch.tensor(school[['uni_rank','uni_long','uni_lati']]), colle))

    better_schools_index = list(map(distances.index, heapq.nsmallest(10, distances)))  # 选取可选大学中，与预测大学距离最近的10个大学索引
    best_school_index = map(distances.index, heapq.nsmallest(1, distances))
    better_schools_index.pop(better_schools_index.index(best_school_index)) #去除最接近的大学
    for better_school_index in better_schools_index:
        better_schools.append(data_university.iloc[better_school_index])
    best_school = data_university.iloc[best_school_index]

    for better_school in better_schools:
        model2_data_humanities.append(better_school['uni_rank'].append(student[['stu_long','stu_lati']]-better_school[['uni_long','uni_lati']]).append(pd.Series([1])))

    model2_data_humanities.append(best_school['uni_rank'].append(student[['stu_long','stu_lati']]-best_school[['uni_long','uni_lati']]).append(pd.Series([0])))