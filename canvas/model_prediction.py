import pandas as pd
import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from django.conf import settings


####Class for models
class Cnn_model(nn.Module):

    def __init__(self):

        super(Cnn_model, self).__init__()

        # convolutional layer (takes 28x28x1 image tensor)
        self.conv1 = nn.Conv2d(1, 12, 3, padding=1)
        # convolutional layer (takes 12x14x14 tensor)
        self.conv2 = nn.Conv2d(12, 18, 3, padding=1)

        # max pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        # linear layer (18 * 7 * 7 -> 250)
        self.fc1 = nn.Linear(18 * 7 * 7, 250)
        # linear layer (250 -> 10)
        self.fc2 = nn.Linear(250, 10)
        # dropout layer (p=0.25)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        #Sequence of convolutional and max pooling layers
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        # flattening image input
        x = x.view(-1, 18 * 7 * 7)
        # adding dropout layer
        x = self.dropout(x)
        # adding 1st hidden layer, with relu activation function
        x = F.relu(self.fc1(x))
        # adding dropout layer
        x = self.dropout(x)
        # adding 2nd hidden layer
        x = self.fc2(x)
        return x



def predict_pytorch(pixel_array):
    custom_image_scaled_array = (np.array(pixel_array))
    custom_image_scaled_array = custom_image_scaled_array.reshape(28,28)

    list_req = list(list(custom_image_scaled_array.reshape(1,-1))[0])
    req_dict = {}

    for k in range(len(list_req)):
        key = 'pixel'+ str(k)
        req_dict[key] = [list_req[k]]
    new_df = pd.DataFrame(req_dict)

    X = np.array(new_df).reshape(-1,1,28,28)/255

    X = torch.tensor(X,dtype = torch.float32)

    model = Cnn_model()

    model_path = os.path.join(settings.BASE_DIR, 'canvas/cnn_model_pytorch/model.pth')
    model.load_state_dict(torch.load(model_path,map_location=lambda storage, loc: storage))
    model.eval()

    model.cpu()
    X = X.view(1,1,28,28)


    scores = model(X)

    softmax = nn.Softmax(dim=1)
    probabilities = softmax(scores)



    return probabilities[0]
