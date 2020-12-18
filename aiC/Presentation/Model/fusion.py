from 单科2专业 import  majorscore,sggraderemmendation
from grade1 import getrecommendation1
import pandas as pd
from 竞赛2专业 import recommand,group_score
from 问卷2专业 import Recommendation_of_Major

def main():
    province='江苏'
    category='理科'
    college='复旦大学'
    rank=2000
    #major="纺织工程（普通类）"       
    gradelist={"数学":140,"语文":130,"外语":120,"物理":90,"化学":100,"生物":90,"历史":0,"政治":0,"地理":0,"技术":0}
    exp=[['全国中学生科普科幻作文大赛','全国一等奖'],['全国青少年科学影像大赛','提名奖']]
    #exp=[['全国中学生数学竞赛','国家二等奖'],['中国青少年机器人竞赛','二等奖']]
    answer={1:'A',2:'B',3:'C',4:'D',5:'D',6:'A',7:'B',8:'D',9:'C',10:'D',11:'C',12:'D',13:'C',14:'D',15:'C',16:'C',17:'C',18:'C'}
    result=getr(province, category, college,rank,exp,gradelist,answer)


def getsgscore(province, category, college, rank,exp,gradelist,answer):
    sgscore={}    
    gradescore=sggraderemmendation(gradelist,province,category)
    competitionscore=recommand(group_score(exp))
    questionscore=Recommendation_of_Major(answer)
    wg=wc=wq=1/3
    for key,values in gradescore.items():
        sgscore[key]=gradescore[key]*wg+competitionscore[key]*wc+questionscore[key]*wq
    return sgscore


def getr(province, category, college, rank,exp,gradelist,answer):
    
    rrc=getrecommendation1(province, category, college, rank)
    if(rrc==0):
        print("我们系统不推荐这个大学")
        return
    
    sgscore=getsgscore(province, category, college, rank,exp,gradelist,answer)
    result=[]
    for temp in rrc:
        major=temp[-1]
        risk=temp[1]
        r1=temp[0]
        r2=majorscore(major,sgscore)
        
        w1=0.5
        w2=0.5
        
        rl=r1*w1+r2*w2
        
        result.append([rl,risk,major])
        
    result.sort(reverse=True)
    
    for i in range(len(result)):
        result[i]=[result[i][-1],result[i][0],result[i][1]]
    result=pd.DataFrame(result, columns=['专业', '推荐度', '风险值'])
    print(result)
    
    
if __name__ == '__main__':
    main()