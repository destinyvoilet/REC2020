import torch
import pandas as pd
import os

rank = int(input('请输入你的排名：'))
prov = input('请输入你的省份：')
sb_type = input('文理科（文科/理科/all）：')

data = pd.read_csv('./out.csv')
data.info()
data_prov = data[data['province'].isin([prov])]
data_cate = data_prov[data_prov['category'].isin([sb_type])]
data_cate['rank'] = data_cate['rank'].astype('int32')

available_data = data_cate.loc[data_cate['rank']>=rank]
available_college = available_data['college'].unique()
print(available_college)
