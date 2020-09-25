import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from models import Model1, Model2, UniversityDataset, Model1Loss
import torch.optim as optim

if __name__ == '__main__':
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
