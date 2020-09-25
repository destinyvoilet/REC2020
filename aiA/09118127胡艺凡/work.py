import json
import csv
# import pandas as pd

provinces = {
  '吉林': [125.326800, 43.896160], '黑龙江': [126.662850, 45.742080],
  '辽宁': [123.429250, 41.835710], '内蒙古': [111.765220, 40.817330],
  '新疆': [87.627100, 43.793430], '青海': [101.780110, 36.620870],
  '北京': [116.407170, 39.904690], '天津': [117.199370, 39.085100],
  '上海': [121.473700, 31.230370], '重庆': [106.550730, 29.564710],
  '河北': [114.469790, 38.035990], '河南': [113.753220, 34.765710],
  '陕西': [108.954240, 34.264860], '江苏': [118.762950, 32.060710],
  '山东': [117.020760, 36.668260], '山西': [112.562720, 37.873430],
  '甘肃': [103.826340, 36.059420], '宁夏': [106.258670, 38.471170],
  '四川': [104.075720, 30.650890], '西藏': [91.117480, 29.647250],
  '安徽': [117.285650, 31.861570], '浙江': [120.153600, 30.265550],
  '湖北': [114.342340, 30.545390], '湖南': [112.983400, 28.112660],
  '福建': [119.296590, 26.099820], '江西': [115.910040, 28.674170],
  '贵州': [106.707220, 26.598200], '云南': [102.709730, 25.045300],
  '广东': [113.266270, 23.131710], '广西': [108.327540, 22.815210],
  '香港': [114.165460, 22.275340], '澳门': [113.549130, 22.198750],
  '海南': [110.348630, 20.019970], '台湾': [121.520076, 25.030724],
}
list_1=[]
list_2=[]
for i in provinces:
    list_1.append(int(provinces[i][0]))
    list_2.append(int(provinces[i][1]))

max_1=max(list_1)
min_1=min(list_1)
max_2=max(list_2)
min_2=min(list_2)

for i in provinces:
    provinces[i][0]=(int(provinces[i][0])-min_1)/(max_1-min_1)
    provinces[i][1] = (int(provinces[i][1]) - min_2) / (max_2 - min_2)

print(provinces)

# head=['大学','经度','纬度','排名']
# d3=356
# d3min=1
# d2=22.934949800000002
# d2min=22.8065434
# d1=39.0372239
# d1min=87.6061172
# data = []
# with open('college_code(1).json', 'r', encoding='utf8') as f:
#     datas = json.load(f)
#     with open('colle_shrink.csv','w',newline='') as p:
#         writer=csv.writer(p)
#         writer.writerow(head)
#         for i in datas:
#             D1=(float(i['college_code'][0])-d1min)/d1
#             D2 = (float(i['college_code'][1]) - d2min) / d2
#             D3 = (float(i['college_code'][2]) - d3min) / d3
#             DataRow=[i['college_name']]+[D1]+[D2]+[D3]
#             print(DataRow[0])
#             data.append(DataRow)
#         writer.writerows(data)




#     # df = pd.read_json(datas)
#     # df.to_csv('result.csv')
# print(datas)
# print(data[0][3])
# col_list = []
# for i in range(len(data)):
#     col_list+=[data[i][2]]
# print(col_list)
# for i in range(len(col_list)):
#     col_list[i]=float(col_list[i])
# # col_rank=col_list.sort()
# # print(col_list[0])
# # print(col_list[len(col_list)-1])
# max=max(col_list)
# min=min(col_list)
# d=max-min
# print(d)
# print(min)
# #####################################缩放完毕####################################、
# collea=[]
# with open('college_code(1).json', 'r', encoding='utf8') as f:
#     datas = json.load(f)
#     for i in datas:
#         collea.append(i['college_name'])
# print(collea)
line=0
with open ("colle_shrink.csv",'r',encoding='gbk') as f:
    collegue_List=csv.reader(f)
    print(collegue_List)
    sheet={}
    for rows in collegue_List:
        if line!=0:
            collegue_name = ""
            collegue_number = ""
            print(rows)
            sheet[rows[0]]=[[float(rows[1]),float(rows[2])],float(rows[3])]
            print(sheet[rows[0]])
        line+=1



        # for col in range(collegue_List):
        #     if row > 1 and col == 0:
        #         data = collegue_List.cell_value(row, col)
        #         patient_name = data
        #         print(patient_name)
        #
        #     if row > 1 and col == 1:
        #         data = collegue_List.cell_value(row, col)
        #         patient_number = data
        #         print(patient_number)
        #         sheet[patient_name] = patient_number
        #         break



Province = ['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江',
    '安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川',
    '贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','香港','澳门','台湾']
category = ["文科","理科", "all"]
print(sheet)
NameList=['09118209祁丁然.csv','09118206陶特.csv','09118205王昕彤.csv','09118145邵彤.csv','09118122邵一展.csv',
'09118101高捷.csv','清北.csv']

# with open('out.csv', 'a', newline='', encoding="utf-8-sig") as q:
#     writer = csv.writer(q)
#     row=['rank','province','category','college']
#     writer.writerow(row)
#
# for names in NameList:
#     print(names)
#     c=0
#     with open(names, 'r', encoding='UTF-8') as f:
#         reader=csv.reader(f)
#         print(reader)
#         with open('out.csv','a',newline='',encoding="utf-8-sig") as q:
#             writer=csv.writer(q)
#             for row in reader:
#                 if c!=0:
#                     writer.writerow(row)
#                 c+=1
        # for row in reader:
        #     print(row)
        # print(names)
        #     for i in Province:
        #         for p in category:
#


with open('result_1.csv','a',encoding='utf8') as o:
    tittle=['rank','province','cate','coll_rank','locate']
    writer=csv.writer(o)
    for P in Province:

        for c in category:
            Rank = []
            with open('out.csv',encoding='utf-8') as p :
                reader=csv.reader(p)
                for row in reader:
                    if row[2]==c and row[1]==P:
                        Rank+=[int(row[0])]
            if Rank:
                with open('out.csv', encoding='utf-8') as p:
                    reader = csv.reader(p)
                    for row in reader:
                        if row[2]==c and row[1]==P:
                            print(min(Rank),max(Rank),P,c)
                            print(row[3])
                            rank=(int(row[0])-min(Rank))/(max(Rank)-min(Rank))
                            location=provinces[row[1]]
                            print(location)
                            Out_Put=[rank,location,c,sheet[row[3]][1],sheet[row[3]][0]]
                            writer.writerow(Out_Put)
#             # print(MAX)

#     # csv_data=pd.DataFrame(reader)
#     # for p in Province:
#     #     for c in category:
#     #         temp_data = csv_data.loc[((csv_data["province"] == p)&(csv_data["category"] == c),["rank"])]

