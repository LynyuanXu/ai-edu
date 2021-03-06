# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math

from LossFunction import * 
from Level0_TwoLayerNet import *
from DataReader import * 
from WeightsBias import *
from GDOptimizer import *

x_data_name = "X8.dat"
y_data_name = "Y8.dat"

def ShowResult(net, X, Y, title, wb1, wb2):
    # draw train data
    plt.plot(X[0,:], Y[0,:], '.', c='b')
    # create and draw visualized validation data
    TX = np.linspace(0,1,100).reshape(1,100)
    dict_cache = net.forward(TX, wb1, wb2)
    TY = dict_cache["Output"]
    plt.plot(TX, TY, 'x', c='r')
    plt.title(title)
    plt.show()


def train(init_method):
    dataReader = DataReader(x_data_name, y_data_name)
    XData,YData = dataReader.ReadData()
    X = dataReader.NormalizeX(passthrough=True)
    Y = dataReader.NormalizeY()
    
    n_input, n_hidden, n_output = 1, 4, 1
    eta, batch_size, max_epoch = 0.5, 10, 30000
    eps = 0.001

    params = CParameters(n_input, n_hidden, n_output,
                         eta, max_epoch, batch_size, eps, 
                         init_method,
                         OptimizerName.SGD)

    loss_history = CLossHistory()
    net = TwoLayerNet(NetType.Fitting)
    net.train(dataReader, params, loss_history)

    trace = loss_history.GetMinimalLossData()
    print(trace.toString())
    title = loss_history.ShowLossHistory(params)
    ShowResult(net, X, YData, title, trace.wb1, trace.wb2)

if __name__ == '__main__':    
    #train(InitialMethod.Zero)
    #train(InitialMethod.Normal)
    train(InitialMethod.Xavier)
    #train(InitialMethod.MSRA)