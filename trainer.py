from agent import Agent
from network import Network 
import multiprocessing
class Trainer:
    def __init__(self,gen_num,gen_size) -> None:
        self.gen=0
        self.max_gen=gen_num
        self.pop_size=gen_size
        self.popultaion=[]#agents 
        
        for i in range (self.pop_size):
            self.popultaion.append(Agent())
        
    def Selection(self,perc):
        sort_pop=sorted(self.popultaion, key=lambda x: x.Score(),reverse=True)
        size=self.pop_size*perc 
        return sort_pop[0:size]
        
    def NextGen(self):
        self.popultaion.sort(key=lambda x: x.Score(),reverse=True)
        #original_pop=self.Selection(self,1/2)        
        #mutated=[]

        for i in range(self.pop_size/2,len(self.pop_size)):
            self.popultaion[i]=(self.popultaion[i-self.pop_size/2].network.MutantClone())
        
    def RunGen(self,num_threads):
        threads=multiprocessing.Pool(num_threads)
        scores=threads.map(Agent.Run,self.popultaion)
        
        self.gen+=1
        self.NextGen()
        
    def Train(self):
        while(self.gen<=self.max_gen):
            self.RunGen(8)

        print(self.popultaion[0].network.print())