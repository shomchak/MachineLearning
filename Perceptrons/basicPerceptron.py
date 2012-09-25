import numpy as np

def perceptron(data,target,neurons=1,eta=.1,iterations=100):
    data = addBias(data)
    Ndata = np.shape(data)[0]  
    weights = np.random.rand(neurons,Ndata)
    for i in range(0,iterations):
        for d in range(0,Ndata):
            y = weights.dot(data[d,:].T)
            y = np.where(y>0,1,0)
            for w in range(0,neurons):
                weights[w,:] = weights[w,:] + eta*(target[d,w]-y[w])*data[d,:]
        print "Iteration %i" % i
        print weights
    return weights

def addBias(data):
    for row in data:
        row = np.append(row,-1)
    return data
