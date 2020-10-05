import torch
import torch.nn as nn
import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from models import Model1, Model2, UniversityDataset, Model1Loss
import torch.optim as optim

def train_humanities():
    raw = pd.read_csv('./aiA/09118120徐浩卿/raw_humanities.csv')
    X = raw[['stu_rank', 'stu_long','stu_lati']]
    y = raw[['uni_rank', 'uni_long','uni_lati']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    trainset = UniversityDataset(X_train.join(y_train))
    testset = UniversityDataset(X_test.join(y_test))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=32, shuffle=False)

    model1 = Model1().double().cuda()
    criterion = Model1Loss().cuda()
    optimizer = optim.SGD(model1.parameters(), lr=0.1)

    for epoch in range(2):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs
            inputs, labels = data
            inputs = inputs.cuda()
            labels = labels.cuda()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model1(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            #for parms in model1.parameters():	
            #    print('-->grad_requirs:',parms.requires_grad,' -->grad_value:',parms.grad)
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                print('[%d, %5d] loss: %.6f' % (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished Training')
    with torch.no_grad(): # when in test stage, no grad
        loss = 0
        for (inputs, labels) in testloader:
            inputs = inputs.cuda()
            labels = labels.cuda()
            out = model1(inputs)
            loss += criterion(out, labels)
    print('Test MSE: {}'.format(loss))
    torch.save(model1.state_dict(),'./aiA/09118120徐浩卿/humanities.mod1')

def train_science():
    raw = pd.read_csv('./aiA/09118120徐浩卿/raw_science.csv')
    X = raw[['stu_rank', 'stu_long','stu_lati']]
    y = raw[['uni_rank', 'uni_long','uni_lati']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    trainset = UniversityDataset(X_train.join(y_train))
    testset = UniversityDataset(X_test.join(y_test))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=2048, shuffle=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=2048, shuffle=False)

    model1 = Model1().double().cuda()
    criterion = nn.MSELoss().cuda()
    optimizer = optim.SGD(model1.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(2):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs
            inputs, labels = data
            inputs = inputs.cuda()
            labels = labels.cuda()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model1(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 10 == 9:    # print every 10 mini-batches
                print('[%d, %5d] loss: %.6f' % (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished Training')
    with torch.no_grad(): # when in test stage, no grad
        loss = 0
        for (inputs, labels) in testloader:
            inputs = inputs.cuda()
            labels = labels.cuda()
            out = model1(inputs)
            loss += criterion(out, labels)
    print('Test MSE: {}'.format(loss))
    torch.save(model1.state_dict(),'./aiA/09118120徐浩卿/science.mod1')

def train_all():
    raw = pd.read_csv('./aiA/09118120徐浩卿/raw_all.csv')
    X = raw[['stu_rank', 'stu_long','stu_lati']]
    y = raw[['uni_rank', 'uni_long','uni_lati']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    trainset = UniversityDataset(X_train.join(y_train))
    testset = UniversityDataset(X_test.join(y_test))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=2048, shuffle=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=2048, shuffle=False)

    model1 = Model1().double().cuda()
    criterion = nn.MSELoss().cuda()
    optimizer = optim.SGD(model1.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(2):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs
            inputs, labels = data
            inputs = inputs.cuda()
            labels = labels.cuda()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model1(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 10 == 9:    # print every 10 mini-batches
                print('[%d, %5d] loss: %.6f' % (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished Training')
    with torch.no_grad(): # when in test stage, no grad
        loss = 0
        for (inputs, labels) in testloader:
            inputs = inputs.cuda()
            labels = labels.cuda()
            out = model1(inputs)
            loss += criterion(out, labels)
    print('Test MSE: {}'.format(loss))
    torch.save(model1.state_dict(),'./aiA/09118120徐浩卿/all.mod1')

def test():
    class model1(nn.Module):
        '''
        输入：学生排名、学生经纬度
        输出：大学排名、大学经纬度
        '''
        def __init__(self, input_size=3, hidden1_size=4, hidden2_size=4, hidden3_size=4, output_size=3):
            super(model1, self).__init__()
            self.layer1 = nn.Sequential(nn.Linear(input_size, hidden1_size), nn.ReLU(True))
            self.layer2 = nn.Sequential(nn.Linear(hidden1_size, hidden2_size), nn.ReLU(True))
            self.layer3 = nn.Sequential(nn.Linear(hidden2_size, hidden3_size), nn.ReLU(True))
            self.layer4 = nn.Sequential(nn.Linear(hidden3_size, output_size))

        def forward(self, x):
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            x = self.layer4(x)
            x = F.softmax(x, dim=0)
            return x


    mymodel1 = model1().double()
    # X 为当前学生数据 (经度，纬度，排名）  00000000000000000000000000000000000000000000000000000000000000
    X_np = np.array([0.4, 0.2, 0.1])  # np.ndarray格式
    X = torch.from_numpy(X_np)  # torch.Tensor格式

    predict_school = mymodel1(X)

    print(predict_school)


    ###################################################################################
    '''
    流程2：对于所有的大学，首先筛选掉那些上不了的，然后在能上的大学中，选与流程1输出大学距离最近的前10所大学
    '''
    schools = [[0.3, 0.3, 0.1], [0.4, 0.1, 0.5], [0.1, 0.5, 0.7]]  # 每个元素是一条大学数据（经度，纬度，排名） 111111111111111111111111111111111111111111
    schools_baseline = [0.01, 0.25, 0.44]  # 每个元素是对应下标大学的最低学生排名  222222222222222222222222222222222222222222222222222
    paiming = X[2]  # 当前的学生排名
    schools_available = []  # 可选的大学
    for i, school in enumerate(schools):
        if paiming <= schools_baseline[i]:
            schools_available.append(schools[i])


    # 现在schools_available中都是可选的大学了。
    # 现在利用流程1的预测大学值，从这些可选大学中再做筛选

    distances = []  # 用于存储每所可选大学与预测大学的距离
    for school in schools_available:
        school = torch.from_numpy(np.array(school))
        distances.append(torch.dist(school, predict_school))

    better_schools_index = list(map(distances.index, heapq.nsmallest(2, distances)))  # 选取可选大学中，与预测大学距离最近的10个大学索引（此处为两个，示范用）
    better_schools = []
    for better_school_index in better_schools_index:
        better_schools.append(schools_available[better_school_index])

    print('better_schools:', better_schools)
    ###################################################################################
    '''
    流程3：对于这20个大学，衡量它们的经纬度和排名因素，计算大学得分
    '''
    class model2(nn.Module):
        '''
        输入：大学经纬度和学生经纬度之差、大学排名
        输出：大学得分
        '''
        def __init__(self, input_size=2, hidden1_size=4, hidden2_size=4, output_size=1):
            super(model2, self).__init__()
            self.layer1 = nn.Sequential(nn.Linear(input_size, hidden1_size), nn.ReLU(True))
            self.layer2 = nn.Sequential(nn.Linear(hidden1_size, hidden2_size), nn.ReLU(True))
            self.layer3 = nn.Sequential(nn.Linear(hidden2_size, output_size))

        def forward(self, x):
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            return x

    mymodel2 = model2().double()
    scores = []  # 存储better大学们的得分
    for school in better_schools:
        school_student_distance = np.sqrt((school[0]-X_np[0])**2+(school[1]-X_np[1])**2)
        school_info = [school_student_distance, school[2]]
        school_info_model = torch.from_numpy(np.array(school_info))
        scores.append(mymodel2(school_info_model))

    print('scores:', scores)
    # 现在scores里都是每个better_school的得分了
    # 我们选取前5个得分最低的大学（越低越好，因为距离越小越好，排名越靠前越好）（此处为两个，示范用）
    best_schools_index = list(map(scores.index, heapq.nsmallest(2, scores)))
    best_schools = []
    for best_school_index in best_schools_index:
        best_schools.append(better_schools[best_school_index])

    print('best_schools:', best_schools)


with open('colle.csv') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

school_rank = [ele[0] for ele in rows]

if __name__=='__main__':
    rank = int(input('请输入你的排名：'))
    prov = input('请输入你的省份：')
    sb_type = input('文理科（文科/理科/all）：')

    data = pd.read_csv('./out.csv')
    data_prov = data[data['province'].isin([prov])]
    data_cate = data_prov[data_prov['category'].isin([sb_type])]
    data_cate['rank'] = data_cate['rank'].astype('int32')

    available_data = data_cate.loc[data_cate['rank']>=rank]
    available_college = available_data['college'].unique()
    available_college_rank = []
    for ele in available_college:
        if ele in school_rank:
            # print(ele)
            available_college_rank.append(school_rank.index(ele))
    available_college_rank.sort()
    available_college_sorted = [school_rank[i] for i in available_college_rank]
    available_college_five_best = available_college_sorted[:5]
    # print(available_college_five_best)
    print("冲一冲：", available_college_five_best[0])
    print("保一保：", available_college_five_best[1], available_college_five_best[2])
    print("稳一稳：", available_college_five_best[3], available_college_five_best[4])






