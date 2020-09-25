import pandas as pd
import json
import string
import os.path
import math

def getrankpd():
    borderline=pd.read_csv('高校录取分数线整合（省份名字统一）.csv',encoding='utf-8')
    #print(borderline)
    ranks=[]
    for indexs in borderline.index:
        line=borderline.loc[indexs].values
        province=line[2]
        category=line[3]
        college=line[0]
        year=line[1]
        major=line[4]
        score=line[5]
        
        if(category=='不分文理'):
            category='all'
        
        file='json_csv(09150017)/'+str(year)+province+category+'.csv'
        if not(os.path.exists(file)):
            rank=-1
        else:
            rank=pd.read_csv(file,encoding='utf-8') 
            rank=rank[rank["分数"]==score]["累计人数"].tolist()
            if rank:
                rank=rank[0]
            else:
                rank=-1
        
        ranks.append(rank)
    borderline['rank']=ranks
    f1="rank.csv"
    borderline.to_csv(f1, sep=',', header=True, index=False,encoding='utf-8-sig')


def getrecommendation1(province,category,college,rank):
    borderline=pd.read_csv('rank.csv',encoding='utf-8')
    bl= borderline[borderline['Province']==province]
    bl= bl[bl['category']==category]
    bl= bl[bl['College']==college]
    
    
    m=bl['Major'].tolist()
    majors=[]
    for major in m:
        if major not in majors:
            majors.append(major)
    ss=[]


    for major in majors:
        recommendation=evaluate1(bl,major,rank)
        risk=getrisk(bl,major,rank)
        ss.append([recommendation,risk,major])
        
    ss.sort(reverse=True) 
    
    if ss==[]:
        return 0
    
    maxscore=ss[0][0]
    for i in range(len(ss)):
        ss[i][0]/=maxscore
    
    return ss

def getrisk(bl,major,inputrank):
    bl= bl[bl['Major']==major]
    rank9=bl[bl['Year']==2019]['rank'].tolist()[0] if bl[bl['Year']==2019]['rank'].tolist() else -1
    rank8=bl[bl['Year']==2018]['rank'].tolist()[0] if bl[bl['Year']==2018]['rank'].tolist() else -1
    rank7=bl[bl['Year']==2017]['rank'].tolist()[0] if bl[bl['Year']==2017]['rank'].tolist() else -1

    rank=[rank9, rank8, rank7]
    count=0
    a_rank=0
    for y in rank:
        if y!=-1:
            count+=1
            a_rank+=y
        if count==0:
            m_rank=-1
        else:
            m_rank=a_rank/count
    
    diff=m_rank-inputrank
    
    if diff>500:
            risk=0
    elif diff<-500:
        risk=1
    else:
        risk=0.5-diff/1000

    return risk

def evaluate1(bl,major,rank):
    bl= bl[bl['Major']==major]
    rank9=bl[bl['Year']==2019]['rank'].tolist()[0] if bl[bl['Year']==2019]['rank'].tolist() else -1
    rank8=bl[bl['Year']==2018]['rank'].tolist()[0] if bl[bl['Year']==2018]['rank'].tolist() else -1
    rank7=bl[bl['Year']==2017]['rank'].tolist()[0] if bl[bl['Year']==2017]['rank'].tolist() else -1


    r9=rank9-rank if (rank9-rank)>0 else rank-rank9
    r8=rank8-rank if (rank8-rank)>0 else rank-rank8
    r7=rank7-rank if (rank7-rank)>0 else rank-rank7
    
    
    w9=0.4 if rank9!=-1 else 0
    w8=0.3 if rank8!=-1 else 0
    w7=0.3 if rank7!=-1 else 0
        
    
    if((w9+w8+w7)!=1 and (w9+w8+w7)!=0):
        r=1/(w9+w8+w7)
        w9=r*w9
        w8=r*w8
        w7=r*w7

    x=(r9*w9+r8*w8+r7*w7)*0.05   
    recommendation=1/x

    return recommendation




'''
def getrecommendation(province,category,college,rank):
    borderline=pd.read_csv('高校录取分数线整合（省份名字统一）.csv',encoding='utf-8')
    bl= borderline[borderline['Province']==province]
    bl= bl[bl['category']==category]
    bl= bl[bl['College']==college]
    
    
    m=bl['Major'].tolist()
    majors=[]
    for major in m:
        if major not in majors:
            majors.append(major)
    ss=[]
    for major in majors:
        recommendation,risk=evaluate(province,category,bl,major,rank)
        ss.append([recommendation,risk,major])
        
    ss.sort(reverse=True) 
    maxscore=ss[0][0]
    for i in range(len(ss)):
        ss[i][0]/=maxscore
    
    return ss




def evaluate(province,category,bl,major,rank):
    rank9=getrank(province,category,bl,major,2019)
    rank8=getrank(province,category,bl,major,2018)
    rank7=getrank(province,category,bl,major,2017)
    
    w9=0.4 if rank9!=-1 else 0
    w8=0.3 if rank8!=-1 else 0
    w7=0.3 if rank7!=-1 else 0
    
    r9=rank9-rank if (rank9-rank)>0 else rank-rank9
    r8=rank8-rank if (rank8-rank)>0 else rank-rank8
    r7=rank7-rank if (rank7-rank)>0 else rank-rank7
    
    d9=rank-rank9 if (rank9-rank)>0 else 0
    d8=rank-rank8 if (rank8-rank)>0 else 0
    d7=rank-rank7 if (rank7-rank)>0 else 0
    
    
    if((w9+w8+w7)!=1 and (w9+w8+w7)!=0):
        r=1/(w9+w8+w7)
        w9=r*w9
        w8=r*w8
        w7=r*w7

    x=(r9*w9+r8*w8+r7*w7)*0.05
    y=(d9*w9+d8*w8+d7*w7)*0.05
    
    
    
    recommendation=1/x
    risk=2/(1+math.exp(-y))
    return recommendation,risk

    
def getrank(province,category,bl,major,year):
    bl=bl[bl['Year']==year]
    if(category=='不分文理'):
        category='all'
    score=bl[bl['Major']==major]['score'].tolist()
    if score:
        score=score[0]
    else:
        return -1

    file='json_csv(09150017)/'+str(year)+province+category+'.csv'
    if not(os.path.exists(file)):
        return -1
    rank=pd.read_csv(file,encoding='utf-8') 
    rank=rank[rank["分数"]==score]["累计人数"].tolist()
    if rank:
        rank=rank[0]
    else:
        return -1
    return rank
    
'''

'''
#getrankpd()

province='江苏'
category='理科'
college='同济大学'
#grade=400
rank=2000
rcc=getrecommendation1(province, category, college, rank)
result=pd.DataFrame(rcc, columns=['推荐度', '风险值', '专业'])
print(result)
'''