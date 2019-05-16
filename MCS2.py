'''
write MCS player as a small exercise before you implement the MCTS
'''

import numpy as np
import random
from tictactoe.TicTacToeLogic import Board
from tictactoe.TicTacToePlayers import RandomPlayer


class Node:
    def __init__(self, parent=None, action=None, board=None, boardstate=None):
        self.parent = parent
        self.board = boardstate
        self.childnodes = []
        self.wins = 0
        self.availableactions = board.getValidMoves(boardstate[0],boardstate[1])
        if type(board).__name__ == 'TicTacToeGame':
            self.availableactions = board.getValidMoves(boardstate[0],boardstate[1])[:-1].astype(int)
            print(self.availableactions)
        self.action = action
    
    def UCB_bestchild(self, niter):
        expectationvalue = []
        for i in self.childnodes:
            ev = i.wins*1.0/niter
            expectationvalue.append(ev)
        print('Exp values are %s'%(expectationvalue))
        return self.childnodes[np.argmax(expectationvalue)]
    
    def AddchildNodes(self, action, board, boardstate):
        newchildnode = Node(parent = self, action = action, board=board, boardstate=boardstate)
        self.availableactions[action] = 0
        self.childnodes.append(newchildnode)
        return newchildnode
    
    def updateResults(self, result):
        self.wins += result
        
    
class MonteCarloSearch:
    
    def mcs(Iterations, root, boardstate):
        rootstate = [boardstate, 1]
        board  = root
        rootnode = Node(board = root, boardstate=rootstate)
        expectationvalue = np.zeros(len(rootnode.availableactions))
        actionresult = 0
        actionsize = board.getActionSize()                
        if board.getActionSize() == 10:
            actionsize = actionsize -1
        while np.any(rootnode.availableactions == 1):
            randomselection = np.random.randint(actionsize)
            while rootnode.availableactions[randomselection]!=1:
                randomselection = np.random.randint(actionsize)    
            randomaction = randomselection
            boardstate = board.getNextState(rootnode.board[0], rootnode.board[1], randomaction)
            node = rootnode.AddchildNodes(randomaction, board, boardstate)
            #print(boardstate)  
            for i in range(Iterations):
                noderollout = node
                boardstaterollout = boardstate
                board = root

                #Rollout/Simulation with a random roll-out policy
                while board.getGameEnded(boardstaterollout[0],boardstaterollout[1]) == 0.0:
                    randomselection = RandomPlayer(board)
                    randomaction = randomselection.play(boardstaterollout[0])
                    boardstaterollout = board.getNextState(boardstaterollout[0], boardstaterollout[1],randomaction)
                    #print(boardstaterollout)
                #print(board.getGameEnded(boardstaterollout[0],1))
                actionresult = actionresult + board.getGameEnded(boardstaterollout[0],1)
            #print(actionresult)
            node.updateResults(actionresult) 
        #Select the node with the maximum ratio of wins per rollouts and get it's action
        return rootnode.UCB_bestchild(Iterations)


class MCSplayer:
    def __init__(self, game, iterations=50):
        self.game = game
        self.niter = iterations
        
    def play(self, board):
        bestnode = MonteCarloSearch.mcs(self.niter, self.game, board)
        bestaction = bestnode.action
        print('Best action to take is %.3f'%(bestaction))
        return bestaction







    

