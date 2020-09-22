from concretegrade import  majorscore,sgremmendation
from grade1 import getrecommendation
import pandas as pd


province='江苏'
category='理科'
college='同济大学'
rank=1
#major="纺织工程（普通类）"       
gradelist={"数学":140,"语文":130,"外语":120,"物理":90,"化学":100,"生物":90,"历史":0,"政治":0,"地理":0,"技术":0}

rrc=getrecommendation(province, category, college, rank)
#rrc=pd.DataFrame(rrc, columns=['推荐度', '风险值', '专业'])
#print(rrc)

sgscore=sgremmendation(gradelist,province,category)
#print(sgscore)
#print(majorscore(major,sgscore))

result=[]
for temp in rrc:
    major=temp[-1]
    risk=temp[1]
    r1=temp[0]
    r2=majorscore(major,sgscore)
    
    w1=0.6
    w2=0.4
    
    rl=r1*w1+r2*w2
    
    result.append([rl,risk,major])
    
    
 