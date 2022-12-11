from network import Network
from game import Game 
class Agent:
    
    
    def __init__(self):#run simulation, return fitness etc
        self.game=Game(800,800)#?????????? 
        self.network= Network(7,16,1,2)
        self.iter=0
        self.max_iter=999999
        self.dead=False
    
    def __init__(self,network):
        self.game=Game(800,800)
        self.network= network
        self.iter=0
        self.max_iter=999999
        self.dead=False
    
    
    def time_interval(self):
        return (10/self.game.speed)
    def step(self):
        dt=self.time_interval()
        self.game.update(dt)

        if self.game.over:
            self.dead=True

        if self.Action():
            self.game.jump_clicked()

    def run(self):
        while(not self.dead and self.iter<self.max_iter):
            self.iter+=1
            self.step()

        return self.Score()

    def Action(self):
        return self.network.Output(self.game.State())
    
    def Score(self):
        return self.iter


    @staticmethod 
    def Run(agent):
        return agent.run()