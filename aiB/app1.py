from models import Clustering,get_dataset,criterion,readFronSqllite
from view import get_college_name,get_dic,clusterFromData,center,cen,newcen,newcen1,datasetCOLLEGE
import matplotlib.pyplot as plt
from PIL import Image,ImageFont,ImageDraw


###app1:根据用户输入的信息，显示三年的分段图和他所处的位置情况
###延申：根据此分段显示当年他在哪个分段，同时根据分段推荐大学

print('输入省份id，文理科id，分数')

###aa bb cc为从post接受的参数，用以替换a,b,c
def application1(aa,bb,cc):
    a = 0
    b = 0
    c = 0
    d = ''
    a = input('输入省份id：')
    b = input('文理id：')
    c = input('分数：')

    # d=input('用户id：')
    user = [int(a), int(b), int(c)]  # 省id,,理科1文科2综合3,分
    print(user)
    # userid=str(d)
    myinput = user  # 文理，省，分数
    # （2，2017，1）（2，2018，1）（2，2019，1）

    # user[2]
    dataset = get_dataset()

    testdata = []
    for item in dataset:
        if (item[0] == (user[0], 2017, user[1])):
            for items in item:
                testdata.append(items)
    testdata.remove((user[0], 2017, user[1]))

    ######判断此年数据是否缺失(是否为空表)
    if len(testdata) == 0:
        a = 0
    else:
        a = 1

    x = [d[0] for d in testdata]
    y = [d[1] for d in testdata]

    ######去除数据中的负数人数以及对应的分数
    ###为什么数据里面会这样
    for items in y:
        if (items < 0):
            num = y.index(items)
            del x[num]
            del y[num]

    dataset1 = get_dataset()
    testdata1 = []
    for item in dataset1:
        if (item[0] == (user[0], 2018, user[1])):
            for items in item:
                testdata1.append(items)
    testdata1.remove((user[0], 2018, user[1]))

    ######判断数据缺失
    if len(testdata1) == 0:
        b = 0
    else:
        b = 1

    x1 = [d[0] for d in testdata1]
    y1 = [d[1] for d in testdata1]
    ######去除数据中的负数人数以及对应的分数
    for items in y1:
        if (items < 0):
            num = y1.index(items)
            del x1[num]
            del y1[num]

    dataset2 = get_dataset()
    testdata2 = []
    for item in dataset2:
        if (item[0] == (user[0], 2019, user[1])):
            for items in item:
                testdata2.append(items)
    testdata2.remove((user[0], 2019, user[1]))

    ######判断数据缺失
    if len(testdata2) == 0:
        c = 0
    else:
        c = 1

    x2 = [d[0] for d in testdata2]
    y2 = [d[1] for d in testdata2]

    ######去除数据中的负数人数以及对应的分数
    for items in y2:
        if (items < 0):
            num = y2.index(items)
            del x2[num]
            del y2[num]

    ###
    if a == 1:
        belong = Clustering(testdata, 5)
        colorlist = []
        for items in belong[1]:
            if (items == 0):
                colorlist.append('grey')
            if (items == 1):
                colorlist.append('gold')
            if (items == 2):
                colorlist.append('turquoise')
            if (items == 3):
                colorlist.append('plum')
            if (items == 4):
                colorlist.append('lawngreen')
    else:
        print("2017年数据缺失")

    if b == 1:
        belong1 = Clustering(testdata1, 5)
        colorlist1 = []
        for items in belong1[1]:
            if (items == 0):
                colorlist1.append('grey')
            if (items == 1):
                colorlist1.append('gold')
            if (items == 2):
                colorlist1.append('turquoise')
            if (items == 3):
                colorlist1.append('plum')
            if (items == 4):
                colorlist1.append('lawngreen')
    else:
        print("2018年数据缺失")

    if c == 1:
        belong2 = Clustering(testdata2, 5)
        colorlist2 = []
        for items in belong2[1]:
            if (items == 0):
                colorlist2.append('grey')
            if (items == 1):
                colorlist2.append('gold')
            if (items == 2):
                colorlist2.append('turquoise')
            if (items == 3):
                colorlist2.append('plum')
            if (items == 4):
                colorlist2.append('lawngreen')
    else:
        print("2019年数据缺失")

    if a == 1:
        plt.figure()
        plt.title('2017 scores distribution')
        plt.xlabel('scores')
        plt.ylabel('numbers of students')
        plt.bar(x, y, color=colorlist, alpha=0.8)
        plt.bar(user[2], y, color='red', alpha=0.8)
        picid = 'pic1.jpg'
        plt.savefig(picid)
    else:
        text = "2017年数据缺失"
        font = ImageFont.truetype("font.ttf", 18)
        lines = []
        line = "2017年数据缺失"
        lines.append(line)
        line_height = font.getsize(text)[1]
        img_height = line_height * (2)
        im = Image.new("RGB", (200, img_height), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        x, y = 5, 5
        for line in lines:
            dr.text((x, y), line, font=font, fill="#000000")
            y += line_height
        im.save("pic1.jpg")

    if b == 1:
        plt.figure()
        plt.title('2018 scores distribution')
        plt.xlabel('scores')
        plt.ylabel('numbers of students')
        plt.bar(x1, y1, color=colorlist1, alpha=0.8)
        plt.bar(user[2], y1, color='red', alpha=0.8)
        picid = 'pic2.jpg'
        plt.savefig(picid)
    else:
        text = "2018年数据缺失"
        font = ImageFont.truetype("font.ttf", 18)
        lines = []
        line = "2018年数据缺失"
        lines.append(line)
        line_height = font.getsize(text)[1]
        img_height = line_height * (2)
        im = Image.new("RGB", (200, img_height), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        x, y = 5, 5
        for line in lines:
            dr.text((x, y), line, font=font, fill="#000000")
            y += line_height
        im.save("pic2.jpg")

    if c == 1:
        plt.figure()
        plt.title('2019 scores distribution')
        plt.xlabel('scores')
        plt.ylabel('numbers of students')
        plt.bar(x2, y2, color=colorlist2, alpha=0.8)
        plt.bar(user[2], y2, color='red', alpha=0.8)
        picid = 'pic3.jpg'
        plt.savefig(picid)
    else:
        text = "2019年数据缺失"
        font = ImageFont.truetype("font.ttf", 18)
        lines = []
        line = "2019年数据缺失"
        lines.append(line)
        line_height = font.getsize(text)[1]
        img_height = line_height * (2)
        im = Image.new("RGB", (200, img_height), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        x, y = 5, 5
        for line in lines:
            dr.text((x, y), line, font=font, fill="#000000")
            y += line_height
        im.save("pic3.jpg")

    # 最后print出聚类边界和每一个分数的标签，并画出一个分段聚类彩色图
    # 2020.9

    ###下面进行学校推荐

    collegelist = []
    for d in datasetCOLLEGE:
        if d[0:2] == myinput[0:2]:
            collegelist.append(d)

    for e in newcen1:
        if e[0] == myinput[0] and e[1] == myinput[1]:
            abslist = []
            for i in range(2, 7):
                abslist.append(abs(myinput[2] - e[i]))
            # print(abslist)
            minnum = 1000
            minj = 0
            for j in range(5):
                if abslist[j] < minnum:
                    minj = j
                    minnum = abslist[j]
            target = e[minj + 2]
            str1 = "你属于第" + str(minj + 1) + "分段,"

    for e in collegelist:
        e.append(abs(e[3] - target))
    collegelist.sort(key=lambda x: x[4])
    str2 = "为你推荐的大学是："

    strlist = [str1, str2]

    for i in range(1, 7, 2):
        strlist.append(str(collegelist[i][2]) + ' ')

    # print(strlist)
    strsend = ''
    for items in strlist:
        strsend += items

    print(strsend)

    text = strsend
    font = ImageFont.truetype("font.ttf", 18)
    lines = []
    line = strsend
    lines.append(line)
    line_height = font.getsize(text)[1]
    img_height = line_height * (2)
    im = Image.new("RGB", (900, img_height), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    x, y = 5, 5
    for line in lines:
        dr.text((x, y), line, font=font, fill="#000000")
        y += line_height
    im.save("commandtest.jpg")

    ###将图片输出
    ###在网页上添加文字说明


#测试：
application1(0,0,0)