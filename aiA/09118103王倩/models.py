import torch.nn as nn
from torch.nn import functional as F


class model1(nn.Module):
    '''
    输入：学生排名、学生经纬度
    输出：大学排名、大学经纬度
    '''
    def __init__(self, input_size=3, hidden1_size=4, hidden2_size=4, hidden3_size=4, output_size=3):
        super(model1, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(input_size, hidden1_size), nn.Sigmoid())
        self.layer2 = nn.Sequential(nn.Linear(hidden1_size, hidden2_size), nn.Sigmoid())
        self.layer3 = nn.Sequential(nn.Linear(hidden2_size, hidden3_size), nn.Sigmoid())
        self.layer4 = nn.Sequential(nn.Linear(hidden3_size, output_size))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = F.softmax(x, dim=0)
        return x


class model2(nn.Module):
    '''
    输入：大学经纬度和学生经纬度之差、大学排名
    输出：大学得分
    '''
    def __init__(self, input_size=2, hidden1_size=4, hidden2_size=4, output_size=1):
        super(model2, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(input_size, hidden1_size), nn.Sigmoid())
        self.layer2 = nn.Sequential(nn.Linear(hidden1_size, hidden2_size), nn.Sigmoid())
        self.layer3 = nn.Sequential(nn.Linear(hidden2_size, output_size))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x
