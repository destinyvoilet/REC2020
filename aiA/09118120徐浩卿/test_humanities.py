import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from models import Model1, Model2, UniversityDataset
import torch.optim as optim

if __name__=='__main__':
    model1 = Model1().double().cuda()
    criterion = nn.MSELoss().cuda()

    model1.load_state_dict(torch.load('./aiA/09118120徐浩卿/humanities.mod1'))

    with torch.no_grad(): # when in test stage, no grad
        correct = 0
        total = 0
        for (imgs, labels) in testLoader:
            imgs = imgs.to(device)
            labels = labels.to(device)
            out = model(imgs)
            _, pre = torch.max(out.data, 1)
            total += labels.size(0)
            correct += (pre == labels).sum().item()
        print('Accuracy: {}'.format(correct / total))