import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from models import Model1, Model2, UniversityDataset
import torch.optim as optim

if __name__=='__main__':
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
