import numpy as np

list1=[
        '资讯学群'
        ,'工程学群'
        ,'数理化学群'
        ,'医药卫生学群'
        ,'生命科学学群'
        ,'生物资源学群'
        ,'地球与环境学群'
        ,'建筑与设计学群'
        ,'艺术学群'
        ,'社会与心理学群'
        ,'大众传播学群'
        ,'外语学群'
        ,'文史哲学群'
        ,'教育学群'
        ,'法政学群'
        ,'管理学群'
        ,'财经学群'
        ,'游憩与运动学群'
]#学群名称

list2=[
        '计算能力'
        ,'科学能力'
        ,'抽象推理能力'
        ,'机械推理能力'
        ,'操作能力'
        ,'助人能力'
        ,'空间关系'
        ,'艺术创作能力'
        ,'音乐能力'
        ,'语文运用能力'
        ,'亲和力'
        ,'文书速度与准确度'
        ,'文艺创作能力'
        ,'组织能力'
        ,'领导能力'
        ,'销售能力'
        ,'沟通能力'
        ,'阅读能力'
]#能力名称

list3=np.array([
              [3,1,2,0],[3,2,1,0],[1,3,2,0],[3,2,2,1],[3,2,1,0],[3,1,2,0],
              [3,2,1,0],[3,2,1,0],[3,2,1,0],[3,2,1,0],[3,2,1,0],[0,1,2,3],
              [3,2,1,0],[3,2,2,0],[3,2,1,0],[3,2,2,0],[3,2,0,0],[3,2,1,0]
])#分数对照

list4=np.array([
              ['阅读能力','计算能力','科学能力','抽象推理能力']
              ,['阅读能力','计算能力','科学能力','抽象推理能力','机械推理能力','操作能力']
              ,['阅读能力','计算能力','科学能力','抽象推理能力','机械推理能力']
              ,['阅读能力','科学能力','操作能力','助人能力']
              ,['阅读能力','科学能力','操作能力']
              ,['阅读能力','科学能力','操作能力']
              ,['阅读能力','科学能力','操作能力','空间关系']
              ,['阅读能力','操作能力','空间关系','抽象推理能力','艺术创作能力']
              ,['阅读能力','操作能力','空间关系','抽象推理能力','音乐能力']
              ,['阅读能力','语文运用能力','助人能力','亲和力']
              ,['阅读能力','语文运用能力','文艺创作能力','艺术创作能力','操作能力']
              ,['阅读能力','语文运用能力','文艺创作能力','文书速度与准确度']
              ,['阅读能力','语文运用能力','文艺创作能力','文书速度与准确度']
              ,['阅读能力','语文运用能力','助人能力','亲和力']
              ,['阅读能力','语文运用能力','组织能力','领导能力']
              ,['阅读能力','语文运用能力','亲和力','组织能力','领导能力','销售能力']
              ,['计算能力','文书速度与准确度','阅读能力','组织能力','销售能力']
              ,['沟通能力','亲和力','销售能力','操作能力','艺术创作能力','空间关系']
])#能力参照

def Recommendation_of_Major(Answer):
    #Answer 是字典,形如{1:'A',2:'B',...},即第一题选A，第二题选B
    #以下是各项能力的评分
    temp_dict1=dict.fromkeys(list2)
    for i in range(18):
        if Answer[i+1]=='A':
            temp_dict1[list2[i]]=list3[i][0]
        elif Answer[i+1]=='B':
            temp_dict1[list2[i]]=list3[i][1]
        elif Answer[i+1]=='C':
            temp_dict1[list2[i]]=list3[i][2]
        elif Answer[i+1]=='D':
            temp_dict1[list2[i]]=list3[i][3]
    
    #以下是各个学群的推荐度计算
    temp_dict2=dict.fromkeys(list1)
    for i in range(18):
        score=0
        for j in list4[i]:
            score=score+temp_dict1[j]
        temp_dict2[list1[i]]=round(score/(4*len(list4[i])),2)

    m=max(temp_dict2,key=temp_dict2.get)
    m_score=temp_dict2[m]
    for group in temp_dict2.keys():
        temp_dict2[group]=temp_dict2[group]/m_score
    return temp_dict2#返回值是一个字典，形如{'资讯学群':0.56,'工程学群':0.78,...}


'''
# example
test_answer={1:'A',2:'B',3:'C',4:'D',5:'D',6:'A',7:'B',8:'D',9:'C',10:'D',11:'C',12:'D',13:'C',14:'D',15:'C',16:'C',17:'C',18:'C'}
result=Recommendation_of_Major(test_answer)
print(result)
'''