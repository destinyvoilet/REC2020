import torch.nn as nn
import torch
from torch.nn import functional as F
from torch.utils.data import Dataset


class Model1(nn.Module):
    '''
    输入：学生排名、学生经纬度
    输出：大学排名、大学经纬度
    '''

    def __init__(self, input_size=3, hidden1_size=4, hidden2_size=4, hidden3_size=4, output_size=3):
        super(Model1, self).__init__()
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


class Model2(nn.Module):
    '''
    输入：大学经纬度和学生经纬度之差、大学排名
    输出：大学得分
    '''

    def __init__(self, input_size=2, hidden1_size=4, hidden2_size=4, output_size=1):
        super(Model2, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(input_size, hidden1_size), nn.ReLU(True))
        self.layer2 = nn.Sequential(nn.Linear(hidden1_size, hidden2_size), nn.ReLU(True))
        self.layer3 = nn.Sequential(nn.Linear(hidden2_size, output_size))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x


class UniversityDataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe

    def __getitem__(self, index):
        row = self.data.iloc[index]
        x = torch.DoubleTensor([row['stu_rank'], row['stu_long'], row['stu_lati']])
        y = torch.DoubleTensor([row['uni_rank'], row['uni_long'], row['uni_lati']])
        return x, y

    def __len__(self):
        return len(self.data)


class Model1Loss(nn.Module):
    def __init__(self):
        super().__init__()
        self.MSELoss = nn.MSELoss()

    def forward(self, x, y):
        return self.MSELoss(x, y) * 100000