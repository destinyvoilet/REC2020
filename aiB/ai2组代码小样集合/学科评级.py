# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:53:33 2020

@author: yjw
"""
#对于学校的评级，对于每一年而言，1-3为A，4-7为B，8-12为C，12以后都为D
schid=[]#学校的id
major=[]#专业的名称
score=[]#专业的最低分数
year=[]#年份
province=[]
id_2017_m_score=[]
id_2018_m_score=[]
id_2019_m_score=[]
import csv
with open('majorScore.csv','r') as f:
    reader=csv.reader(f)
    for row in reader:
        schid.append(row[2])
        major.append(row[5])
        score.append(row[6])
        year.append(row[4])
        province.append(row[1])
for i in range(10002,10731):
    for j in range(len(schid)):
        if major[j]=='all' or major[j]=='All':
                continue
        if province[j]=='10':
            if schid[j]=='%d'%i and year[j]=='2017':
                m=[schid[j],year[j],major[j],score[j]]
                id_2017_m_score.append(m)
            if schid[j]=='%d'%i and year[j]=='2018':
                n=[schid[j],year[j],major[j],score[j]]
                id_2018_m_score.append(n)
            if schid[j]=='%d'%i and year[j]=='2019':
                k=[schid[j],year[j],major[j],score[j]]
                id_2019_m_score.append(k)
class level:
    def __init__(self,schid,year,major,score):
      self.schid = schid
      self.year = year
      self.major = major
      self.score=score
    def print(self):
        print(self.schid,self.major,self.score)
ob_2017=[]
ob_2018=[]
ob_2019=[]
for i in id_2017_m_score:
    ob_2017.append(level(i[0],i[1],i[2],i[3]))
for i in id_2018_m_score:
    ob_2018.append(level(i[0],i[1],i[2],i[3]))
for i in id_2019_m_score:
    ob_2019.append(level(i[0],i[1],i[2],i[3]))
try:
  import operator
except ImportError:
    cmpfun= lambda x: x.count # use a lambda if no operator module
else:
  cmpfun= operator.attrgetter('score') # use operator since it's faster than lambda
ob_2017.sort(key=cmpfun, reverse=True)
ob_2018.sort(key=cmpfun, reverse=True)
ob_2019.sort(key=cmpfun, reverse=True)
fin_2017=[]
fin_2018=[]
fin_2019=[]
for i in range(10002,10731):
    avr_2017=[]
    for j in ob_2017:
        if j.schid=='%d'%i:
            m=[j.schid,j.major,j.score]
            avr_2017.append(m)
    fin_2017.append(avr_2017)
for i in range(10002,10731):
    avr_2018=[]
    for j in ob_2018:
        if j.schid=='%d'%i:
            m=[j.schid,j.major,j.score]
            avr_2018.append(m)
    fin_2018.append(avr_2018)
for i in range(10002,10731):
    avr_2019=[]
    for j in ob_2019:
            if j.schid=='%d'%i:
                m=[j.schid,j.major,j.score]
                avr_2019.append(m)
    fin_2019.append(avr_2019)
ans=[]
for i in range(729):
    for j in range(len(fin_2017[i])):
        q=fin_2017[i][j][1]
        if q in fin_2018[i]:
            m=fin_2018[i].index(q)+1
        else:
            m=1
        if q in fin_2019[i]:
            n=fin_2019[i].index(q)+1
        else:
            n=1
        a=(m+n+j)/3+1
        if a in range(1,4):
            ans.append([fin_2017[i][j][0],q,'A'])
        if a in range(4,8):
            ans.append([fin_2017[i][j][0],q,'B'])
        if a in range(8,13):
            ans.append([fin_2017[i][j][0],q,'C'])
        else:
            ans.append([fin_2017[i][j][0],q,'D'])
print(ans)

            
    


      
            



        

        