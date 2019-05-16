import numpy as np
import random
from tictactoe.TicTacToeLogic import Board
from tictactoe.TicTacToePlayers import RandomPlayer


class Nodetree:
    def __init__(self, parent=None, action=None, board=None, boardstate=None):
        self.parent = parent
        self.board = boardstate
        self.childnodes = []
        self.wins = 0
        self.visits = 0
        self.availableactions = board.getValidMoves(boardstate[0],boardstate[1]).astype(int)
        print(self.availableactions)
        if type(board).__name__ == 'TicTacToeGame':
            self.availableactions = board.getValidMoves(boardstate[0],boardstate[1])[:-1].astype(int)
            print(self.availableactions)
        self.action = action
    
    def UCB_bestchild(self,UCB_constant = 1):
        child_score = []
        for i in self.childnodes:
            #w = i.wins/i.visits + UCB_constant*np.sqrt(2*np.log(self.visits)/i.visits)  #UCB-2
            w = i.wins + UCB_constant*np.sqrt(2*np.log(self.visits)/i.visits)          #UCB-1
            child_score.append(w)
        #print(child_score)
        return self.childnodes[np.argmax(child_score)]
    
    def AddchildNodes(self, action, board, boardstate):
        newchildnode = Nodetree(parent = self, action = action, board=board, boardstate=boardstate)
        self.availableactions[action] = 0
        #print(self.availableactions)
        self.childnodes.append(newchildnode)
        return newchildnode
    
    def updateResults(self, result):
        self.visits += 1
        self.wins += result
        
    
class MonteCarloTreeSearch:
    
    def mcts(Iterations, root, boardstate):
        rootstate = [boardstate, 1]
        rootnode = Nodetree(board = root, boardstate=rootstate)

        for i in range(Iterations):
            node = rootnode
            board = root
            print(node.availableactions)
            #Selection
            if np.all(node.availableactions == 0):
                while node.childnodes != []:
                    node = node.UCB_bestchild()
                    #print(node.board,boardstate[1], node.action)
                    #board.getNextState(node.board, boardstate[1], node.action)

            #Expansion
            if np.any(node.availableactions == 1):
                actionsize = board.getActionSize()
                
                if board.getActionSize() == 10:
                    actionsize = actionsize -1
                randomselection = np.random.randint(actionsize)
                #print(randomselection)
                while node.availableactions[randomselection]!=1:
                    randomselection = np.random.randint(actionsize)    
                randomaction = randomselection
                #print(rootstate[1])
                boardstate = board.getNextState(node.board[0], node.board[1], randomaction)
                #print(boardstate[0])
                node = node.AddchildNodes(randomaction, board, boardstate)
                
            #Rollout/Simulation with a random roll-out policy
            while board.getGameEnded(boardstate[0],boardstate[1]) == 0.0:
                randomselection = RandomPlayer(board)
                randomaction = randomselection.play(boardstate[0])
                boardstate = board.getNextState(boardstate[0], boardstate[1],randomaction)
                #print(boardstate)
                #print(board.getValidMoves(boardstate[0],1))

            #print(node.availableactions)
            #Backpropagation
            while node != None:
                node.updateResults(board.getGameEnded(boardstate[0],rootstate[1]))#Updating the results for player 1.Stateisterminal.
                node = node.parent                                        # Update node with result from POV of node.playerJustMoved.

            
        #Select the node with the maximum number of wins/visits and get it's action
        return rootnode.UCB_bestchild(UCB_constant = 0)


class MCTSplayer:
    def __init__(self, game, iterations=2000):
        self.game = game
        self.niter = iterations
        
    def play(self, board):
        bestnode = MonteCarloTreeSearch.mcts(self.niter, self.game, board)
        bestaction = bestnode.action
        return bestaction







    

