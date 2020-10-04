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
    
    
def InfoIntoQuestions(request):  #将用户输入信息转化成更具体的问题，经用户选择具体问题后生成图标。by:陈震寰&张立创
    province = request.POST.get('province')
    score = request.POST.get('score')
    score = int(score)
    subject = request.POST.get('subject')
    targetprovince = request.POST.get('Tprovince')
    targetmajor = request.POST.get('Tmajor')
    questions = []

    if(targetprovince == "" and targetmajor == ""):
        questionhead = province + str(score) + "分"
        question11 = questionhead + "冲一冲能上什么学校？"
        question12 = questionhead + "稳一稳能上什么学校？"
        questions.append(question11)
        questions.append(question12)
        #schooltype = "普通一本"
        if(province == "江苏"):
            if(score >= 390):
                question13 = questionhead + "能上什么985学校?"
                questions.append(question13)
            if (score >= 370 and score < 390):
                question13 = questionhead + "能上什么985学校?"
                question14 = questionhead + "能上什么211学校?"
                questions.append(question13)
                questions.append(question14)
            if (score < 370 and score >= 360):
                question13 = questionhead + "能上什么211学校?"
                question14 = questionhead + "能上什么一本学校？"
                questions.append(question13)
                questions.append(question14)
            if(score < 360):
                question13 = questionhead + "能上什么一本学校？"
                questions.append(question13)

        elif(province == "上海"):
            if(score >= 560):
                question13 = questionhead + "能上什么985学校?"
                questions.append(question13)
            if (score >= 510 and score < 560):
                question13 = questionhead + "能上什么985学校?"
                question14 = questionhead + "能上什么211学校?"
                questions.append(question13)
                questions.append(question14)
            if (score < 510 and score >= 450):
                question13 = questionhead + "能上什么211学校?"
                question14 = questionhead + "能上什么一本学校？"
                questions.append(question13)
                questions.append(question14)
            if(score < 450):
                question13 = questionhead + "能上什么一本学校？"
                questions.append(question13)

        else:
            if(score >= 660):
                question13 = questionhead + "能上什么985学校?"
                questions.append(question13)
            if (score >= 620 and score < 660):
                question13 = questionhead + "能上什么985学校?"
                question14 = questionhead + "能上什么211学校?"
                questions.append(question13)
                questions.append(question14)
            if (score < 620 and score >= 590):
                question13 = questionhead + "能上什么211学校?"
                question14 = questionhead + "能上什么一本学校?"
                questions.append(question13)
                questions.append(question14)
            if(score < 590):
                question13 = questionhead + "能上什么一本学校？"
                questions.append(question13)


    if(targetprovince != "" and targetmajor == ""):
        questionhead = province + str(score) + "分"
        question21 = questionhead + "冲一冲能上" + targetprovince + "的什么学校？"
        question22 = questionhead + "稳一稳能上" + targetprovince + "的什么学校？"
        question23 = targetprovince + "大学分数线排名"
        questions.append(question21)
        questions.append(question22)
        questions.append(question23)
        schooltype = "普通一本"

        if(province == "江苏"):
            if(score >= 390):
                question24 = questionhead + "能上" + targetprovince + "的什么985学校?"
                questions.append(question24)
            if (score >= 370 and score < 390):
                question24 = questionhead + "能上" + targetprovince + "的什么985学校?"
                question25 = questionhead + "能上" + targetprovince + "的什么211学校?"
                questions.append(question24)
                questions.append(question25)
            if (score < 370 and score >= 360):
                question24 = questionhead + "能上" + targetprovince + "的什么211学校?"
                question25 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question24)
                questions.append(question25)
            if(score < 360):
                question24 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question24)

        elif(province == "上海"):
            if(score >= 560):
                question24 = questionhead + "能上" + targetprovince + "的什么985学校?"
                questions.append(question24)
            if (score >= 510 and score < 560):
                question24 = questionhead + "能上" + targetprovince + "的什么985学校?"
                question25 = questionhead + "能上" + targetprovince + "的什么211学校?"
                questions.append(question24)
                questions.append(question25)
            if (score < 510 and score >= 450):
                question24 = questionhead + "能上" + targetprovince + "的什么211学校?"
                question25 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question24)
                questions.append(question25)
            if(score < 450):
                question24 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question24)

        else:
            if(score >= 660):
                question24 = questionhead + "能上" + targetprovince + "什么985学校?"
                questions.append(question24)
            if (score >= 620 and score < 660):
                question24 = questionhead + "能上" + targetprovince + "的什么985学校?"
                question25 = questionhead + "能上" + targetprovince + "的什么211学校?"
                questions.append(question24)
                questions.append(question25)
            if (score < 620 and score >= 590):
                question24 = questionhead + "能上" + targetprovince + "的什么211学校?"
                question25 = questionhead + "能上" + targetprovince + "的什么一本学校?"
                questions.append(question24)
                questions.append(question25)
            if(score < 590):
                question24 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question24)

    if(targetprovince == "" and targetmajor != ""):
        question31 = targetmajor + "专业" + "全国大学排名"
        question32 = province + str(score) + "分" + "哪些学校的" + targetmajor + "专业" + "性价比比较高？"
        question33 = province + str(score) + "分" + "能上哪些学校的" + targetmajor + "专业？"
        questions.append(question31)
        questions.append(question32)
        questions.append(question33)

    if(targetprovince != "" and targetmajor != ""):
        question41 = province + str(score) + "在" + targetprovince + "哪些学校的" + targetmajor + "专业性价比比较高？"
        question42 = targetprovince + targetmajor + "专业大学排名"
        questions.append(question41)
        questions.append(question42)

        questionhead = province + str(score) + "分在" + targetprovince + "能上什么"
        if(province == "江苏"):
            if(score >= 390):
                question43 = questionhead + "985学校?"
                questions.append(question43)
            if (score >= 370 and score < 390):
                question43 = questionhead + "985学校?"
                question44 = questionhead + "211学校?"
                questions.append(question43)
                questions.append(question44)
            if (score < 370 and score >= 360):
                question43 = questionhead + "211学校?"
                question44 = questionhead + "一本学校？"
                questions.append(question43)
                questions.append(question44)
            if(score < 360):
                question43 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question43)

        elif(province == "上海"):
            if(score >= 560):
                question43 = questionhead + "985学校?"
                questions.append(question43)
            if (score >= 510 and score < 560):
                question43 = questionhead + "985学校?"
                question44 = questionhead + "211学校?"
                questions.append(question43)
                questions.append(question44)
            if (score < 510 and score >= 450):
                question43 = questionhead + "211学校?"
                question44 = questionhead + "一本学校？"
                questions.append(question43)
                questions.append(question44)
            if(score < 450):
                question43 = questionhead + "能上" + targetprovince + "的什么一本学校？"
                questions.append(question43)

        else:
            if(score >= 660):
                question43 = questionhead + "985学校?"
                questions.append(question43)
            if (score >= 620 and score < 660):
                question43 = questionhead + "985学校?"
                question44 = questionhead + "211学校?"
                questions.append(question43)
                questions.append(question44)
            if (score < 620 and score >= 590):
                question43 = questionhead + "211学校?"
                question44 = questionhead + "一本学校?"
                questions.append(question43)
                questions.append(question44)
            if(score < 590):
                question43 = questionhead + "一本学校？"
                questions.append(question43)
    return render(request,'KgInfoToQuestion.html',{'questions':questions})


def QuestionsIntoAnswer(request):
    question=request.POST.get('question')
    ProvinceID=Provinces.objects.filter(provinceName="江苏")[0].provinceID
    collegelist=Colleges.objects.filter(Q(provinceID_id=ProvinceID)&Q(project985=1)).distinct()
    print(collegelist)
    return render(request,'KgInfoAnswers.html',{'question':question,'collegelist':collegelist})

def MapVisualization(request):
    return render(request, 'MapVisualization.html')

def get_data_985(provinceID):
    list_985 = []
    count_985 = Colleges.objects.filter(provinceID=provinceID, project985=True).aggregate(Count('collegeID'))
    list_985.append(count_985['collegeID__count'])
    return list_985

def get_data_211(provinceID):
    list_211 = []
    count_211 = Colleges.objects.filter(provinceID=provinceID, project211=True).aggregate(Count('collegeID'))
    list_211.append(count_211['collegeID__count'])
    return list_211




#以下函数通过本地测试                                #选择要调用的可视化函数
def ChooseFunction(request):                       
    question = request.POST.get('question')
    question = str(question)
    #首先判断选填内容是否填了
    #tprovince = request.POST.get('Tprovince')
    #tmajor = request.POST.get('Tmajor')            #tprovince/tmajor从前端传回

    tprovince = "all"
    tmajor = "all"

    questionModelList = []
    similarity = []
    #1.两个选填的都没填
    if(tprovince == "all" and tmajor == "all"):
        question11 = "**省*科**分冲一冲能上什么学校？"
        question12 = "**省*科**分稳一稳能上什么学校？"
        question13 = "**省*科**分保一保能上什么学校？"
        question14 = "**省*科**分能上什么/985学校/211学校/本科学校?"
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
        question14 = "***省大学在**省的分数线排名？"
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




    return render(request, 'KgInfoAnswers.html', {})






def GetCollegeMinScore(collegeid, provinceid, categoryid, year):              #获得学校在某个省文科/理科某一年的最低录取分数
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


#以下函数通过本地测试
def QuestionsIntoAnswer11(request):               #**省*科**分冲一冲能上什么学校？
    question = request.POST.get('question')
    #score = request.POST.get('score')
    #province = request.POST.get('province')
    #category = request.POST.get('category')      #question/score/province/categry从前端传回

    province = "江苏"
    category = "理科"
    score = 360

    #获得provinceid和categoryid
    provinceid = Provinces.objects.filter(provinceName = province)[0].provinceID
    categoryid = Category.objects.filter(categoryname = category)[0].categoryID

    AllCollegelist = Colleges.objects.filter().distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score and collegescore <= score + 20):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request,'KgInfoAnswers.html',
                  {'question':question, 'collegelist':collegelist, 'collegeMinScorelist':collegeMinScorelist})



def QuestionsIntoAnswer12(request):              #**省*科**分稳一稳能上什么学校？
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')      #question/score/province/categry从前端传回

    # 获得provinceid和categoryid
    provinceid = Provinces.objects.filter(provinceName=province)[0].provinceID
    categoryid = Category.objects.filter(categoryname=category)[0].categoryID

    AllCollegelist = Colleges.objects.filter().distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 10 and collegescore <= score + 10):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request, 'KgInfoAnswers.html',
                  {'question': question, 'collegelist': collegelist, 'collegeMinScorelist': collegeMinScorelist})



def QuestionsIntoAnswer13(request):              #**省*科**分保一保能上什么学校？
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')      #question/score/province/categry从前端传回

    # 获得provinceid和categoryid
    provinceid = Provinces.objects.filter(provinceName=province)[0].provinceID
    categoryid = Category.objects.filter(categoryname=category)[0].categoryID

    AllCollegelist = Colleges.objects.filter().distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 20 and collegescore <= score):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request, 'KgInfoAnswers.html',
                  {'question': question, 'collegelist': collegelist, 'collegeMinScorelist': collegeMinScorelist})



def QuestionsIntoAnswer14(request):               #**省*科**分能上什么/985学校/211学校/本科学校?
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')       #question/score/province/categry从前端传回

    # 获得provinceid和categoryid
    provinceid = Provinces.objects.filter(provinceName=province)[0].provinceID
    categoryid = Category.objects.filter(categoryname=category)[0].categoryID

    if(question.find("985") != -1):
        AllCollegelist = Colleges.objects.filter(project985=1).distinct()
    elif (question.find("211") != -1):
        AllCollegelist = Colleges.objects.filter(project211=1).distinct()
    else:
        AllCollegelist = Colleges.objects.filter().distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 15 and collegescore <= score + 15):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request, 'KgInfoAnswers.html',
                  {'question': question, 'collegelist': collegelist, 'collegeMinScorelist': collegeMinScorelist})



def QuestionsIntoAnswer21(request):               #**省*科**分冲一冲能上***省的什么学校？
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')
    tprovince = request.POST.get('Tprovince')     #tprovince/question/score/province/categry从前端传回

    #province = "江苏"
    #tprovince = "江苏"
    #category = "理科"
    #score = 360

    provinceid = Provinces.objects.filter(provinceName = province)[0].provinceID
    categoryid = Category.objects.filter(categoryname = category)[0].categoryID
    tprovinceid = Provinces.objects.filter(provinceName = tprovince)[0].provinceID  #目标省份的id


    AllCollegelist = Colleges.objects.filter(provinceID_id = tprovinceid).distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score and collegescore <= score + 20):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request,'KgInfoAnswers.html',
                  {'question':question, 'collegelist':collegelist, 'collegeMinScorelist':collegeMinScorelist})



def QuestionsIntoAnswer22(request):               #**省*科**分稳一稳能上***省的什么学校？
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')
    tprovince = request.POST.get('Tprovince')     #Tprovince/question/score/province/categry从前端传回

    #获得provinceid、categoryid和tprovinceid
    provinceid = Provinces.objects.filter(provinceName = province)[0].provinceID
    categoryid = Category.objects.filter(categoryname = category)[0].categoryID
    tprovinceid = Provinces.objects.filter(provinceName = tprovince)[0].provinceID  #目标省份的id


    AllCollegelist = Colleges.objects.filter(provinceID_id = tprovinceid).distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 10 and collegescore <= score + 10):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request,'KgInfoAnswers.html',
                  {'question':question, 'collegelist':collegelist, 'collegeMinScorelist':collegeMinScorelist})



def QuestionsIntoAnswer22(request):                #**省*科**分稳一稳能上***省的什么学校？
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')
    tprovince = request.POST.get('Tprovince')      #Tprovince/question/score/province/categry从前端传回

    provinceid = Provinces.objects.filter(provinceName = province)[0].provinceID
    categoryid = Category.objects.filter(categoryname = category)[0].categoryID
    tprovinceid = Provinces.objects.filter(provinceName = tprovince)[0].provinceID  #目标省份的id


    AllCollegelist = Colleges.objects.filter(provinceID_id = tprovinceid).distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 10 and collegescore <= score + 10):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request,'KgInfoAnswers.html',
                  {'question':question, 'collegelist':collegelist, 'collegeMinScorelist':collegeMinScorelist})



def QuestionsIntoAnswer23(request):                #**省*科**分保一保能上***省的什么学校？
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')
    tprovince = request.POST.get('Tprovince')      #Tprovince/question/score/province/categry从前端传回

    provinceid = Provinces.objects.filter(provinceName = province)[0].provinceID
    categoryid = Category.objects.filter(categoryname = category)[0].categoryID
    tprovinceid = Provinces.objects.filter(provinceName = tprovince)[0].provinceID  #目标省份的id

    AllCollegelist = Colleges.objects.filter(provinceID_id = tprovinceid).distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 20 and collegescore <= score):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request,'KgInfoAnswers.html',
                  {'question':question, 'collegelist':collegelist, 'collegeMinScorelist':collegeMinScorelist})



def QuestionsIntoAnswer24(request):                #***省大学在**省**科分数线排名？
    question = request.POST.get('question')
    province = request.POST.get('province')
    tprovince = request.POST.get('Tprovince')
    category = request.POST.get('category')
    provinceid = Provinces.objects.filter(provinceName = province)[0].provinceID
    categoryid = Category.objects.filter(categoryname = category)[0].categoryID
    tprovinceid = Provinces.objects.filter(provinceName = tprovince)[0].provinceID  # 目标省份的id

    AllCollegelist = Colleges.objects.filter(provinceID_id = tprovinceid).distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        collegeMinScorelist.append(collegescore)
        collegelist.append(i)
    print(collegelist)
    return render(request,'KgInfoAnswers.html',
                  {'question':question, 'collegelist':collegelist, 'collegeMinScorelist':collegeMinScorelist})



def QuestionIntoAnswer25(request):                 #**省*科**分能上***省的什么/985学校/211学校/本科学校?
    question = request.POST.get('question')
    score = request.POST.get('score')
    province = request.POST.get('province')
    category = request.POST.get('category')
    tprovince = request.POST.get('Tprovince')      #question/score/province/categry从前端传回
    # 获得provinceid和categoryid
    provinceid = Provinces.objects.filter(provinceName=province)[0].provinceID
    categoryid = Category.objects.filter(categoryname=category)[0].categoryID
    tprovinceid = Provinces.objects.filter(provinceName=tprovince)[0].provinceID  # 目标省份的id

    if(question.find("985") != -1):
        AllCollegelist = Colleges.objects.filter(project985=1, provinceID_id = tprovinceid).distinct()
    elif (question.find("211") != -1):
        AllCollegelist = Colleges.objects.filter(project211=1, provinceID_id = tprovinceid).distinct()
    else:
        AllCollegelist = Colleges.objects.filter(provinceID_id = tprovinceid).distinct()
    collegeMinScorelist = []
    collegelist = []
    for i in AllCollegelist:
        collegeid = i.collegeID
        collegescore = GetCollegeMinScore(collegeid, provinceid, categoryid, 2019)
        if (collegescore >= score - 15 and collegescore <= score + 15):
            collegeMinScorelist.append(collegescore)
            collegelist.append(i)
    print(collegelist)
    return render(request, 'KgInfoAnswers.html',
                  {'question': question, 'collegelist': collegelist, 'collegeMinScorelist': collegeMinScorelist})

