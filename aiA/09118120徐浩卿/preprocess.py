import torch
import pandas as pd
import os

main_dataframe = pd.read_csv('./aiA/09118120徐浩卿/result_1.csv')
data_humanities = main_dataframe[main_dataframe['sbj_type'].isin(['文科'])].drop(columns=['sbj_type'])
data_science = main_dataframe[main_dataframe['sbj_type'].isin(['理科'])].drop(columns=['sbj_type'])
data_all = main_dataframe[main_dataframe['sbj_type'].isin(['all'])].drop(columns=['sbj_type'])

data_humanities.to_csv('./aiA/09118120徐浩卿/raw_humanities.csv')
data_science.to_csv('./aiA/09118120徐浩卿/raw_science.csv')
data_all.to_csv('./aiA/09118120徐浩卿/raw_all.csv')