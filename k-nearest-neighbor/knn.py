# A generalized k-nearest-neighbor algorithm for data of arbitrary dimension. 
# Invoke makeNodeList(data) with properly formatted data to return a NodeList 
# object. A Node object represents a single data point. Each data point should 
# have format {'parameter1':value1,'parameter2':value2,...,'type':'type_string'}.
# To weight the parameters, feed the NodeList.normalizeData(weights) function
# a dictionary of weights {'parameter1':weight1,'parameter2':weight2,...}. To
# classify an unknown data point, create a Node object with the unclassified 
# data, and run NodeList.classify(unknown,k), where k is the number of neighbors
# desired.



import math,copy

class Node(object):
    'a k-dimensional data point'

    __node_count = 0

    def __init__(self,data,gtype=None):
        self.data = data.copy()
        self.type = gtype
        Node.__node_count += 1
    
    def __str__(self):
        return "%s, %s" % (self.data, self.type)
    
    def nodeCount(self):
        return Node.__node_count

class NodeList(object):
    'a collection of data points'
    
    def __init__(self):
        self.nodes = []
        self.ranges = {}
        self.weights = {}
        self.parameters = []
        self.normalized = False

    def addNode(self,node):
        self.nodes.append(node)
        self.parameters = node.data.keys()
        
        for p in self.parameters:
            self.weights[p] = 1
    
    def printData(self):
        for node in self.nodes:
            print node

    def calculateRanges(self):
        if len(self.nodes) == 0:
            print "List contains no nodes."
            return
        for p in self.parameters:
            p_min = self.nodes[0].data[p]
            p_max = self.nodes[0].data[p]
            for n in self.nodes:
                if n.data[p] < p_min:
                    p_min = n.data[p]
                if n.data[p] > p_max:
                    p_max = n.data[p]
            self.ranges[p] = {'min':p_min,'max':p_max}

    def normalizeData(self, weights):
        self.calculateRanges()
        self.weights = weights
        for w in weights:
            gmin = self.ranges[w]['min']
            gmax = self.ranges[w]['max']
            for n in self.nodes:
                n.data[w] = (n.data[w]-gmin)*float(weights[w])/(gmax-gmin)
            #self.ranges[w]['min'] = 0
            #self.ranges[w]['max'] = weights[w]
        self.normalized = True
        print "Normalized."
    
    def distance(self,a,b):
        distance = 0
        for p in self.parameters:
            distance += math.pow(a.data[p]-b.data[p],2)
        return math.sqrt(distance)

    def classify(self,unknown,k):
        if(k<1 or k>len(self.nodes)):
            print "Invalid K."
            return
        if(self.normalized):
            unknown = copy.deepcopy(unknown)
            for w in self.weights:
                gmin = self.ranges[w]['min']
                gmax = self.ranges[w]['max']
                unknown.data[w] = (unknown.data[w] - gmin)*float(self.weights[w])/(gmax-gmin)
        nodes = self.nodes[::]
        nodes = [x for y,x in sorted(zip([self.distance(a,unknown) for a in nodes],nodes))]
        nodes = nodes[0:k]
        #for n in nodes:
        #    print n
        tally = {}
        for n in nodes:
            tally[n.type]=tally.setdefault(n.type,0)+1
        gtype = max(tally.items(),key=lambda x: x[1])[0]
        print "Data point is of type %s." % gtype

def makeNodeList(data):
    myList = NodeList()
    for element in data:
        node_data = {}
        for parameter in element.keys():
            if parameter != 'type':
                node_data[parameter]=element[parameter]
            else:
                node_type = element[parameter]
        myList.addNode(Node(node_data,node_type))
    return myList

