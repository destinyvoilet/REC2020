
import pandas as pd
df = pd.read_csv("Province.csv",encoding="gbk")
province = df['Unnamed: 1'].tolist()
code = [i for i in range(1,len(province)+1)]
code = dict(zip(province,code))
print(code)

#存放json的文件夹名称
jsonpath = './json'
#输出csv的文件夹名称
csvpath = './json_csv/'

import os
def scan_files(directory,prefix=None,postfix=None):
    files_list=[]
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root,special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root,special_file))
            else:
                files_list.append(os.path.join(root,special_file)) 
    return files_list
#读取当前目录的上级目录
temp = os.path.abspath(jsonpath)
all_files = scan_files(temp)

import json
with open(all_files[0],'r',encoding='utf8')as fp:
    json_data = json.load(fp)
print(json_data)
for a in json_data.items():
    for b in a[1].items():
        for c in b[1].items():
            print(c[1])
values = [i for i in c[1].values()]
keys = [i for i in c[1].keys()]
print(values)
print(keys)

pro_num = 0
for file in all_files:
    file_name = file.split('\\')[-1].split('.')[0]
    year = file_name[0:4]
    for pro in province:
        if pro in file:
            pro_num = code[pro]
            break
    if "理科" in file:
        subject = "理科"
    elif "文科" in file:
        subject = "文科"
    else:
        subject = "综合"
    try:
        try:
            with open(file,'r',encoding='gbk')as fp:
                json_data = json.load(fp)
        except:
            with open(file,'r',encoding='utf-8-sig')as fp:
                json_data = json.load(fp)
    except:
        print(file_name,"failed!")
        continue
    for a in json_data.items():
        for b in a[1].items():
            for c in b[1].items():
                print(file," open successfully!"," ",subject)
    values = [i for i in c[1].values()]
    keys = [i for i in c[1].keys()]
    df = pd.DataFrame([keys,values,[pro_num] * len(keys),[year] * len(keys),[subject] * len(keys)])
    df = df.T
    df.set_axis(['分数', '累计人数', '省份','年份','科类'], axis='columns')
    
    new_path = csvpath + file_name + '.csv'
    df.to_csv(new_path,encoding='utf-8-sig')

