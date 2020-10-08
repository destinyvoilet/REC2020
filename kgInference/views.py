from django.http import HttpResponse
from django.shortcuts import render
from ormDesign.models import *
import Levenshtein
from django.db.models import Max,Min,Count,Sum,Avg
import math
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from matplotlib.pyplot import MultipleLocator


# Create your views here.
#主页
def helloworld(request):
    majorlist = Firstlevel.objects.values_list('firstlevelName', flat=True).distinct()
    provincelist = Provinces.objects.values_list('provinceName', flat=True).distinct()
    return render(request, 'KgI_index.html', {'majorlist': majorlist, 'provincelist': provincelist})

#Get certain major scores in different univ. and rank them  信息统计组数据需求

#大学地图可视化
def MapVisualization(request):
    return render(request,'map.html',)

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


    












#输入推荐学校，得到学校近三年的录取分数，录取位次和变化趋势
def getInfoOfUniv(college,pID,cID,major="all"):
    #参数为学校ID，省份ID（整数1-34），科类ID（整数1-3）
    scoreList=[]
    rankList=[]
    for _i in range(2017,2020):
        result1=Majors.objects.filter(collegeID=college,
                                provinceID=pID,
                                categoryID=cID,
                                year=_i,
                                majorName__contains=major,)   #模糊查询
        if(result1.exists()):
            score=result1[0].minScore
        else:
            score=0
        scoreList.append(score)
        result2=Rankings.objects.filter(score=score,
                                    provinceID=pID,
                                    categoryID=cID,
                                    year=_i,)
        if(result2.exists()):
            rank=result2[0].rank
        else:
            rank=0
        
        rankList.append(rank)
        
    return scoreList,rankList

def drawPicture(List,name):
    years=[2017,2018,2019]
    plt.xlabel('year')
    plt.ylabel(name)
    plt.plot(years,List,linewidth=3, color='b', marker='o',
         markerfacecolor='blue', markersize=5)
    
    x_major_locator=MultipleLocator(1)   #设置x坐标轴的坐标间隔为1
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    for _, score in zip(years, List):
        plt.text(_, score, score, ha='center', va='bottom', fontsize=10)
    #将生成的图表返回到前端
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    plt.close()
    
    return src

def CollegeInfoGraphs(request):
    categoryDict={"文科":1,"理科":2,"综合":3}
    zeroList=[0,0,0]
    src1=drawPicture(zeroList,"score")
    src2=drawPicture(zeroList,"rank")
    if(request.method=="POST"):
        college = request.POST.get("college")
        category = request.POST.get("category")
        province=request.POST.get("province")
        provinceID=Provinces.objects.get(provinceName=province).provinceID
        collegeID=Colleges.objects.get(collegeName=college).collegeID
    
        scoreList,rankList=getInfoOfUniv(collegeID,provinceID,categoryDict[category])
        src1=drawPicture(scoreList,"score")
        src2=drawPicture(rankList,"rank")
        text1="图1：近三年"+college+"录取分数线变化"
        text2="图2：近三年"+college+"录取位次变化"
        return render(request,"CollegeInfoGraphs.html",{"src1":src1,"src2":src2,"text1":text1,"text2":text2})
    else:
        return render(request,"CollegeInfoGraphs.html",{"src1":src1,"src2":src2})


def MajorInfoGraphs(request):
    categoryDict={"文科":1,"理科":2,"综合":3}
    zeroList=[0,0,0]
    src1=drawPicture(zeroList,"score")
    src2=drawPicture(zeroList,"rank")
    if(request.method=="POST"):
        college = request.POST.get("college")
        category = request.POST.get("category")
        province=request.POST.get("province")
        majorName=request.POST.get("majorName")
        provinceID=Provinces.objects.get(provinceName=province).provinceID
        collegeID=Colleges.objects.get(collegeName=college).collegeID
    
        scoreList,rankList=getInfoOfUniv(collegeID,provinceID,categoryDict[category],majorName)
        src1=drawPicture(scoreList,"score")
        src2=drawPicture(rankList,"rank")
        text1="图1：近三年"+college+majorName+"专业录取分数线变化"
        text2="图2：近三年"+college+majorName+"专业录取位次变化"
        return render(request,"MajorInfoGraphs.html",{"src1":src1,"src2":src2,"text1":text1,"text2":text2})
    else:
        return render(request,"MajorInfoGraphs.html",{"src1":src1,"src2":src2})


#输入考生省份ID，展示本省及相邻省份的双一流院校
def getTopUnivOfNeighbors(pID):
    #存储相邻省份的字典
    Regions={1:[17,25,2,10,5,21,28,16],
             2:[17,25],
             3:[24,29],
             4:[16,28,13,9],
             5:[34,9,1,21,27,33,30,31],
             6:[30,33,15,20],
             7:[8,24,3],
             8:[7,24,3],
             9:[4,13],
             10:[1,34,17,25,2.5],
             11:[21,22,28,13,19,24],
             12:[34,23],
             13:[4,9,28,11,19],
             14:[27,22,29,32,33],
             15:[6,20,32,33,20],
             16:[17,25,2,1,4,9,28],
             17:[16,25,1,2,10,18,34],
             18:[23,34,17,25,2],
             19:[13,11,24,26],
             20:[30,15,6],
             21:[1,5,22,27,28,11],
             22:[11,14,21,27,14,29],
             23:[12,18,34],
             24:[19,11,22,29,3,7,8],
             25:[17,2],
             26:[19,24],
             27:[21,22,33,5,14],
             28:[4,16,13,9,1,21,11],
             29:[3,24,22,14,32],
             30:[34,31,5,33,6,20],
             31:[34,5,30],
             32:[33,14,29,15],
             33:[15,32,6,30,5,27,14],
             34:[30,31,5,10,17,25,2,18,23,12]}
    topDict={}
    Neighbors=Regions[pID]
    Neighbors.append(pID)
    for ID in Neighbors:
        pName=Provinces.objects.get(provinceID=ID).provinceName
        tops=Colleges.objects.filter(provinceID=ID,top=True)
        if(tops.exists()):
            topList=[]
            for top in tops:
                topList.append(top.collegeName)
            topDict[pName]=topList
        
    return topDict

def DisplayTopUnivOfNeighbors(request):
    if(request.method=="POST"):
        province=request.POST.get("province")
        provinceID=Provinces.objects.get(provinceName=province).provinceID
        
        topDict=getTopUnivOfNeighbors(provinceID)
        
        return render(request,"TopUnivOfNeighbors.html",{"topDict":topDict})
    else:
        return render(request,"TopUnivOfNeighbors.html")

#高考招生百分比
def getPercent(request):
    provinceNum = [[863000, 983000, 1084000], [57000, 55000, 56000], [57000, 58000, 59000], [330000, 330000, 339000],
                   [319000, 319000, 325900], [46000, 42000, 57000], [float('inf'), float('inf'), float('inf')],
                   [float('inf'), float('inf'), float('inf')], [51000, 50000, 50000], [317000, 305000, 314000],
                   [365000, 380000, 421000], [188000, 169000, 204000], [291000, 306000, 314000], [412000, 441000, 458000],
                   [28500, 25300, 27600], [583000, 592000, 559900], [436000, 486000, 559600], [208000, 185000, 244000],
                   [188000, 200000, 207800], [184000, 207000, 220900], [362000, 374000, 384000], [411000, 452000, 500000],
                   [143000, 150000, 162700], [757000, 758000, 768000], [60000, 63000, 59000], [float('inf'), float('inf'), float('inf')],
                   [247000, 250000, 264000], [499000, 499000, 513000], [412000, 400000, 460000], [285000, 273000, 218000],
                   [69000, 69000, 71700], [293000, 300000, 326000], [583000, 620000, 650000], [198000, 195000, 199000]]


    percent2017 = []
    percent2018 = []
    percent2019 = []

    #province = request.POST.get('province')
    category = request.POST.get('category')
    college = request.POST.get('college')

    #provinceid = Provinces.objects.filter(provinceName=province)[0].provinceID
    categoryid = Category.objects.filter(categoryname=category)[0].categoryID
    collegeid = Colleges.objects.filter(collegeName=college)[0].collegeID

    for pid in range(1, 35):
        objectList1 = Majors.objects.filter(provinceID=pid,
                                            categoryID=categoryid,
                                            collegeID=collegeid)
        scoreDict = {'2017': [], '2018': [], '2019': []}
        for item in objectList1:
            if item.year == 2017:
                scoreDict['2017'].append(item.minScore)
            elif item.year == 2018:
                scoreDict['2018'].append(item.minScore)
            else:
                scoreDict['2019'].append(item.minScore)

        scoreList = []
        for k, v in scoreDict.items():
            if v:
                scoreList.append(min(v))
            if not v:
                scoreList.append(0)

        

        objectList2 = Rankings.objects.filter(provinceID=pid,
                                              categoryID=categoryid)


        rankList = [0, 0, 0]
        for item in objectList2:
            if item.year == 2017 and item.score == scoreList[0]:
                rankList[0] = item.rank
            elif item.year == 2018 and item.score == scoreList[1]:
                rankList[1] = item.rank
            elif item.year == 2019 and item.score == scoreList[2]:
                rankList[2] = item.rank

        

        total_num = provinceNum[pid - 1]
        percent2017.append(rankList[0] / total_num[0])
        percent2018.append(rankList[1] / total_num[1])
        percent2019.append(rankList[2] / total_num[2])

    percent = []
    percent.append(percent2017)
    percent.append(percent2018)
    percent.append(percent2019)
    provinceList = Provinces.objects.values_list('provinceName', flat=True).distinct()
    #AllCollegelist = Colleges.objects.filter().distinct()
    
    year=2017
    for i in range(3):
        x = [i for i in range(len(provinceList))]
        width = 0.2
        index = np.arange(len(provinceList))

        for xx, yy in zip(x, percent[i]):
            plt.text(xx, yy + 2, str(yy), ha='center')
        figsize = (20, 10)

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.bar(index, percent[i], width, color="#87CEFA")

        plt.ylabel('percent', fontsize=20)
        plt.xlabel('provinces', fontsize=20)
        
        figname='各省招生位次/人数比'
        plt.xticks(rotation=-45)
        plt.title(str(year)+'年'+college+figname)
        year=year+1
        plt.xticks(index, provinceList, fontsize=10)
        plt.yticks(fontsize=15)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)
        # filepath = "D:\软件实践\rec2020\static\images"+ "\\" + filename
        plt.savefig('./static/images/Percent' + str(i) + '.png', dpi=400)

    return render(request, 'KgI_getPercent.html')