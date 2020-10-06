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



