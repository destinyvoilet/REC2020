# -*- coding: utf-8 -*-
"""

@author: Jessica
"""

import csv

def entity_formatting(in_file,out_file,title,label):
    '''
    in_file 输入文件，out_file 输出文件，
    title 表头，label 标签
    '''
    in_f = open(in_file,'r')
    out_f = open(out_file,'w',newline='',encoding='utf-8')
    data = csv.reader(in_f)
    writer = csv.writer(out_f)  # 写入表头
    writer.writerow(title)
    for i,row in enumerate(data):
        if i>0:
            row.append(label)  # 增加label
            writer.writerow(row)
    in_f.close()
    out_f.close()
    
    
def relation_formatting(in_file,out_file,title):
    in_f = open(in_file,'r',encoding='utf-8')
    out_f = open(out_file,'w',newline='',encoding='utf-8')
    data = csv.reader(in_f)
    writer = csv.writer(out_f)
    writer.writerow(title)
    for i,row in enumerate(data):
        if i>0:
            del row[1]   # 删去多余的一列
            writer.writerow(row)        
    in_f.close()
    out_f.close()
        
   

# entity-college    
entity_formatting('E:\\preprocess\\entity\\college.csv',
          'E:\\import\\college.csv',
          ['CollegeID:ID','CollegeName','985:int','211:int','Top:int',':LABEL'],
          'College')  
# entity-displine
entity_formatting('E:\\preprocess\\entity\\displine.csv',
          'E:\\import\\displine.csv',
          ['DisplineID:ID','DisplineName',':LABEL'],
          'First-level discipline')
# entity-province
entity_formatting('E:\\preprocess\\entity\\province.csv',
          'E:\\import\\province.csv',
          ['ProvinceID:ID','ProvinceName',':LABEL'],
          'Province') 
# entity-year   
entity_formatting('E:\\preprocess\\entity\\year.csv',
          'E:\\import\\year.csv',
          ['YearID:ID','YearName',':LABEL'],
          'Year')
# entity-major
in_f = open('E:\\preprocess\\entity\\major.csv','r')
out_f = open('E:\\import\\major.csv','w',newline='',encoding='utf-8')
writer = csv.writer(out_f)
writer.writerow(['MajorID:ID','MajorName','Contributor',':LABEL'])
data = csv.reader(in_f)
for i,row in enumerate(data):
    if i>0:
        del row[2]
        row.append('Major')
        writer.writerow(row)
in_f.close()
out_f.close()

#entity-subject
out_f = open('E:\\import\\subject.csv','w',newline='',encoding='utf-8')
writer = csv.writer(out_f)
writer.writerows([['SubjectID:ID','SubjectName',':LABEL'],
                 ['s1','文科','Subject'],
                 ['s2','理科','Subject'],
                 ['s3','all','Subject']])
out_f.close()




    
    
    
# relation-located_in
relation_formatting('E:\\preprocess\\relation\\located_in.csv',
                    'E:\\import\\located_in.csv',
                    [':START_ID',':END_ID',':TYPE']) 
# relation-is_subject
relation_formatting('E:\\preprocess\\relation\\is_subject.csv',
                    'E:\\import\\is_subject.csv',
                    [':START_ID',':END_ID',':TYPE'])
# relation-belong_to
relation_formatting('E:\\preprocess\\relation\\belong_to.csv',
                    'E:\\import\\belong_to.csv',
                    [':START_ID',':END_ID',':TYPE'])
# relation-has
in_f = open('E:\\preprocess\\relation\\has.csv','r',encoding='utf-8')
out_f = open('E:\\import\\has.csv','w',newline='',encoding='utf-8')
data = csv.reader(in_f)
writer = csv.writer(out_f)
writer.writerow([':START_ID',':END_ID',':TYPE'])
for i,row in enumerate(data):
    if i>0:
        del row[1]
        if row[0]=='c?北京航空航天大学':
            row[0]='c10006'
        if row[0]=='c北京理科大学':
            row[0]='c10007'
        if row[0]=='c华东理科大学':
            row[0]='c10251'
        writer.writerow(row)
in_f.close()
out_f.close()

# relation-need_score
in_f = open('E:\\preprocess\\relation\\need_score.csv','r',encoding='utf-8')
out_f = open('E:\\import\\need_score.csv','w',newline='',encoding='utf-8')
data = csv.reader(in_f)
writer = csv.writer(out_f)
writer.writerow([':START_ID','Score:int',':END_ID',':TYPE'])
for i,row in enumerate(data):
    if i>0:
        writer.writerow(row)
in_f.close()
out_f.close()

# relation established_in   在major表中，将专业与省份的关系提取出来
in_f = open('E:\\preprocess\\entity\\major.csv','r')
out_f = open('E:\\import\\established_in.csv','w',newline='',encoding='utf-8')
data = csv.reader(in_f)
writer = csv.writer(out_f)
writer.writerow([':START_ID',':END_ID',':TYPE'])   
for i,row in enumerate(data):
    if i>0:
        new_row = [row[0],row[2],'ESTABLISHED_IN']
        writer.writerow(new_row)
in_f.close()
out_f.close()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    