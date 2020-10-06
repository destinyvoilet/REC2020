from django.http import HttpResponse
from django.shortcuts import render
from ormDesign.models import *
import Levenshtein



# Create your views here.
def helloworld(request):
    return HttpResponse('Hello World! by kgInference group')

#Get certain major scores in different univ. and rank them  信息统计组数据需求

def getMajorScoresRanking(pID,cID,y,mName):
    #参数为省份ID（整数1-34），科类ID（整数1-3），年份（整数）和专业名称
    majorList=Majors.objects.filter(provinceID=pID,
                                    categoryID=cID,
                                    year=y,
                                    majorName=mName)
    scoresDict={}
    for major in majorList:
        scoresDict[major.collegeID.collegeName]=major.minScore
    #return scoresDict
    scoresOrder=dict(sorted(scoresDict.items(), key = lambda kv:kv[1],reverse=True))
    return scoresOrder

#Get the number of 985,211 and top in every province   地图组数据需求
def get_data_985():
    list_985=[]
    for i_ in range(1,35):
        count_985=Colleges.objects.filter(provinceID=i_,project985=True).aggregate(Count('collegeID'))
        list_985.append(count_985['collegeID__count'])
    return list_985


def get_data_211():
    list_211=[]
    for i_ in range(1,35):
        count_211=Colleges.objects.filter(provinceID=i_,project211=True).aggregate(Count('collegeID'))
        list_211.append(count_211['collegeID__count'])
    return list_211


def get_data_top():
    list_top=[]
    for i_ in range(1,35):
        count_top=Colleges.objects.filter(provinceID=i_,top=True).aggregate(Count('collegeID'))
        list_top.append(count_top['collegeID__count'])
    return list_top

def get_data():
    series=[]
    list_985=get_data_985()
    list_211=get_data_211()
    list_top=get_data_top()
    for i_ in range(0,34):
        temp={}
        province=Provinces.objects.filter(provinceID=i_+1)
        temp["name"]=province[0].provinceName
        temp["value"]=i_
        temp["project985"]=list_985[i_]
        temp["project211"]=list_211[i_]
        temp["doubleTop"]=list_top[i_]
        series.append(temp)
    return series

def testData(request):
    #scoresRanking=getMajorScoresRanking(16,1,2018,"all")
    #return render(request,"testData.html",{"scoresRanking":scoresRanking})
    series=get_data()
    return render(request,"testData.html",{"series":series})


def KgBaseInfoFillin(request):
    majorlist=Majors.objects.values_list('majorName',flat=True).distinct()
    provincelist=Provinces.objects.values_list('provinceName',flat=True).distinct()
    return render(request,'KgBaseInfoFillin.html',{'majorlist':majorlist,'provincelist':provincelist})
    
def InfoIntoQuestions(request):         #将用户输入信息转化成更具体的问题供用户选择
    province = request.POST.get('province')
    score = request.POST.get('score')
    score = int(score)
    category = request.POST.get('category')
    targetprovince = request.POST.get('Tprovince')
    targetmajor = request.POST.get('Tmajor')
    questions = []

    if(targetprovince == "" and targetmajor == ""):
        questionhead = province + category + str(score) + "分"
        question11 = questionhead + "冲一冲能上什么学校？"
        question12 = questionhead + "稳一稳能上什么学校？"
        question13 = questionhead + "保一保能上什么学校？"
        questions.append(question11)
        questions.append(question12)
        questions.append(question13)

        if(province == "江苏"):
            if(score >= 390):
                question14 = questionhead + "能上什么985学校?"
                questions.append(question13)
            if (score >= 370 and score < 390):
                question14 = questionhead + "能上什么985学校?"
                question15 = questionhead + "能上什么211学校?"
                questions.append(question14)
                questions.append(question15)
            if (score < 370 and score >= 360):
                question14 = questionhead + "能上什么211学校?"
                question15 = questionhead + "能上什么一本学校？"
                questions.append(question14)
                questions.append(question15)
            if(score < 360):
                question14 = questionhead + "能上什么一本学校？"
                questions.append(question14)

        elif(province == "上海"):
            if(score >= 560):
                question14 = questionhead + "能上什么985学校?"
                questions.append(question14)
            if (score >= 510 and score < 560):
                question14 = questionhead + "能上什么985学校?"
                question15 = questionhead + "能上什么211学校?"
                questions.append(question14)
                questions.append(question15)
            if (score < 510 and score >= 450):
                question14 = questionhead + "能上什么211学校?"
                question15 = questionhead + "能上什么一本学校？"
                questions.append(question14)
                questions.append(question15)
            if(score < 450):
                question14 = questionhead + "能上什么一本学校？"
                questions.append(question14)

        else:
            if(score >= 660):
                question14 = questionhead + "能上什么985学校?"
                questions.append(question14)
            if (score >= 620 and score < 660):
                question14 = questionhead + "能上什么985学校?"
                question15 = questionhead + "能上什么211学校?"
                questions.append(question14)
                questions.append(question15)
            if (score < 620 and score >= 590):
                question14 = questionhead + "能上什么211学校?"
                question15 = questionhead + "能上什么一本学校?"
                questions.append(question14)
                questions.append(question15)
            if(score < 590):
                question14 = questionhead + "能上什么一本学校？"
                questions.append(question14)


    if(targetprovince != "" and targetmajor == ""):
        questionhead = province + category + str(score) + "分"
        question21 = questionhead + "冲一冲能上" + targetprovince + "的什么学校？"
        question22 = questionhead + "稳一稳能上" + targetprovince + "的什么学校？"
        question23 = questionhead + "稳一稳能上" + targetprovince + "的什么学校？"
        question24 = targetprovince + "大学在本省" + category + "的录取分数线排名"

        questions.append(question21)
        questions.append(question22)
        questions.append(question23)
        questions.append(question24)

        if(province == "江苏"):
            if(score >= 390):
                question25 = questionhead + "能上" + targetprovince + "的什么985学校?"
                questions.append(question25)
            if (score >= 370 and score < 390):
                question25 = questionhead + "能上" + targetprovince + "的什么985学校?"
                question26 = questionhead + "能上" + targetprovince + "的什么211学校?"
                questions.append(question25)
                questions.append(question26)
            if (score < 370 and score >= 360):
                question25 = questionhead + "能上" + targetprovince + "的什么211学校?"
                question26 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question25)
                questions.append(question26)
            if(score < 360):
                question25 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question25)

        elif(province == "上海"):
            if(score >= 560):
                question25 = questionhead + "能上" + targetprovince + "的什么985学校?"
                questions.append(question25)
            if (score >= 510 and score < 560):
                question25 = questionhead + "能上" + targetprovince + "的什么985学校?"
                question26 = questionhead + "能上" + targetprovince + "的什么211学校?"
                questions.append(question25)
                questions.append(question26)
            if (score < 510 and score >= 450):
                question25 = questionhead + "能上" + targetprovince + "的什么211学校?"
                question26 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question25)
                questions.append(question26)
            if(score < 450):
                question25 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question25)

        else:
            if(score >= 660):
                question25 = questionhead + "能上" + targetprovince + "什么985学校?"
                questions.append(question25)
            if (score >= 620 and score < 660):
                question25 = questionhead + "能上" + targetprovince + "的什么985学校?"
                question26 = questionhead + "能上" + targetprovince + "的什么211学校?"
                questions.append(question25)
                questions.append(question26)
            if (score < 620 and score >= 590):
                question25 = questionhead + "能上" + targetprovince + "的什么211学校?"
                question26 = questionhead + "能上" + targetprovince + "的什么一本学校?"
                questions.append(question25)
                questions.append(question26)
            if(score < 590):
                question25 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question25)

    if(targetprovince == "" and targetmajor != ""):
        question31 = targetmajor + "专业" + "全国大学在本省的录取分数线排名？"
        question32 = province + category + str(score) + "分" + "能上哪些学校的" + targetmajor + "专业？"
        questions.append(question31)
        questions.append(question32)

        questionhead = province + category + str(score) + "分"
        question33 = questionhead + "冲一冲能上" + "什么学校？"
        question34 = questionhead + "稳一稳能上" + "什么学校？"
        question35 = questionhead + "稳一稳能上" + "什么学校？"

        questions.append(question33)
        questions.append(question34)
        questions.append(question35)

    if(targetprovince != "" and targetmajor != ""):
        question41 = targetmajor + "专业" + targetmajor + "省的大学在" + targetprovince + "省的录取分数排名"
        #questions.append(question41)
        questions.append(question41)

        questionhead = province + category + str(score) + "分"
        question42 = questionhead + "冲一冲能上" + targetprovince + "的什么学校？"
        question43 = questionhead + "稳一稳能上" + targetprovince + "的什么学校？"
        question44 = questionhead + "稳一稳能上" + targetprovince + "的什么学校？"
        question45 = targetprovince + "大学在本省" + category + "的录取分数线排名"

        questions.append(question42)
        questions.append(question43)
        questions.append(question44)
        questions.append(question45)

        questionhead = province + category + str(score) + "分能上什么" + targetprovince + "省的大学？"
        if(province == "江苏"):
            if(score >= 390):
                question46 = questionhead + "985学校?"
                questions.append(question46)
            if (score >= 370 and score < 390):
                question46 = questionhead + "985学校?"
                question47 = questionhead + "211学校?"
                questions.append(question46)
                questions.append(question47)
            if (score < 370 and score >= 360):
                question46 = questionhead + "211学校?"
                question47 = questionhead + "一本学校？"
                questions.append(question46)
                questions.append(question47)
            if(score < 360):
                question46 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question46)

        elif(province == "上海"):
            if(score >= 560):
                question46 = questionhead + "985学校?"
                questions.append(question46)
            if (score >= 510 and score < 560):
                question46 = questionhead + "985学校?"
                question47 = questionhead + "211学校?"
                questions.append(question46)
                questions.append(question47)
            if (score < 510 and score >= 450):
                question46 = questionhead + "211学校?"
                question47 = questionhead + "一本学校？"
                questions.append(question46)
                questions.append(question47)
            if(score < 450):
                question46 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question46)

        else:
            if(score >= 660):
                question46 = questionhead + "985学校?"
                questions.append(question46)
            if (score >= 620 and score < 660):
                question46 = questionhead + "985学校?"
                question47 = questionhead + "211学校?"
                questions.append(question46)
                questions.append(question47)
            if (score < 620 and score >= 590):
                question46 = questionhead + "211学校?"
                question47 = questionhead + "一本学校?"
                questions.append(question46)
                questions.append(question47)
            if(score < 590):
                question46 = questionhead + "一本学校？"
                questions.append(question46)
    return render(request,'KgInfoToQuestion.html',{'questions':questions,'score':score})


def getSimilarity(str1, str2):
   return Levenshtein.ratio(str1, str2)



def ChooseFunction(request):
    question = request.POST.get('question')
    question = str(question)
    #首先判断选填内容是否填了
    tprovince = request.POST.get('Tprovince')
    tmajor = request.POST.get('Tmajor')        #tprovince/tmajor从前端传回

    tprovince = "all"
    tmajor = "all"

    questionModelList = []
    similarity = []
    #1.两个选填的都没填
    if(tprovince == "all" and tmajor == "all"):
        question11 = "**省*科**分冲一冲能上什么学校？"
        question12 = "**省*科**分稳一稳能上什么学校？"
        question13 = "**省*科**分保一保能上什么学校？"
        question14 = "**省*科**分能上什么/985学校/211学校/本科学校？"
        questionModelList = [question11, question12, question13, question14]
        similarity = [getSimilarity(question, i) for i in questionModelList]
        quesindex=similarity.index(max(similarity))
        switch = {
            0: QuestionsIntoAnswer11,
            1: QuestionsIntoAnswer12,
            2: QuestionsIntoAnswer13,
            3: QuestionsIntoAnswer14
        }
        switch[quesindex](request)


    if(tprovince != "all" and tmajor == "all"):
        question11 = "**省*科**分冲一冲能上***省的什么学校？"
        question12 = "**省*科**分稳一稳能上***省的什么学校？"
        question13 = "**省*科**分保一保能上***省的什么学校？"
        question14 = "***省大学在**省*科的分数线排名？"
        question15 = "**省*科**分能上**省的什么985学校/211学校/本科学校？"
        questionModelList = [question11, question12, question13, question14, question15]
        similarity = [getSimilarity(question, i) for i in questionModelList]
        quesindex=similarity.index(max(similarity))
        switch = {
            0: QuestionsIntoAnswer21,
            1: QuestionsIntoAnswer22,
            2: QuestionsIntoAnswer23,
            3: QuestionsIntoAnswer24,
            4: QuestionsIntoAnswer25,
        }
        switch[quesindex](request)

    if(tprovince == "all" and tmajor != "all"):
        question11 = "**专业全国大学在**省的录取分数线排名？"
        question12 = "**省*科*分能上哪些学校的**专业？"
        question13 = "**省*科**分冲一冲能上什么学校？"
        question14 = "**省*科**分稳一稳能上什么学校？"
        question15 = "**省*科**分保一保能上什么学校？"
        question16 = "**省*科**分能上什么/985学校/211学校/本科学校?"

        questionModelList = [question11, question12, question13, question14,question15, question16]
        similarity = [getSimilarity(question, i) for i in questionModelList]
        quesindex = similarity.index(max(similarity))
        switch = {
            0: QuestionsIntoAnswer31,
            1: QuestionsIntoAnswer32,
            2: QuestionsIntoAnswer11,
            3: QuestionsIntoAnswer12,
            4: QuestionsIntoAnswer13,
            5: QuestionsIntoAnswer14,
        }
        switch[quesindex](request)

    if (tprovince != "all" and tmajor != "all"):
        question11 = "**专业***省的大学在本省录取分数线排名？"
        question12 = "**省*科*分冲一冲能上***省的什么学校？"
        question13 = "**省*科*分稳一稳能上***省的什么学校？"
        question14 = "**省*科*分保一保能上***省的什么学校？"
        question15 = "**省*科**分能上**省的什么985学校/211学校/本科学校？"
        question16 = "**专业***省的大学在本省的录取分数线排名？"
        question17 = "**专业全国大学在本省的录取分数线排名？"
        questionModelList = [question11, question12, question13, question14,question15, question16]
        similarity = [getSimilarity(question, i) for i in questionModelList]
        quesindex = similarity.index(max(similarity))
        switch = {
            0: QuestionsIntoAnswer41,
            1: QuestionsIntoAnswer21,
            2: QuestionsIntoAnswer22,
            3: QuestionsIntoAnswer23,
            4: QuestionsIntoAnswer25,
            5: QuestionsIntoAnswer42,
            6: QuestionsIntoAnswer31,
        }
        switch[quesindex](request)

    return render(request, 'KgInfoAnswers.html', {})

def GetCollegeMinScore(collegeid, provinceid, categoryid, year):               #获得学校在某个省文科/理科某一年的最低录取分数
    collegeMajorScoreList = Majors.objects.filter(collegeID_id = collegeid, provinceID_id=provinceid, categoryID_id = categoryid, year=year)
    scores = []
    for i in collegeMajorScoreList:
        scores.append(int(i.minScore))
    minscore = 0
    if len(scores):    #若列表不为空
        minscore = min(scores)
    return minscore

def GetCollegeAverageMinScore(collegeid, provinceid, categoryid):              #获得学校在某个省文科/理科三年的最低录取分数
    average = (GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)+
              GetCollegeMinScore(collegeid, provinceid, categoryid, 2018)+
              GetCollegeMinScore(collegeid, provinceid, categoryid, 2017))/3
    return average


