from functions import sigmoide, tangente
class network:
    
    def __init__(self, name='Unknown', learn ='sigmoide', error=0.001):
        """
        # We initialize the network with for parameters :
            - a name with an insightful title
            - an activation function
            - the error during the learning
        """
        self.name = name
        if 'tangente' == str.lower(learn):
            self.fun_learn = tangente
            self.name_fun_learn = 'tangente'
        else:
            self.fun_learn = sigmoide
            self.name_fun_learn = 'sigmoide'
        self.error = error # error during learning
        self.layer = [] # table of layers with the numbers of neurons by layers
        self.link = [] # tableau with all weights
        self.values = [] # table with differents values of neurons
        self.control = 0 # controller to stop the adding of layer/neuron after the initialization


        """
        # Getters and setters
        """

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def getError(self):
        return self.error

    def setError(self,nb):
        if (nb > 0):
            self.error = nb

    def setFunLearn(self, name):
        if 'tangente' == str.lower(name):
            self.fun_learn = tangente
            self.name_fun_learn = 'tangente'
        else:
            self.fun_learn = sigmoide
            self.name_fun_learn = 'sigmoide'

    def getNameFunLearn(self):
        return self.name_fun_learn

    def getData(self):
        return [self.getName(), self.getNameFunLearn(), self.getError(), self.getNbLayer()]

    def getNbLayer(self):
        return len(self.layer)

    def getLastLayer(self):
        return self.values[-1]

    def setLayer(self, value=2):
        """
        # We initialize differents layers of network
        # we have 2 layers at least (input + output)
        """
        if(self.control == 0):
            if(value >= 2):
                for i in range(0, value):
                    self.layer.append(0)
            else:
                print("There is 2 layers at least")
        else:
            print("The network is already created, you can't edit it anymore")


    def addLayer(self, pos):
        """
        # function which permites us to add a new layer
        """
        if(self.control == 0):
            if (pos >=0 and pos < len(self.layer)):
                self.layer.insert(pos,0)
            else:
                print("You can add a layer in the range [0,", len(self.layer), "]")
        else:
            print("The network is already created, you can't edit it anymore")


    def addNeuron(self, layer, nb=1):
        """
        # function which permites us to add at least one neuron on a specific layer
        """
        if(self.control == 0):
            if layer >=0 and layer <len(self.layer) and nb > 0:
                self.layer[layer] += nb
        else:
            print("The network is already created, you can't edit it anymore")

    def addAllNeuron(self, tab):
        """
        # function which permites us to add at least one neuron on a specific layer
        """
        if(self.control == 0):
            if (len(tab) == len(self.layer)):
                for i in range(0,len(tab)):
                    self.addNeuron(i, tab[i])
            else:
                print("Your table size has to be ",len(self.layer))
        else:
            print("The network is already created, you can't edit it anymore")


    def createNetwork(self):
        """
        # We initialize all connections between neurons
        # By default, all weights value 0.5
        # We initialize also the table of neurons values to 0
        """
        test = 0
        for j in range(0, len(self.layer)):
            if(self.layer[j] <= 0):
                print("The layer", j , "has to contain at least 1 value")
                test = 1 
        if test != 1:
            if self.control == 0:
                self.control = 1
                for i in range(0, len(self.layer)):
                    add = []
                    add1 = []
                    addValues = []
                    for j in range(0, self.layer[i]):
                        if i != len(self.layer) - 1:
                            for k in range(0,self.layer[i + 1]):
                                add1.append(0.5)
                            add.append(add1)
                            add1 = []
                        addValues.append(0)
                    if i != len(self.layer) - 1:
                        self.link.append(add)
                    self.values.append(addValues)
            else: 
                print("Network already initialized")
        else:
            print("You can't launch the initialization")


    def browse(self, tab):
        """
        # Function which permites us to browse the neuron network
        # In parameters, data to test
        """ 
     
        if self.control == 1:
            if(len(tab) == self.layer[0]):
                for i in range(0, len(tab)):
                    # we stock in the first layer input data
                    self.values[0][i] = tab[i]
                for i in range(1, len(self.values)):
                    for j in range(0, len(self.values[i])):
                        var = 0
                        for k in range(0,len(self.values[i -1])):
                            # we stock the weighted sum for the next neuron
                            var += self.values[i - 1][k] * self.link[i - 1][k][j]
                        self.values[i][j] = self.fun_learn(var)
            else:
                print("The input layer has to contain", self.layer[0], "values")
        else:
               print("Network not initialized")


    def retropropaganda(self, tab):
        """
        # Function which permites us to browse the neuron network
        # In parameters, data to test
        """ 
        if len(tab) == len(self.values[len(self.values) - 1]):
            for i in range(0, len(tab)):
                # we stock in the last layer the difference between the expected value and the real value
                self.values[len(self.values)-1][i] = tab[i] - self.values[len(self.values) -1][i]
            for i in range(len(self.values) - 1 , 0, -1):
                for j in range(0, len(self.values[i - 1])):
                    for k in range(0, len(self.link[i - 1][j])):
                        sum = 0
                        for l in range(0, len(self.values[i - 1])):
                            # we do the weighted sum of the neuron to which points the connection
                            sum += self.values[i -1][l] * self.link[i -1][l][k]
                        sum = self.fun_learn(sum)

                        #we update the connection weight
                        self.link[i - 1][j][k] -= self.getError() * (-1 * self.values[i][k] * sum * (1 - sum) * self.values[i - 1][j])
                for j in range(0, len(self.values[i - 1])):
                    sum = 0
                    for k in range(0, len(self.values[i])):
                        # we update neurons of the next layer according to the error which is retropropaged
                        sum += self.values[i][k] * self.link[i - 1][j][k]
                    self.values[i - 1][j] = sum


    def learn(self, input, output):
        """
        # Function which permites us to learn the network
        # the first parameter represents the set of values to test 
        the second parameter represents the expected result
        """  

        if (self.control == 1):
            if len(input) == self.layer[0] and len(output) == self.layer[len(self.getLastLayer())]:
                self.browse(input)
                self.retropropaganda(output)
            else:
                print("The input layer must contain", self.layer[0], "values \n The output layer must contain ", self.layer[len(self.getLastLayer())])
        else:
            print("Network not initialized")


    
    def printLastLayer(self):
        print(self.values[len(self.values)-1])

    def printData(self):
        tab = self.getData()
        print("Name of the network :", tab[0],
        "\nLearning function :", tab[1],
        "\nLearning error value  :", tab[2],
        "\nNumber of layers :", tab[3])

    def printAll(self):
        print("Values :")
        self.printValues()
        print("\nLink :")
        self.printLink()

    def printLink(self):
        i = 1
        for each in self.link:
            print("Links", i , ":")
            i += 1
            print(each)

    def printValues(self):
        i = 1
        for each in self.values:
            print("Layer", i , ":")
            i += 1
            for k in each:
                print(k)
            print()

    def printLayer(self):
        print(self.layer)