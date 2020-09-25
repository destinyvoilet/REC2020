import pandas as pd


#输入的单科成绩,输出学群推荐度
def sgremmendation(gradelist,province,category):
    sg2abl=getsg2abl()
    sub2abl=getsub2abl()
    advancesub=getadvancesub(gradelist,province,category)
    
    sgscore={}
    
    for key,values in sg2abl.items():
        sgscore[key]=0
        
        for subject in advancesub:
            abls=sub2abl[subject]
            for abl in abls:
                if abl in values: 
                    sgscore[key]+=1
                    
    vec = sorted(sgscore.items(), key=lambda d:d[1], reverse=True)
    maxscore=vec[0][1]
    for key,values in sgscore.items():
        sgscore[key]=values/maxscore
        
    return sgscore




#获得优势学科
def getadvancesub(gradelist,province,category):
    advancesub=[]
    if (province == '江苏'):
        if (category == '文科'):
            for key,values in gradelist.items():
                if(key=='语文'):
                    if values>155:
                        advancesub.append(key)
                elif(key=='数学'):
                    if values>140:
                        advancesub.append(key)
                elif(key=='外语'):
                    if values>105:
                        advancesub.append(key)
        if (category == '理科'):
            for key,values in gradelist.items():
                if(key=='语文'):
                    if values>120:
                        advancesub.append(key)
                elif(key=='数学'):
                    if values>170:
                        advancesub.append(key)
                elif(key=='外语'):
                    if values>105:
                        advancesub.append(key)
    elif (province == '上海'):
        for key,values in gradelist.items():
            if(key=='语文'):
                if values>130:
                    advancesub.append(key)
            elif(key=='数学' or key=='外语'):
                if values>140:
                    advancesub.append(key)
            else:
                if values>65:
                    advancesub.append(key)
    elif (province == '浙江'):
        for key,values in gradelist.items():
            if(key=='语文'):
                if values>125:
                    advancesub.append(key)
            elif(key=='数学'):
                if values>130:
                    advancesub.append(key)
            elif(key=='外语'):
                if values>140:
                    advancesub.append(key)
            else:
                if values>90:
                    advancesub.append(key)
    elif (province == '北京' or province == '天津'):
        for key,values in gradelist.items():
            if(key=='语文'):
                if values>130:
                    advancesub.append(key)
            elif(key=='数学' or key=='外语'):
                if values>140:
                    advancesub.append(key)
            elif(key=='物理'):
                if values>110:
                    advancesub.append(key)
            elif(key=='生物'):
                if values>70:
                    advancesub.append(key)
            elif(key=='化学' or key=='政治' or key=='历史' or key=='地理'):
                if values>90:
                    advancesub.append(key)
    else:
        for key,values in gradelist.items():
            if(key=='语文'):
                if values>130:
                    advancesub.append(key)
            elif(key=='数学' or key=='外语'):
                if values>140:
                    advancesub.append(key)
            elif(key=='物理'):
                if values>100:
                    advancesub.append(key)
            elif(key=='生物'):
                if values>80:
                    advancesub.append(key)
            elif(key=='化学' or key=='政治' or key=='历史' or key=='地理'):
                if values>90:
                    advancesub.append(key)
    return advancesub


#获得单科推荐度
def majorscore(major,sgscore):
    majorscore=0
    count=0
    
    maj2maj1=getmaj2maj1()
    maj12sg=getmaj12sg()
    major1=maj2maj1[major]
    major1=major1.split(";")
    for temp1 in major1:
        sg=maj12sg[temp1]
        majorscore+=sgscore[sg]
        count+=1
        
    return majorscore/count
        


#科目对应能力
def getsub2abl():
    sub2abl={}
    with open('单科成绩-能力.txt','r+',encoding='utf-8') as f:
        for line in f:
            subject,abilities=line.split()
            ability=abilities.split('，')
            sub2abl[subject]=ability
    return sub2abl


#学群对应能力
def getsg2abl():
    sgcsv=pd.read_excel("学群能力对应关系.xlsx")
    sg=sgcsv["学群"]
    ability=sgcsv["需要能力"]
    sg2abl=dict(zip(sg,ability))
    return sg2abl
            
#一级学科对应学群
def getmaj12sg():
    maj12sg={}
    with open('一级学科-学群.txt','r+',encoding='utf-8') as f:
        for line in f:
            if(len(line.split())==2):
                major1,sg=line.split()
                id,major1=major1.split(",")
                maj12sg[major1]=sg
    return maj12sg
    

#具体学科对应一级学科
def getmaj2maj1():
    majorcsv=pd.read_csv('result.csv')
    major1=majorcsv['major2 (disambiguated)']
    major=majorcsv['major (origin)']  
    maj2maj1=dict(zip(major,major1))  
    return maj2maj1

'''
major="纺织工程（普通类）"       
gradelist={"数学":140,"语文":130,"外语":120,"物理":90,"化学":100,"生物":90,"历史":0,"政治":0,"地理":0,"技术":0}
province='浙江'
category='不分文理'

sgscore=sgremmendation(gradelist,province,category)
#print(sgscore)
#print(majorscore(major,sgscore))

#print(getmaj12sg()) #{'哲学': '文史哲学群', '理论经济学': '财政学群', '应用经济学': '财政学群', '法学': '法政学群', '政治学': '法政学群', '社会学': '社会与心理学群', '民族学': '社会与心理学群', '马克思主义理论': '文史哲学群', '教育学': '教育学群', '心理学': '社会与心理学群', '体育学': '游憩与运动学群', '中国语言文学': '文史哲学群', '外国语言文学': '外语学群', '新闻传播学': '大众传媒学群', '艺术学': '艺术学群', '历史学': '文史哲学群', '数学': '数理化学群', '物理学': '数理化学群', '化学': '数理化学群', '天文学': '数理化学群', '地理学': '地球与环境学群', '大气科学': '地球与环境学群', '海洋科学': '地球与环境学群', '地球物理学': '地球与环境学群', '地质学': '地球与环境学群', '生物学': '生命科学学群', '系统科学': '资讯学群，管理学群', '力学': '工程学群', '机械工程': '工程学群', '仪器科学与技术': '工程学群', '材料科学与工程': '工程学群', '冶金工程': '工程学群', '动力工程及工程热物理': '工程学群', '电气工程': '工程学群', '电子科学与技术': '工程学群', '信息与通讯工程': '资讯学群', '控制科学与工程': '工程学群', '计算机科学与技术': '资讯学群', '建筑学': '建筑与设计学群', '土木工程': '工程学群', '水利工程': '工程学群', '测绘科学与技术': '工程学群', '化学工程与技术': '工程学群', '地质资源与地质工程': '地球与环境学群', '矿业工程': '地球与环境学群', '石油与天然气工程': '地球与环境学群', '纺织科学与工程': '工程学群', '轻工技术与工程': '工程学群', '交通运输工程': '工程学群', '船舶与海洋工程': '工程学群', '航空宇航科学与技术': '工程学群', '兵器科学与技术': '工程学群', '核科学与技术': '工程学群', '农业工程': '工程学群', '林业工程': '工程学群', '环境科学与工程': '生物资源学群', '食品科学与工程': '生物资源学群', '作物学': '生物资源学群', '园艺学': '生物资源学群', '农业资源与环境': '生物资源学群', '植物保护': '生物资源学群', '畜牧学': '生物资源学群', '兽医学': '生物资源学群', '林学': '生物资源学群', '水产': '生物资源学群', '基础医学': '医药卫生学群', '临床医学': '医药卫生学群', '口腔医学': '医药卫生学群', '公共卫生与预防医学': '医药卫生学群', '中医学': '医药卫生学群', '中西医结合': '医药卫生学群', '药学': '医药卫生学群', '军事思想及军事历史': '军事学群', '战略学': '军事学群', '战役学': '军事学群', '战术学': '军事学群', '军队指挥学': '军事学群', '军制学': '军事学群', '军事后勤学与军事装备学': '军事学群', '工商管理': '管理学群', '农林经济管理': '管理学群', '公共管理': '管理学群', '图书情报与档案管理': '管理学群'}
#print(getsg2abl()) #{'资讯学群': '阅读能力，计算能力，科学能力，抽象推理能力', '工程学群': '阅读能力，计算能力，科学能力，抽象推理能力，机械推理能力，操作能力', '数理化学群': '阅读能力，计算能力，科学能力，抽象推理能力，机械推理能力', '医药卫生学群': '阅读能力，科学能力，操作能力，助人能力', '生命科学学群': '阅读能力，科学能力，操作能力', '生物资源学群': '阅读能力，科学能力，操作能力', '地球与环境学群': '阅读能力，科学能力，操作能力，空间关系', '建筑与设计学群': '阅读能力，操作能力，空间关系，抽象推理能力，艺术创作能力', '艺术学群': '阅读能力，操作能力，空间关系，抽象推理能力，音乐能力', '社会与心理学群': '阅读能力，语文运用能力，助人能力，亲和力', '大众传播学群': '阅读能力，语文运用能力，文艺创作能力，艺术创作魅力，操作能力', '外语学群': '阅读能力，语文运用能力，文艺创作能力，文书速度与准确度', '文史哲学群': '阅读能力，语文运用能力，文艺创作能力，文书速度与准确度', '教育学群': '阅读能力，语文运用能力，助人能力，亲和力', '法政学群': '阅读能力，语文运用能力，组织能力，领导能力', '管理学群': '阅读能力，语文运用能力，亲和力，组织能力，领导能力，销售能力', '财政学群': '计算能力，文书速度与准确度，阅读能力，组织能力，销售能力', '游憩与运动学群': '沟通能力，亲和力，销售能力，操作能力，艺术创作能力，空间关系'}

#print(getmaj2maj1())

#print(getsub2abl())#{'语文': ['阅读能力', '语文运用能力', '文艺创作能力', '文书速度与准确度', '沟通能力'], '数学': ['计算能力', '科学能力', '抽象推理能力', '机械推理能力', '空间关系', '销售能力'], '外语': ['阅读能力', '语文运用能力', '文艺创作能力', '文书速度与准确度', '沟通能力'], '物理': ['计算能力', '科学能力', '抽象推理能力', '机械推理能力', '操作能力', '空间关系'], '化学': ['计算能力', '科学能力', '抽象推理能力', '机械推理能力', '操作能力'], '生物': ['阅读能力', '机械推理能力'], '历史': ['阅读能力', '语文运用能力', '文书速度与准确度'], '政治': ['阅读能力', '科学能力', '抽象推理能力', '语文运用能力', '文书速度与准确度', '组织能力', '领导能力', '销售能力'], '地理': ['阅读能力', '计算能力', '科学能力', '机械推理能力', '空间关系', '文书速度与准确度'], '技术': ['计算能力', '科学能力', '抽象推理能力', '机械推理能力', '操作能力']}

'''
