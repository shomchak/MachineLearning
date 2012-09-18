import math

class Node(object):
    'a k-dimensional data point'

    __node_count = 0

    def __init__(self,data,type):
        self.data = {}
        for key in data:
            self.data[key] = data[key]
        self.type = type
        Node.__node_count += 1
    
    def __str__(self):
        return "%s, %s" % (self.data, self.type)
    
    def nodeCount(self):
        return Node.__node_count

class NodeList(object):
    'a collection of data points'
    
    def __init__(self):
        self.nodes = []

    def addNode(self,node):
        self.nodes.append(node)
        self.parameters = node.data.keys()
        self.weights = {}
        for p in self.parameters:
            self.weights[p] = 1
    
    def printData(self):
        for node in self.nodes:
            print node

    def calculateRanges(self):
        if len(self.nodes) == 0:
            print "List contains no nodes."
            return
        self.ranges = {}
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
            self.ranges[w]['min'] = 0
            self.ranges[w]['max'] = weights[w]
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
        for w in self.weights:
            gmin = self.ranges[w]['min']
            gmax = self.ranges[w]['max']
            unknown.data[w] = (unknown.data[w] - gmin)*float(self.weights[w])/(gmax-gmin)
        nodes = self.nodes[::]
        nodes = [x for y,x in sorted(zip([self.distance(a,unknown) for a in nodes],nodes),reverse = True)]
        nodes = nodes[0:k]
        for n in nodes:
            print n
        tally = {}
        for n in nodes:
            tally[n.type]=tally.setdefault(n.type,0)+1
        gtype = max(tally.items(),key=lambda x: x[1])[0]
        print "Data point is of type %s." % gtype

data = [
    {'rooms': 1, 'area': 350, 'type': 'apartment'},
    {'rooms': 2, 'area': 300, 'type': 'apartment'},
    {'rooms': 3, 'area': 300, 'type': 'apartment'},
    {'rooms': 4, 'area': 250, 'type': 'apartment'},
    {'rooms': 4, 'area': 500, 'type': 'apartment'},
    {'rooms': 4, 'area': 400, 'type': 'apartment'},
    {'rooms': 5, 'area': 450, 'type': 'apartment'},

    {'rooms': 7,  'area': 850,  'type': 'house'},
    {'rooms': 7,  'area': 900,  'type': 'house'},
    {'rooms': 7,  'area': 1200, 'type': 'house'},
    {'rooms': 8,  'area': 1500, 'type': 'house'},
    {'rooms': 9,  'area': 1300, 'type': 'house'},
    {'rooms': 8,  'area': 1240, 'type': 'house'},
    {'rooms': 10, 'area': 1700, 'type': 'house'},
    {'rooms': 9,  'area': 1000, 'type': 'house'},

    {'rooms': 1, 'area': 800,  'type': 'flat'},
    {'rooms': 3, 'area': 900,  'type': 'flat'},
    {'rooms': 2, 'area': 700,  'type': 'flat'},
    {'rooms': 1, 'area': 900,  'type': 'flat'},
    {'rooms': 2, 'area': 1150, 'type': 'flat'},
    {'rooms': 1, 'area': 1000, 'type': 'flat'},
    {'rooms': 2, 'area': 1200, 'type': 'flat'},
    {'rooms': 1, 'area': 1300, 'type': 'flat'},
] 

def makeNodeList(data):
    myList = NodeList()
    for element in data:
        node_data = {'rooms':element['rooms'],'area':element['area']}
        node_type = element['type']
        myList.addNode(Node(node_data,node_type))
    return myList
