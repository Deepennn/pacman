from glob import glob
from logging import exception
from pathlib import Path
from parameter import *
from util import Direction,Map
from agent import Pacman,Ghost, if_touch
import random,pathctrl
import copy

def getposindex(x,y):
    tempsize=Map.mapobject.get_size()
    return x*tempsize[0]+y

def ghost_random(ghostobj:Ghost):
    tempghostpos=ghostobj.getposition()
    tempchoice=ghostobj.validposition()
    if tempchoice==[]:
        return -1
    else:
        return tempchoice[random.randint(0,len(tempchoice)-1)]

def ghost_best(ghostobj:Ghost):
    global navigating_method
    if navigating_method==999:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostpos=ghostobj.getposition()
    way=pathctrl.how_to_go(tempghostpos[0],tempghostpos[1],temppacmanpos[0],temppacmanpos[1])
    if len(way)<=1:
        return -1
    return way[1][2]

def lambda_random(lambda_pos,ghostobj:Ghost):
    temprandom=random.random()
    if temprandom<lambda_pos:
        return ghost_random(ghostobj)
    else:
        return ghost_best(ghostobj)

def ghost_predict(lambda_pos,ghostobj:Ghost):
    global navigating_method
    if navigating_method==999:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostpos=ghostobj.getposition()
    temppacori=temppacman.getorient()
    tempmovevec=Direction.movevector[temppacori]
    temprandom=random.random()
    if temprandom<lambda_pos:
        return ghost_random(ghostobj)
    predictpos=[temppacmanpos[0]+3*tempmovevec[0],temppacmanpos[1]+3*tempmovevec[1]]
    if Pacman.pacmanmap_valid(predictpos[0],predictpos[1])==True:
        way=pathctrl.how_to_go(tempghostpos[0],tempghostpos[1],predictpos[0],predictpos[1])
    else:
        way=pathctrl.how_to_go(tempghostpos[0],tempghostpos[1],temppacmanpos[0],temppacmanpos[1])
    if len(way)<=1:
        return -1
    return way[1][2]
        
def ghost_frightened(ghostobj:Ghost):
    global navigating_method
    if navigating_method==999:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostpos=ghostobj.getposition()
    way=pathctrl.how_to_go(tempghostpos[0],tempghostpos[1],temppacmanpos[0],temppacmanpos[1])
    if len(way)<=1:
        return -1
    vaguedis=abs(tempghostpos[0]-temppacmanpos[0])+abs(tempghostpos[1]-temppacmanpos[1])
    togoway=-1
    for i in range(4):
        newx= tempghostpos[0] + Direction.movevector[i][0]
        newy= tempghostpos[1] + Direction.movevector[i][1]
        if Ghost.ghostmap_valid(newx,newy)==True:
            if abs(newx-temppacmanpos[0])+abs(newy-temppacmanpos[1])>vaguedis:
                vaguedis=abs(newx-temppacmanpos[0])+abs(newy-temppacmanpos[1])
                togoway=i
    return togoway
            
def lambda_frightened(lambda_pos,ghostobj:Ghost):
    temprandom=random.random()
    if temprandom<lambda_pos:
        return ghost_random(ghostobj)
    else:
        return ghost_frightened(ghostobj)

#Basic Rule-Based Pacman

def naive_pacman():
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    toghostdis=[0 for i in range(len(Ghost.ghostvector))]
    toway=[None for i in range(len(Ghost.ghostvector))]
    cnt=-1
    mindis=const_inf
    ghostpos=[]
    for ghostobj in Ghost.ghostvector:
        cnt+=1
        ghostpos.append(ghostobj.getposition())
        toway[cnt]=pathctrl.how_to_go(temppacmanpos[0],temppacmanpos[1],ghostpos[cnt][0],ghostpos[cnt][1])
        toghostdis[cnt]=len(toway[cnt])-1
        mindis=min(mindis,toghostdis[cnt])
    if mindis>=6:
        scatter_food=pathctrl.find_nearest(temppacmanpos[0],temppacmanpos[1])
        way=pathctrl.how_to_go(temppacmanpos[0],temppacmanpos[1],scatter_food[0][0],scatter_food[0][1])
        return way[1][2]
    else:
        maxdis=0
        choice=-1
        for i in range(4):
            newpos=[temppacmanpos[0] + Direction.movevector[i][0], temppacmanpos[1] + Direction.movevector[i][1]]
            if Ghost.ghostmap_valid(newpos[0],newpos[1])==True:
                tempmindis=const_inf
                for j in range(len(Ghost.ghostvector)):
                    tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                if tempmindis>maxdis:
                    choice=i
                    maxdis=tempmindis
        return choice

#Rule-Based Pacman with higher Intelligence and smarter consideration

def sophisticated_pacman():
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    toghostdis=[0 for i in range(len(Ghost.ghostvector))]
    toway=[None for i in range(len(Ghost.ghostvector))]
    cnt=-1
    mindis=const_inf
    ghostpos=[]
    for ghostobj in Ghost.ghostvector:
        cnt+=1
        ghostpos.append(ghostobj.getposition())
        toway[cnt]=pathctrl.how_to_go(temppacmanpos[0],temppacmanpos[1],ghostpos[cnt][0],ghostpos[cnt][1])
        toghostdis[cnt]=len(toway[cnt])-1
        mindis=min(mindis,toghostdis[cnt])
    # print(mindis)
    maxdis=0
    choice=-1
    if temppacman.invtime==0:
        if mindis<=4:
            for i in range(4):
                # if i==toway[0][1][2] or i==toway[1][1][2]:
                    # continue
                newpos=[temppacmanpos[0] + Direction.movevector[i][0], temppacmanpos[1] + Direction.movevector[i][1]]
                if Ghost.ghostmap_valid(newpos[0],newpos[1])==True:
                    tempmindis=const_inf
                    for j in range(len(Ghost.ghostvector)):
                        tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                    if tempmindis>maxdis:
                        choice=i
                        maxdis=tempmindis
            # print("choice"+str(choice))
            return choice
        elif mindis<=8 and (system_default_ghost_num<=1 or toway[0][1][2]!=toway[1][1][2]):
            for i in range(4):
                # if i==toway[0][1][2] or i==toway[1][1][2]:
                    # continue
                newpos=[temppacmanpos[0] + Direction.movevector[i][0], temppacmanpos[1] + Direction.movevector[i][1]]
                if Ghost.ghostmap_valid(newpos[0],newpos[1])==True:
                    tempmindis=const_inf
                    for j in range(len(Ghost.ghostvector)):
                        tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                    if tempmindis>maxdis:
                        choice=i
                        maxdis=tempmindis
            # print("choice"+str(choice))
            return choice
        else:
            scatter_food=pathctrl.find_nearest(temppacmanpos[0],temppacmanpos[1])
            for tempfood in scatter_food:    
                way=pathctrl.how_to_go(temppacmanpos[0],temppacmanpos[1],tempfood[0],tempfood[1])
                tempgoal=way[1][2]
                newpos=[temppacmanpos[0] + Direction.movevector[tempgoal][0], temppacmanpos[1] + Direction.movevector[tempgoal][1]]
                tempmindis=const_inf
                for j in range(len(Ghost.ghostvector)):
                    tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                if tempmindis>maxdis:
                    choice=tempgoal
                    maxdis=tempmindis
            return choice
    else:                
        scatter_food=pathctrl.find_nearest(temppacmanpos[0],temppacmanpos[1])
        for tempfood in scatter_food:    
            way=pathctrl.how_to_go(temppacmanpos[0],temppacmanpos[1],tempfood[0],tempfood[1])
            tempgoal=way[1][2]
            newpos=[temppacmanpos[0] + Direction.movevector[tempgoal][0], temppacmanpos[1] + Direction.movevector[tempgoal][1]]
            tempmindis=const_inf
            for j in range(len(Ghost.ghostvector)):
                tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
            if tempmindis>maxdis:
                choice=tempgoal
                maxdis=tempmindis
        return choice

