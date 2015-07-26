#Neural Network for AND

class Netz:

	def __init__(self, inp, out):
		self.inp=inp
		self.out=out

	def lassKnacken(self, inp):
		z = len(inp)
		for i in range(z):
			self.inp[i].net= inp[i]
		self.out[0].berechneNet()
		print "berechne Netzausgabe:"
		return(self.out[0].net >= 0)



class Neuron:

	def __init__(self):
		self.edgeIn = []
		self.edgeOut = []
		self.net = 0
		self.bias = 0

	def __init__(self, thresh):
		self.edgeIn = []
		self.edgeOut = []
		self.net = 0
		self.bias = thresh

	def berechneNet(self):
		if(self.edgeIn!=[]):
			sum=0
			for edge in self.edgeIn:
				sum += edge.val*edge.von.net
			self.net = sum-self.bias


class Kante:

	def __init__(self, wert, von, zu):
		self.val = wert
		self.von = von
		self.zu = zu

def verbinde(von, zu, wert):
	kante = Kante(wert, von, zu)
	von.edgeOut.append(kante)
	zu.edgeIn.append(kante)

i1 = Neuron(0)
i2 = Neuron(0)
o1 = Neuron(1.5)

print("Neuronen erstellt")

verbinde(i1,o1,1)
verbinde(i2,o1,1)

print ("Neuronen verbunden")

netz = Netz([i1,i2],[o1])

ausgabe = netz.lassKnacken([1,1])

print ausgabe
