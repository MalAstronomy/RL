'''Testing and Experiments'''

import Arena
#from MCTS import MonteCarloTreeSearch, MCTSplayer
from MCTS2 import MonteCarloTreeSearch, MCTSplayer
from MCS import MonteCarloSearch, MCSplayer
import random
import numpy as np
from tictactoe.TicTacToeGame import TicTacToeGame, display
from tictactoe.TicTacToePlayers import *
from tictactoe.TicTacToeLogic import Board
from utils import *
import matplotlib.pyplot as plt
import seaborn as sns
from connect4.Connect4Game import Connect4Game, display
from connect4.Connect4Players import *
from connect4.Connect4Logic import Board



niter = np.arange(1,200,20)
wins = np.zeros((4,len(niter)))
gamesplayed = 100

root = TicTacToeGame(3)
rp = RandomPlayer(root).play

for k in range(4):
    for i in range(len(niter)):
        mctsplayer = MCTSplayer(root,iterations = niter[i]).play
        arena_rp_mcts = Arena.Arena(mctsplayer,rp, root, display=display)
        gameswon, gameslost, gamesdrawn = arena_rp_mcts.playGames(gamesplayed,verbose=False)
        wins[k,i] = gameswon
        #winspercentage = wins/gamesplayed
        
        
sns.set()
plt.figure(figsize=(12,8))
plt.rc('axes', labelsize=20, titlesize=22)
#plt.rc('figure', titlesize=22)
#plt.rc('font',size = 22)
for k in range(4):
    plt.plot(niter,wins[k,:])
plt.xlabel('Iterations')
plt.ylabel('Wins per 100 games played')
plt.title('TicTacToe: MCTS player v Random player (UCB-1)')
plt.savefig('Tictactoe_mctsVrandom_UCB1.png')