import pygame as pg 
import random as rnd 

class Bird:
    def __init__(self,x,y,r,y_vel,jump_vel,g,color):
        self.x=x 
        self.y=y 
        self.r=r 
        self.y_vel=y_vel
        self.g=g 
        self.color=color
        self.jump_vel=jump_vel
    
    def flap(self,t):
        self.y_vel+=self.g*t
        self.y+=self.y_vel*t
    def hit_box(self):
        return pg.Rect(self.x-self.r,self.y-self.r,self.r,self.r)
    def out_of_cage(self,scr_size):
        return self.y-self.r<0 or self.y+self.r>scr_size[1]
    def jump(self):
        self.y_vel=self.y_vel*0-self.jump_vel
    def draw(self,wnd):
        pg.draw.circle(wnd,self.color,(self.x,self.y),self.r)
    def draw(self,wnd,outline):
        pg.draw.circle(wnd,self.color,(self.x,self.y),self.r)
        if outline:
            pg.draw.rect(wnd,pg.Color.black,self.hit_box(self),1)

class Pipe_pair:
    def __init__(self,rect1,rect2):
        self.top=rect1
        self.bot=rect2 
        self.color=(30,200,80)
    def __init__(self,rect1,rect2,color):
        self.top=rect1
        self.bot=rect2 
        self.color=color
    def __init__(self,scr_size):#yikes
        
        margin_per=0.15
        hole_height=scr_size[1]*0.33
        pipe_width=hole_height*0.3

        min_bot_top=(1-margin_per)*scr_size[1]
        max_bot_top=margin_per*scr_size[1]+hole_height
        top_of_bot_pipe=rnd.randint(max_bot_top,min_bot_top)
        
        self.bot=pg.Rect(scr_size[0],top_of_bot_pipe,pipe_width,scr_size[1]-top_of_bot_pipe)
        self.top=pg.Rect(scr_size[0],0,pipe_width,top_of_bot_pipe-hole_height)

        self.color=(30,200,80)

    def draw(self,wnd):
        pg.draw.rect(wnd,self.color,self.top)                
        pg.draw.rect(wnd,self.color,self.bot)                
    def collision(self,rect):
        return self.top.colliderect(rect) or self.bot.colliderect(rect)
    def move(self,px):
        self.top.x+=px
        self.bot.x+=px
    def out_of_screen(self,scr_size):
        return self.bot.right<scr_size[0]
    def hole_rect(self):
        return (self.top.left,self.top.bottom,self.bot.width,self.bot.top-self.top.bottom)
class Game:
    def __init__(self,scr_size):#scr_rect????
        init_speed=300
        self.game_size=scr_size
        self.bird=Bird(scr_size[0]/6,scr_size[1]/2,25,0,550,800,(230,200,80))
        self.speed=init_speed
        self.pipes=[]
        self.points=0
        self.new_pipe()
        self.over=False
    def new_pipe(self):
        self.points+=1
        self.speed+=10+(100/(40+self.points))

        self.distance_to_next=rnd.randint(round(self.game_rect.width*0.3),round(self.game_rect.width*0.6))
        self.pipes.append(Pipe_pair(self.game_rect))
    def draw(self,wnd):
        for pipe in self.pipes:
            pipe.draw(wnd) 
        self.bird.draw(wnd,False)

        font = pg.font.SysFont(None, self.bird.r)
        score = font.render("Speed: " + str(round(self.speed)), True, (255,255,255))
        wnd.blit(score,(self.bird.r,self.bird.r))

    def update(self,t):
        step=-t*self.speed
        
        i=0
        n=len(self.pipes)
        while(i<n):
            pipe=self.pipes[i]
            pipe.move(step)
            i+=1
            if(pipe.collision(self.bird.hit_box())):
                self.over=True 
            if(pipe.out_of_screen(self.game_rect)):
                self.pipes.remove(pipe)
                i-=1
                n-=1
               

        self.distance_to_next+=step 
        if(self.distance_to_next<0):
            self.new_pipe()

        self.bird.flap(t)
        if(self.bird.out_of_cage(self.game_rect)):
            self.over=True
    def jump_clicked(self):
        self.bird.jump()
    def pipes_infront(self,num):
            next_pipes=[]
            for pipe in self.pipes:
                if num<=0:
                    break
                if pipe.right>self.bird.left:
                    num-=1
                    next_pipes.append(pipe)
            return next_pipes
    def State(self):
        trans_x=-self.game_size[0]/6
        trans_y=-self.game_size[1]/2
        pipe=self.pipes_infront(1)
        
        (hole_x,hole_y,hole_w,hole_h)=pipe.hole_rect()
        return (self.bird.y+trans_y,self.speed,self.bird.y_vel,hole_x+trans_x,hole_y+trans_y,hole_w,hole_h)
        
