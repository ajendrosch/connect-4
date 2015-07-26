feld = [[' ' for x in range(7)] for x in range(5)]

#1 if there is a winning move, take it
#2 if your opponent has a winning move, take the move first
#3 take the center square over edges and corners
#4 take corner squares over edges
#5 take edges if they are the only thing available

class Spielbaum():
    
    def __init__(self, s1=1, s2=2):
        situation = []
        sp1 = s1
        sp2 = s2
        tiefe = 0
        wert1 = 0
        wert2 = 0
        folgesituationen = []

    def bewerte(self):
        wert1 = bewertesp(self.situation, 1)
        wert2 = bewertesp(self.situation, 2)

    def machbaum(self, feld, t, sp):
        self.tiefe = t
        self.situation = dupl(feld)
        self.letztersp = sp
        self.bewerte()
        if (t>0):
            spielerwechsel = (1 if self.letztersp==2 else 2)
            for i in range(7):
                if checkspalte(feld, i):
                    tmpBaum = Spielbaum()
                    tmpBaum.machbaum(wirfinfeld(dupl(feld),i+1, spielerwechsel), t-1, spielerwechsel)
                    self.folgesituationen.insert(i, tmpBaum)
                else:
                    self.folgesituationen.insert(i,[])
        
    situation = []
    letztersp = 1
    sp1 = 1
    sp2 = 2
    tiefe = 0
    wert1 = 0
    wert2 = 0
    folgesituationen = []

def printfeld(feld):
    for i in range(5):
        print("|",end='')
        for j in range(7):
            print(feld[i][j],end='')
            print("|",end='')
        print()

        
def wirfinfeld(feld, z, char):
    for i in range(4,-1,-1):
        if(feld[i][z-1]==' '):
            feld[i][z-1]=char
            return feld
    return False


def dupl(feld):
    feld2 = [[feld[i][j] for j in range(7)] for i in range(5)]
    return feld2



def checkspalte(feld, i):
    return (True if (feld[4][i]==' ') else False)

# 4 = 1000
# 3 = 10
# 2 = 1
#

def bewertesp(feld, sp):
    vier = check(feld, sp, 4)
    drei = check(feld, sp, 3)
    zwei = check(feld, sp, 2)
    gewichtung = gewichte(feld, sp)
    return (1000*vier+10*drei+zwei)*gewichtung

def check(feld, sp, anz):
    breite = len(feld[0])
    hoehe = len(feld)
    ret = 0
    
    #waagerecht
    for i in range(hoehe):
        tmp = 0
        for j in range(breite):
            if feld[i][j]==sp:
                tmp = tmp + 1
            else:
                tmp = 0
            if tmp>=anz:
                    ret = ret + 1
    #senkrecht
    for i in range(breite):
        tmp = 0
        for j in range(hoehe):
            if feld[j][i]==sp:
                tmp = tmp + 1
            else:
                tmp = 0
            if tmp>=anz:
                    ret = ret + 1

    #schräg rechts
    for i in range(anz-1, hoehe):
        for j in range(0,hoehe):
            try:
                if feld[i-k][k]==sp:
                    tmp = tmp +1
                else:
                    tmp=0
                if tmp>=anz:
                    ret = ret + 1
            except:
                tmp=0
                pass
            
    for i in range(breite):
        for j in range(hoehe):
            pass

    #schräg links

    return ret
#############################################################################################################


#baum = Spielbaum()
#wirfinfeld(feld,1,1)
#baum.machbaum(feld,1)
#for i in range(7):
#	printfeld(baum.folgesituationen[i])
