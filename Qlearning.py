'''
write a simple Q-learning player
'''

#QLearning
'''
define a dictionary q
define a state= np.zeros((6,7))
define actions= the list of unfilled columns 
define previous state as None

1) start with an empty state/prev_state/state- and 'pick a random action to begin with' / 'pick the action 
 corresponding to the maximum qs for all the actions in that state'
2) get current_state.
3) q(state,action)=1 if q=None, if not, return q(state,action)
4) calculate the q value where 
    q(prev_state,chosen_action)= prev_q+alpha(R+gamma*(maxq(current_state,all actions))-prev_q)
'''

import numpy as np
import ast


class QLearningPlayer():
    
    def __init__(self,game):       
        self.game = game
        self.gamma=1 
        self.alpha=1
        self.q={}
        self.c=0
#         print('first ',self.q)
        
#         with open('qvalue.txt','r') as data:
#             qvalue=data.read()
#             self.q=ast.literal_eval(qvalue)
        
        
    def learning(self, current_state): #add curplayer to all play functions
        self.c+=1
#         if (self.game.getCanonicalForm(current_state,curPlayer)==self.game.getInitBoard()).all(): 
#             self.q={}
        action=np.random.choice(self.possible_actions(current_state),1)[0]
        
        if self.retrieveQ(current_state,action)==1: 
            self.q=self.updateQ(current_state,action)
            #print('Q ',self.q)
            
            with open('_qvalue_.txt','w') as data:
                data.write(str(self.q))
                
            if self.c%100 ==0:  
                with open('_Qvalue_/qvalue_'+ str(self.c)+'.txt','w') as data:
                    data.write(str(self.q))
            print('action',action)        
            action= action

        else: 
            learned_act=self.learned_action(current_state)
            
#             if learned_act in 
            action= np.int64(int(learned_act))
            
#             if action in 
            #print('action1',action) 
            self.q=self.updateQ(current_state,action)
            
            #print('Q ',self.q)
            
            with open('_qvalue_.txt','w') as data:
                data.write(str(self.q))
                
            if self.c%100 ==0:  
                with open('_Qvalue_/qvalue_'+ str(self.c)+'.txt','w') as data:
                    data.write(str(self.q))
                   
#             print('im working too')
        return action
    
    def learned(self,current_state): 
        
        with open('_Qvalue_/qvalue_37700.txt','r') as data:
             qvalue=data.read()
        qvalue=ast.literal_eval(qvalue)
        
        actions=np.where(self.game.getValidMoves(current_state,1)==True)[0]
#         print('valid moves',actions)

        board=self.array_to_tuple(current_state)
        
        for action in actions:   
            if qvalue.get((board,action))==None:
                qvalue[(board,action)]=1
      
        result=[]                                       #Making ready of the result list

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
        print('type',type(action))
        
        
#         print('actions',actions)
#         print('actionss',actionss)
#         print('action',action)
        return action


    def extracting_action(): 
        
        result=[]                                       #Making ready of the result list

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
        print('type',type(action))
        
        
            
    def updateQ(self,current_state,action):  
        
        currentQ= self.retrieveQ(current_state,action)  
        next_state = self.game.getNextState(current_state, 1, action)
        reward= self.game.getGameEnded(next_state[0],1)
#         print('reward ' ,reward)
#         print('next state',next_state[0])
        nextQ= [self.retrieveQ(next_state[0],action) for action in self.possible_actions(current_state)]
#         print('before',currentQ)
        Q= currentQ+ self.alpha*(reward+(self.gamma*(max(nextQ))-currentQ))
        #print(Q,self.q)#####################################see this 
#         print('after cal ',Q)
        self.updatingQ(Q,current_state,action)
#         
#         print('after updating ',self.q.values())
        return self.q
                                                              
#     def play(self,current_state,curplayer): 
          #get the q                                                    
#         action=  self.learned_action(current_state,curplayer)   
#         return action                                          
                                                                                                                      
                                                              
    def learned_action(self,current_state): 
        actions=np.where(self.game.getValidMoves(current_state,1)==True)[0]
        board=self.array_to_tuple(current_state)
        print('allowed',actions)
        
        result=[]                                       #Making ready of the result list

        maxi=max(np.array([self.retrieveQ(current_state,action) for action in actions]))
        for keywords in self.q.keys():
            if self.q[keywords]==maxi:
                result.append(keywords) 
        actionss=[]       
        for i in np.arange(len(result)): 
            if result[i][0]==board: 
                actionss.append(result[i][1])
        
        
        acs= np.intersect1d(actionss,actions)
        
        action=np.random.choice(acs,1)[0]
        
        #action= np.where(max([self.retrieveQ(current_state,action) for action in actions]))[0]   
        
        print('la',action)
        return action                                                     
        
    def possible_actions(self,board): 
        actions=np.where(self.game.getValidMoves(board,1)==True)[0]
        return actions                                                      

    def retrieveQ(self,board,action): 
        print('8',action)
        #print('board type before', type(board))
        board=self.array_to_tuple(board)
        #print('board type after', type(board))
        print(board)
        #print(self.q.keys())
        #print(self.q.get((board,action)))
        #print('action',action)
        
        if self.q.get((board,action))==None:
            self.q[(board,action)]=1
            
        return self.q.get((board,action))
    
    
    def array_to_tuple(self,board): 
        
        return  tuple(map(tuple,board))
        
    def updatingQ(self,Q,board,action):
        board=self.array_to_tuple(board)
        self.q[(board,action)]=Q
    
    def selfq(self): 
        return self.q
    
    def printme(self): 
        print('im here QL')
    