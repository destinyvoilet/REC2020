import pandas as pd  
import Levenshtein
from string import digits
import re

def getSimilarity(str1, str2):                      
   return Levenshtein.ratio(str1, str2)

def removeUnrelatedStr(string):                    
    #去除数字
    remove_digits = string.maketrans('', '', digits)
    string = string.translate(remove_digits)
    #去除无关字符/文字
    string = re.sub(r'[+＋“”，类（）批()？?+、含#H班【年】类]*', '', string)
    string = re.sub(r'[一二三四五六七八九十]*', '', string)
    string = re.sub(r'[ABCDE]*', '', string)
    #去除无关短语
    string = string.replace('一体化', '')
    string = string.replace('预备班', '')
    string = string.replace('预科班','')
    string = string.replace('中外合作办学', '')
    string = string.replace('实验班', '')
    string = string.replace('双语', '')
    string = string.replace('普通', '')
    string = string.replace(' ', '')
    string = string.replace('教学','')
    string = string.replace('合作','')
    string = string.replace('国防生','')
    string = string.replace('免费','')
    string = string.replace('公费','')
    string = string.replace('基地班','')
    string = string.replace('卓越','')
    string = string.replace('国家','')
    string = string.replace('试点','')
    string = string.replace('单列','')
    string = string.replace('民族','')
    string = string.replace('国家专项','')
    string = string.replace('提前','')
    return string

data = pd.read_csv("Majors.csv", encoding="gbk")
majors = data["majorName"].tolist()                  #获取majorName

#去重
majors = set(majors)
majors = list(majors)
majors.sort()

dfMajors = pd.DataFrame(majors, columns=['major'])

data2 = pd.read_csv("FirstLevelDiscipline.csv", encoding="gbk")
firstLevelDisciplineList = data2["1"].values.tolist()

Majors = []
for i in majors:
    k = removeUnrelatedStr(i)
    Majors.append(k)

first = []
simlist = []
for i in Majors:
    firstSimilarity = []
    for j in firstLevelDisciplineList:
        similarity = getSimilarity(i, j)
        firstSimilarity.append(similarity)
    index = firstSimilarity.index(max(firstSimilarity))
    firstLevelName = firstLevelDisciplineList[index]
    if(max(firstSimilarity) == "人工智能"):
        firstLevelName = "计算机科学与技术"
    if(i.find("语") != -1 and i.find("汉") == -1 and i.find("双语") == -1 and i.find("中国") == -1):
        firstLevelName = "外国语言文学"
    if(i.find("会计") != -1):
        firstLevelName = "工商管理"
    if(max(firstSimilarity)==0.0):
        firstLevelName = "！！！"
    first.append(firstLevelName)
    
firstDiscipline = pd.DataFrame(first, columns=["firstDiscipline"])
dfMajors = pd.concat([dfMajors, firstDiscipline], axis = 1)

dfMajors.to_csv('matchedFirstLevel6.csv', index = False, 
              columns = ['major', 'firstDiscipline'])


'''
#手动修改了约2%的数据
dfMajors = pd.read_csv("matchedFirstLevel6.csv", encoding="gbk")
SubjectCategory = []
for i in range(dfMajors.shape[0]):                
    for j in range(data2.shape[0]):
        if (dfMajors.iloc[i][1] == data2.iloc[j][1]):
            SubjectCategory.append(data2.iloc[j][0])
            break
            
#增加一列:对应的学科大类            
SubjectCategory = pd.DataFrame(SubjectCategory, columns=["SubjectCategory"])
dfMajors = pd.concat([dfMajors, SubjectCategory], axis = 1)

dfMajors.to_csv('matchedFirstLevel6.csv', index = False, 
              columns = ['major', 'firstDiscipline', "SubjectCategory"])
'''

