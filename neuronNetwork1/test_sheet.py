from network import network

reseau = network()
reseau.setError(0.05)
reseau.setLayer(4)
reseau.printData()
reseau.addAllNeuron([3,5,7,3])
reseau.createNetwork()


reseau.learn([1,0,1],[1,1,0])
reseau.learn([1,0,0],[0,0,0])
reseau.learn([0,0,0],[1,0,1])
reseau.learn([1,1,1],[1,1,1])
reseau.printAll()