class Flowers(): 
    def __init__(self,q=None,name=""):
        if q==None:  
            self.q={}
        else: 
            self.q=q
        self.name=name
        
    def tulips(self,q):
        print('kuekenhoff')
        self.q=q
        print(self.q)
        return self.q
        
        
        