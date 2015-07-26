import random
import NN2

KI_level = 2

evaluationTable = [[3, 4, 5, 7, 5, 4, 3], 
                  [ 4, 6, 8, 10, 8, 6, 4],
                  [ 5, 8, 11, 13, 11, 8, 5], 
                  [ 5, 8, 11, 13, 11, 8, 5],
                  [ 4, 6, 8, 10, 8, 6, 4],
                  [ 3, 4, 5, 7, 5, 4, 3]]

def evaluateContent(board, player1):
        player2 = "X" if player1=="O" else "O"
        utility = 138
        if check(board, player1, 4) > 0:
            if check(board, player2, 4) > 0:
                return 0
            return 2*utility
        if check(board, player2, 4) > 0:
            return -2*utility
        sum = 0
        for i in [0,1,2,3,4,5]:
            for j in [0,1,2,3,4,5,6]:
                if (board[i][j] == player1):
                    sum += evaluationTable[i][j]
                else:
                    if (board[i][j] == player2):
                        sum -= evaluationTable[i][j]
        return sum
        #return utility + sum

def minimax(board, depth, player, maximizingPlayer=True, alpha=-9999, beta=9999):
    steps = poss_steps(board)
    if depth==0 or steps==[]:
        # IST DAS SO RICHTIG??? ICH MEIN WARUM MUSS ICH DEN PLAYER BEI DER EVALUATION BERÜCKSICHTIGEN
        wert = evaluate(board, player)
        #print "Kind: "+str(wert)
        return [wert,-1]
    if maximizingPlayer:
        #bestValue = -999999
        maxValue = alpha
        bestStep = -1
        next_player = "O" if player=="X" else "X"
        for step in steps:
            insert(board, step, player)
            #print "schritt: " + str(step) + " bei min"
            # QUICK EVALUATION if 4 CONNECTED then no need for further computation
            if check(board, "O", 4) > 0:
                uninsert(board, step, player)
                return [999,step]
            val = minimax(board, depth-1, next_player, False, maxValue, beta)[0]
            uninsert(board, step, player)
            if val > maxValue:
                bestStep= step
                maxValue=val
                #alphabeta ergänzung
                if maxValue >= beta:
                    break
            #bestValue = max(bestValue, val)
            #print "bestVal: " + str(bestValue)
        return [maxValue, bestStep]
    else:
        #bestValue = 999999
        minValue = beta
        bestStep = -1
        next_player = "O" if player=="X" else "X"
        for step in steps:
            insert(board, step, player)
            #print "schritt: " + str(step) + " bei max"
            # QUICK EVALUATION if 4 enemy CONNECTED NO NEED for further computation
            if check(board, "X", 4) > 0:
                uninsert(board, step, player)
                return [-999,step]
            val = minimax(board, depth-1, next_player, True, alpha, minValue)[0]
            uninsert(board, step, player)
            if val < minValue:
                bestStep= step
                minValue=val
                if minValue <= alpha:
                    break
            #bestValue = min(bestValue, val)
            #print "bestVal: " + str(bestValue)
        return [minValue, bestStep]


def poss_steps(board):
    ret = []
    for i in range(len(board[1])):
        if board[0][i]==" ":
            ret.append(i)
    return map(lambda x:x+1, ret)

def evaluate(board, player1):
    #player2 = "X" if player1=="O" else "O"
    # WÄHLE FESTEN PLAYER BEI EVALUATION
    return evaluateContent(board, "O")
    #return (bewertesp(board, player2)-bewertesp(board, player1))

def bewertesp(feld, sp):
    vier = check(feld, sp, 4)
    drei = check(feld, sp, 3)
    zwei = check(feld, sp, 2)
    eins = check(feld, sp, 1)
    #gewichtung = gewichte(feld, sp)
    return (1000*vier+100*drei+10*zwei+eins)

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

    #schräg rechts hoch

    sub=anz-1
    for i in range(hoehe-1,sub-1,-1):
        for j in range(0,breite-sub,1):
            tmp = 0
            for t in range(anz):
                if(feld[i-t][j+t]==sp): tmp = tmp+1
            if tmp == anz: ret = ret + 1

    # for i in range(anz-1, hoehe):
    #     for j in range(0,hoehe):
    #         try:
    #             if feld[i-k][k]==sp:
    #                 tmp = tmp +1
    #             else:
    #                 tmp=0
    #             if tmp>=anz:
    #                 ret = ret + 1
    #         except:
    #             tmp=0
    #             pass
            
    # for i in range(breite):
    #     for j in range(hoehe):
    #         pass

    #schräg links
    for i in range(hoehe-1,sub-1,-1):
        for j in range(breite-1,sub-1,-1):
            tmp = 0
            for t in range(anz):
                if(feld[i-t][j-t]==sp): tmp = tmp+1
            if tmp == anz: ret = ret + 1

    return ret



class MinMaxBaum:

    def __init__(self, feld, tiefe, vater, typ="min"):
        self.Vater = vater
        self.Tiefe = tiefe
        self.Situation = feld
        self.Children = {}
        self.Typ = typ
        self.Wert = 0

    def build(self):
        if(self.Tiefe > 0 and self.Situation != []):
            print "Tiefe:" + str(self.Tiefe)
            symbol="O" if self.Typ=="min" else "X"
            typ= "max" if self.Typ=="min" else "min"
            for i in map(lambda x:x+1, range(7)):
                tree = MinMaxBaum(insert2(self.Situation, i, symbol), self.Tiefe-1, self, typ)
                tree.build()
                self.Children[i]=tree

    def bewerte(self):
        if(self.Situation)!=[]:
            Wert_X = bewertesp(self.Situation, "X")
            Wert_O = bewertesp(self.Situation, "O")
            for i in self.Children:
                self.Children[i].bewerte()


def dupl(feld):
    feld2 = [[feld[i][j] for j in range(7)] for i in range(6)]
    return feld2

def winner(board):
    if check(board, "X",4)>0:
        return "X"
    if check(board, "O",4)>0:
        return "O"
    return ""



def display_board(board):

    print "   1   2   3   4    5   6   7"
    print "1: " + board[0][0] + " | " + board[0][1] + " | " + board[0][2] + " | " + board[0][3] + " | " + board[0][4] + " | " + board[0][5] + " | " + board[0][6] + " | "
    print "  ---+---+---+---+---+---+---"
    print "2: " + board[1][0] + " | " + board[1][1] + " | " + board[1][2] + " | " + board[1][3] + " | " + board[1][4] + " | " + board[1][5] + " | " + board [1][6] + " | "
    print "  ---+---+---+---+---+---+---+"
    print "3: " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + " | " + board[2][3] + " | " + board [2][4] + " | " + board [2][5] + " | " + board [2][6] + " | "
    print "  ---+---+---+---+---+---+---+"
    print "4: " + board[3][0] + " | " + board[3][1] + " | " + board[3][2] + " | " + board[3][3] + " | " + board [3][4] + " | " + board [3][5] + " | " + board [3][6] + " | "
    print "  ---+---+---+---+---+---+---+"
    print "5: " + board[4][0] + " | " + board[4][1] + " | " + board[4][2] + " | " + board[4][3] + " | " + board [4][4] + " | " + board [4][5] + " | " + board [4][6] + " | "
    print "  ---+---+---+---+---+---+---+"
    print "6: " + board[5][0] + " | " + board[5][1] + " | " + board[5][2] + " | " + board[5][3] + " | " + board [5][4] + " | " + board [5][5] + " | " + board [5][6] + " | "
    print


def uninsert(board, col, symbol):
    for row in [1,2,3,4,5,6]:
        if (board[row-1][col-1] == symbol):
            board[row-1][col-1] = " "
            break


def insert(board, col, symbol):
    
    valid_move = False
    if(1 <= col <= 7):
        while not valid_move:
            for row in range (6,0,-1):
                if (1 <= row <= 6) and (board[row-1][col-1] == " "):
                    board[row-1][col-1] = symbol
                    return True
    else:
        print "Sorry, invalid input. Please try again!\n"
    return False

def insert2(board, col, symbol):
    board_copy = dupl(board)
    if(insert(board_copy,col,symbol)):
        return board_copy
    return [] 


def make_user_move(board):

    # sorge fuer guten Input
    while True:
        try:
            col = raw_input("What col would you like to move to (1-7):")
            col = int(col)
            break
        except ValueError:
            print("Only Numbers from (1-7)")

    valid_move = False
    while not valid_move:
        valid_move = insert(board, col, "X")

def make_nn_move(board, sym = "O"):

    valid_move = False
    while not valid_move:
            
        steps = poss_steps(board)
        li = [NN2.nn.activate(NN2.board2NN(insert2(board,step,sym))) for step in steps]
        col = steps[li.index(max(li))]

        valid_move = insert(board, col, sym)

def make_ab_move(board, sym = "O"):
    
    # alpha-beta Algorithm
    valid_move = False
    while not valid_move:
        col = minimax(board, KI_level, sym)[1]
        valid_move = insert(board, col, sym)

def make_random_move(board, sym = "X"):
    # Random KI
    steps = poss_steps(board)
    valid_move = False
    while not valid_move:
        nr = random.randint(0, len(steps)-1)
        valid_move = insert(board, steps[nr], sym)

def main():

    free_cells = 42
    users_turn = True
    count = 1
    #ttt_board = [ [ " ", " ", " ", " ", " ", " "," ", " "], [ " ", " ", " ", " ", " "," ", " ", " "], [ " ", " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " ", " "] ]
    ttt_board = [ [ " ", " ", " ", " ", " ", " "," "], [ " ", " ", " ", " "," ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "] ]
    
##    print "\nHALL OF FAME \n"
##
##    try:
##        hall_of_fame = open("HallOfFame.txt", 'r')
##
##        for name in hall_of_fame:
##            print str(count) + ".", name
##            print
##            count += 1
##
##        hall_of_fame.close()
##
##    except IOError:
##        print "No Human Has Ever Beat Me.. mwah-ha-ha-ha!\n" 

    choice = raw_input("Would you like to go first? (y or n): ")

    if (choice == 'y' or choice=='Y'):
        users_turn = True


    elif (choice == 'n' or choice =='N') :
        users_turn = False        

    else:
        print 'invalid input'

    while not winner(ttt_board) and (free_cells > 0):
        display_board(ttt_board)
        if users_turn:
            make_user_move(ttt_board)
            users_turn = not users_turn
        else:
            #make_ab_move(ttt_board)
            make_nn_move(ttt_board)
            users_turn = not users_turn
        free_cells -= 1

    display_board(ttt_board)
    if (winner(ttt_board) == 'X'):
        print "You Won!"

        # print "Your name will now be added to the Hall of Fame!"

        # hall_of_fame = open("HallOfFame.txt", 'a')
        # name = raw_input("Enter your name: ")
        # hall_of_fame.write(name+ '\n')
        # print "Your name has been added to the Hall of Fame!"

        # hall_of_fame.close()

        # print "\nGAME OVER"
    elif (winner(ttt_board) == 'O'):
        print "The Computer Won!"
        print "\nGAME OVER"
    else:
        print "Stalemate!"
        print "\nGAME OVER \n"




def randomVsNN(times=100):
    nnwon = 0
    randwon = 0
    stalemate = 0
    for i in range(times):
        free_cells = 42
        ttt_board = [ [ " ", " ", " ", " ", " ", " "," "], [ " ", " ", " ", " "," ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "] ]

        #change beginner 50/50
        randStart = True if (i%2==0) else False
        
        while not winner(ttt_board) and (free_cells > 0):
            if randStart:
                make_random_move(ttt_board)
                randStart = not randStart
            else:
                make_nn_move(ttt_board)
                randStart = not randStart
            free_cells -= 1

        if (winner(ttt_board) == 'X'):
            randwon += 1
            
        elif (winner(ttt_board) == 'O'):
            nnwon += 1
        else:
            stalemate += 1
            
    print "NN, Random, Stalemate"
    return (nnwon,randwon,stalemate)

# AB level1 : unentschieden, level 2: NN gewinnt, level 3: AB gewinnt
def NNVsAB(times=100):
    nnwon = 0
    abwon = 0
    stalemate = 0
    for i in range(times):
        print i
        free_cells = 42
        ttt_board = [ [ " ", " ", " ", " ", " ", " "," "], [ " ", " ", " ", " "," ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "] ]

        #change beginner 50/50
        nnStart = True if (i%2==0) else False
        
        while not winner(ttt_board) and (free_cells > 0):
            if nnStart:
                make_nn_move(ttt_board, sym="X")
                nnStart = not nnStart
            else:
                make_ab_move(ttt_board)
                nnStart = not nnStart
            free_cells -= 1

        if (winner(ttt_board) == 'X'):
            #print "NN won"
            nnwon += 1
            
        elif (winner(ttt_board) == 'O'):
            #print "AB won"
            abwon += 1
        else:
            stalemate += 1

        display_board(ttt_board)
            
    print "NN, AB, Stalemate"
    return (nnwon,abwon,stalemate)


def randomVsAB(times=100):
    abwon = 0
    randwon = 0
    stalemate = 0
    for i in range(times):
        free_cells = 42
        ttt_board = [ [ " ", " ", " ", " ", " ", " "," "], [ " ", " ", " ", " "," ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "], [ " ", " ", " ", " ", " ", " ", " "] ]

        #change beginner 50/50
        randStart = True if (i%2==0) else False
        
        while not winner(ttt_board) and (free_cells > 0):
            if randStart:
                make_random_move(ttt_board)
                randStart = not randStart
            else:
                make_ab_move(ttt_board)
                randStart = not randStart
            free_cells -= 1

        if (winner(ttt_board) == 'X'):
            randwon += 1
            
        elif (winner(ttt_board) == 'O'):
            nnwon += 1
        else:
            stalemate += 1
            
    print "AB, Random, Stalemate"
    return (abwon,randwon,stalemate)


###################################################################################
#start the game
#main()

#sit1 = [[' ', ' ', ' ', 'X', ' ', ' ', ' '], [' ', ' ', ' ', 'O', ' ', ' ', ' '], ['O', 'X', ' ', 'X', 'X', ' ', ' '], ['X', 'O', ' ', 'O', 'O', ' ', ' '], ['O', 'X', ' ', 'X', 'O', ' ', ' '], ['X', 'O', 'O', 'O', 'X', ' ', ' ']]
#sit2 = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'X', 'X', 'X', ' '], [' ', ' ', ' ', 'O', 'O', 'O', ' ']]






