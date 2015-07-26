#from pybrain.tools.shortcuts import buildNetwork
#from pybrain.datasets import SupervisedDataSet
#from pybrain.supervised.trainers import BackpropTrainer
#from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer

###################################################################################

def StrToBoard(string):
    ret = [[],[],[],[],[],[]]
    for i in range(7):
        for j in range(6):
            z = 5-j+6*i
            ret[j].append(" " if string[z]=="b" else string[z])
    return [ret, string[42]]

def displayStr(string):
    display_board(StrToBoard(string)[0])


def list4NN(string):
	# unlisted
	# A= [[1,2],[3,4]] -> A= [1,2,3,4]
	# sum(StrToBoard(string)[0])
    ret = []
    for i in range(7):
        for j in range(6):
            z = 5-j+6*i
            ret.append(0 if string[z]=="b" else (-1 if string[z]=="o" else 1))
    target = 0 if string[42]=="b" else (-1 if string[42]=="o" else 1)
    return [ret, target]

def board2NN(board):
    tmp = np.array(board)
    tmp = tmp.T
    tmp = tmp.tolist()
    tmp = sum(tmp,[])
    tmp = [1 if x=="O" else (-1 if x=="X" else 0) for x in tmp]

def NN2board(li):
    tmp = ["X" if x==1 else ("O" if x==-1 else " ") for x in li]
    tmp = np.array(tmp)
    tmp.shape = (7,6)
    tmp = tmp.T
    return tmp


###################################################################################


'''
net = buildNetwork(42, 40, 1, bias=True, hiddenclass=TanhLayer, outclass=TanhLayer)

ds = SupervisedDataSet(42, 1)

trainer = BackpropTrainer(net, ds, learningrate=0.35, momentum=0.7)

fobj = open("database.txt")
counter=0
for line in fobj:
	#print line.rstrip()
    #displayStr(line.rstrip())
	tmp = list4NN(line.rstrip())
	ds.addSample(tmp[0],tmp[1])
	# counter for stopping if its too long
	#counter = counter+1
	#if counter > 1000:
	#	break
fobj.close()

print "Got the Data!"

#trainer.trainEpochs(epochs=40)
trainer.train()
#trainer.trainUntilConvergence()

print "Trained Sir!"
'''

