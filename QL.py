'''
    write a simple Q-learning player
    '''

#QLearning
'''
    define a dictionary q
    define a state= np.zeros((6,7))
    define actions= the list of unfilled columns
    define previous state as None
    
    1) start with an empty state/current_state/state- and 'pick a random action to begin with' / 'pick the action
    corresponding to the maximum qs for all the actions in that state'
    2) get next_state.
    3) q(state,action)=1 if q=None, if not, return q(state,action)
    4) calculate the q value where
    q(current_state,chosen_action)= current_q+alpha(R+gamma*(maxq(next_state,all actions))-current_q)
    '''

import numpy as np
import ast
import pickle


class QLearningPlayer():
    
    #Initialise the Qvalue dictionary, the constants gamma and alpha from the Bellmans equation and the game being played.
    def __init__(self,game):
        self.game = game
        self.gamma=1
        self.alpha=1
        self.q={}
        self.c=0
    
    #returns an action based on the stored qvalues and updates the qtable
    def learning(self, current_state):
        
        self.c+=1
        
        action=np.random.choice(self.possible_actions(current_state),1)[0]
        if self.retrieveQ(current_state,action)==1:
            self.updateQ(current_state,action)
            
            with open("_Qvalue_p/qvalue.txt", "wb") as myFile:
                pickle.dump(self.q, myFile)
        
        else:
            learned_act=self.learned_action(current_state)
            action= np.int64(int(learned_act))
            self.updateQ(current_state,action)
            
            with open("_Qvalue_p/qvalue.txt", "wb") as myFile:
                pickle.dump(self.q, myFile)

    return action

    #returns an action based on the stored q values
    def learned(self,current_state):
    
        with open("_Qvalue_p/qvalue.txt", "rb") as myFile:
            qvalue = pickle.load(myFile)
        
        actions=self.possible_actions(current_state)
        
        board=self.array_to_tuple(current_state)
        
        for action in actions:
            if qvalue.get((board,action))==None:
                qvalue[(board,action)]=1
    
        result=[]
        maxi=max(np.array([qvalue.get((board,action)) for action in actions]))
        for keywords in qvalue.keys():
            if qvalue[keywords]==maxi:
                result.append(keywords)
        actionss=[]
        for i in np.arange(len(result)):
            if result[i][0]==board:
                actionss.append(result[i][1])

        acs= np.intersect1d(actionss,actions)
        action=np.random.choice(acs,1)[0]

        return action
    
    #Returns the actions with the maximum Qvalue for a given state.
    def extracting_MaxQactions(self,current_state):
        
        board=self.array_to_tuple(current_state)
        result=[]
        actions= self.possible_actions(current_state)
        maxi=max(np.array([self.retrieveQ(current_state,action) for action in actions]))
        for keywords in self.q.keys():
            if self.q[keywords]==maxi:
                result.append(keywords)
        actionss=[]
        for i in np.arange(len(result)):
            if result[i][0]==board:
                actionss.append(result[i][1])

        return actionss

    #Updates the Qvalue for a given state and its corresponding action.
    def updateQ(self,current_state,action):
    
        currentQ= self.retrieveQ(current_state,action)
        next_state = self.game.getNextState(current_state, 1, action)
        reward= self.game.getGameEnded(next_state[0],1)
        nextQ= [self.retrieveQ(next_state[0],action) for action in self.possible_actions(current_state)]
        Q= currentQ+ self.alpha*(reward+(self.gamma*(max(nextQ))-currentQ))
        board=self.array_to_tuple(current_state)
        self.q[(board,action)]=Q
    
    #Returns a valid action with the maximum Qvalue pertaining to a given state.
    def learned_action(self,current_state):
        
        actions=self.possible_actions(current_state)
        actionss=self.extracting_MaxQactions(current_state)
        acs= np.intersect1d(actionss,actions)
        action=np.random.choice(acs,1)[0]
        return action
    
    #Returns all valid actions given a state.
    def possible_actions(self,current_state):
        
        if type(self.game).__name__=='TicTacToe':
            ValidMoves=self.game.getValidMoves[:-1]
        
        else:
            ValidMoves=self.game.getValidMoves
        actions=np.where(ValidMoves(current_state,1)==True)[0]
        return actions

    #Returns the Qvalue associated with the given state and an action.
    def retrieveQ(self,current_state,action):
        board=self.array_to_tuple(current_state)
        if self.q.get((board,action))==None:
            self.q[(board,action)]=1
        
        return self.q.get((board,action))

    #Returns the state as a tuple to be stored as a key in the Q_dictionary.
    def array_to_tuple(self,board):
        return  tuple(map(tuple,board))



