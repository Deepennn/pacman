from ast import Pass
import pygame
import os

import pygame as pygame
from pygame.locals import *
from srcload import agentinit,initset,imageinit,fontinit,setbutton
from painting import repainting
from agent import Pacman,Ghost,if_touch
from util import Map,Direction,Button
from parameter import *
import pathctrl
import agentctrl



def restart(type=0, navigate=nownavigating):
    global pygame_event_text,ifwin,navigating_method
    Ghost.clearghost()
    agentinit(type)
    tempMap=Map.mapobject
    navigating_method=nownavigating
    tempPac=Pacman.pacmanobject
    tempPacDir=tempPac.getposition()
    eatresult=tempMap.eat(tempPacDir[0],tempPacDir[1])
    if eatresult==2:
        tempPac.becomeinv()
    repainting()
    pygame_event_text=[]
    pathctrl.clear_manhanttan()
    pathctrl.clear_dfs()
    pathctrl.cleardp()
    ifwin=False
    # pygame.event.set_blocked(MOUSEMOTION)
    
if __name__=="__main__":
    #pacman_flash_x,pacman_flash_y
    
    '''These are first-only functions'''
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    pygame.init()
    initset()
    imageinit()
    fontinit()
    setbutton()
    ifwin=False
    '''End'''
    
    agentinit(0)
    repainting()
    pygame_event_text=[]
    # pygame.event.set_blocked(MOUSEMOTION)

    firsttime=True

    while True:
        now_event=pygame.event.get()

        '''This is first-time judgement'''
        if firsttime:
            for every_event in now_event:
                if every_event.type==QUIT:
                    exit()
                if every_event.type == MOUSEMOTION or every_event.type == MOUSEBUTTONDOWN:
                    temp_mousepos = pygame.mouse.get_pos()
                    for everybutton in Button.buttonobject:
                        if everybutton.be_clicked(temp_mousepos) == True:
                            everybutton.changebackcolor((15, 77, 146))
                            everybutton.changelinecolor((0, 0, 0))
                            pygame.time.set_timer(29, 200, 1)
                            beclicked = everybutton
                            # table
                            if everybutton.tag == 6:
                                if every_event.type == MOUSEBUTTONDOWN:
                                    firsttime = False
                        else:
                            everybutton.changebackcolor((0, 114, 187))
                            everybutton.changelinecolor((0, 0, 0))
                repainting()
            pygame.display.update()
            continue
        '''End'''


        if len(now_event)>0:
            # print(len(now_event))
            for every_event in now_event:
                # print(str(every_event))
                temp_pacman=Pacman.pacmanobject
                temp_ghostvec=Ghost.ghostvector
                temp_pacmanpredic=temp_pacman.getpreviousposition()
                temp_pacmandic=temp_pacman.getposition()
                temp_ori=temp_pacman.getorient()
                temp_map=Map.mapobject
                if temp_map.if_win()==True or temp_map.getfoodnum()==0:
                    navigating_method=999
                if every_event.type==QUIT:
                    exit()
                if every_event.type==25:
                    Pacman.pacmanobject.changemouthopen()
                    if_pacmanmouse_open=Pacman.pacmanobject.getmouthopen()
                    # print(str(every_event))
                    
                if every_event.type==27:
                    if temp_map.if_win()==False and navigating_method!=999:
                        temp_map.updatetime()
                        temp_pacman.decreaseinvtime()
                    temp_pacman.pacman_flash_x=temp_pacmanpredic [0]+movingtick/5*(temp_pacmandic[0]-temp_pacmanpredic[0])
                    temp_pacman.pacman_flash_y=temp_pacmanpredic[1]+movingtick/5*(temp_pacmandic[1]-temp_pacmanpredic[1])
                    for ghostobj in Ghost.ghostvector:
                        temp_ghostdic=ghostobj.getposition()
                        temp_ghostpredic=ghostobj.getpreviousposition()
                        ghostobj.ghost_flash_x=temp_ghostpredic[0]+movingtick/5*(temp_ghostdic[0]-temp_ghostpredic[0])
                        ghostobj.ghost_flash_y=temp_ghostpredic[1]+movingtick/5*(temp_ghostdic[1]-temp_ghostpredic[1])
                    
                    touchtime=if_touch()
                    if touchtime[0]==True:
                        if temp_pacman.invtime==0:
                            # print("You died!")
                            navigating_method=999
                            diepacman=Pacman(11,18,-1)
                            for ghostobj in Ghost.ghostvector:
                                ghostobj.changeorient(-1)
                        else:
                            # Ghost.ghostvector.remove(touchtime[1])
                            touchtime[1].respawn()
                            temp_map.updatescore(10)
                        # restart(0,False,False)
                        # pass
                        # print(score)
                    if movingtick>=5:
                        
                        if temp_map.if_win()==False and navigating_method!=999:
                            temp_map.updatestep()
                        # print("pacmanx:"+str(temp_dic[0]))
                        # print("pacmany:"+str(temp_dic[1]))
                        movingtick-=5
                        
                        ''''''
                        Pacman.pacmanobject.updatepreviousposition()
                        Pacman.pacmanobject.updatepreviousorient()
                        for ghostobj in Ghost.ghostvector:
                            ghostobj.updatepreviousposition()
                            ghostobj.updatepreviousorient()
                            temp_ghostori=ghostobj.getorient()
                            
                            # if temp_ori!=None:
                                # pacman_move_vector=Directions.getmove(temp_ori)
                            if temp_ghostori in ghostobj.validposition():
                            # print("move:")
                                ghostobj.move(temp_ghostori)
                        # if temp_ori!=None:
                            # pacman_move_vector=Directions.getmove(temp_ori)
                        if temp_ori in Pacman.pacmanobject.validPosition():
                            # print("move:")
                            Pacman.pacmanobject.move(temp_ori)
                    if movingtick==3:
                        # print(Map.mapobject.get_ifeaten(temp_dic[0],temp_dic[1]))
                        if Map.mapobject.get_ifeaten(temp_pacmandic[0],temp_pacmandic[1])==1:
                            eatresult=temp_map.eat(temp_pacmandic[0],temp_pacmandic[1])
                            if eatresult==2:
                                Pacman.pacmanobject.becomeinv()
                                for ghost in Ghost.ghostvector:
                                    ghost.if_scared=1
                            temp_map.if_win()
                            scores+=1


                        if navigating_method==2:
                            temp_moveaction = agentctrl.naive_pacman()
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method==3:
                            temp_moveaction = agentctrl.sophisticated_pacman()
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction


                        elif navigating_method == 4:
                            temp_moveaction = pathctrl.greedy_search_bfs()
                            if temp_moveaction != -1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method == 5:
                            temp_moveaction = pathctrl.greedy_search_massive_manhattan()
                            if temp_moveaction != -1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method == 6:
                            # print("3333")
                            temp_moveaction = pathctrl.greedy_search_dfs()
                            # print("tempmove:"+str(temp_moveaction))
                            if temp_moveaction != -1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method == 7:
                            # print("3333")
                            temp_moveaction = pathctrl.dp()
                            # print("tempmove:"+str(temp_moveaction))
                            if temp_moveaction != -1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction


                        elif navigating_method==999:
                            pass
                        if ghost_navigating_method==1:
                            for ghostobj in Ghost.ghostvector:
                                # temp_move=agentctrl.ghost_random(ghostobj)
                                if navigating_method==999:
                                    continue
                                if ghostobj.if_scared>0:
                                    temp_move=agentctrl.lambda_frightened(ghost_lambda,ghostobj)
                                elif ghostobj.chasemethod==1:
                                    temp_move=agentctrl.lambda_random(ghost_lambda,ghostobj)
                                elif ghostobj.chasemethod==2:
                                    temp_move=agentctrl.ghost_predict(ghost_lambda,ghostobj)
                                if temp_move!=-1:
                                    ghostobj.changeorient(temp_move)
                    movingtick+=1
                    repainting()  
                if every_event.type==29:
                    beclicked.changebackcolor((15,77,146))
                    beclicked.changelinecolor((0,0,0))
                if every_event.type==KEYDOWN and navigating_method==0:
                    if every_event.key==K_UP:
                        movevec=Direction.getmove(2)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(2)
                    elif every_event.key==K_DOWN:
                        movevec=Direction.getmove(0)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(0)
                    elif every_event.key==K_LEFT:
                        movevec=Direction.getmove(3)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(3)
                    elif every_event.key==K_RIGHT:
                        movevec=Direction.getmove(1)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(1)
                    
                    # ghostpanel()
                    
                    # if if_touch()==True:
                        # print("You died!")
                        # restart()
                        # pass
                        # print(score)
                if every_event.type==MOUSEMOTION:
                    # print("True")
                    temp_mousepos=pygame.mouse.get_pos()
                    for everybutton in Button.buttonobject:
                        if everybutton.be_clicked(temp_mousepos)==True:
                            everybutton.changebackcolor((15,77,146)) #hover
                            everybutton.changelinecolor((0,0,0))
                            # pygame.time.set_timer(29,200,1)
                        else:
                            everybutton.changebackcolor((0,114,187))
                            everybutton.changelinecolor((0,0,0))
                if every_event.type==MOUSEBUTTONDOWN:
                    temp_mousepos=pygame.mouse.get_pos()
                    #restart button
                    for everybutton in Button.buttonobject:
                        if everybutton.be_clicked(temp_mousepos)==True:
                            everybutton.changebackcolor((15,77,146))
                            everybutton.changelinecolor((0,0,0))
                            pygame.time.set_timer(29,200,1)
                            beclicked=everybutton

                            if everybutton.tag==6:
                                navigating_method = 0
                                nownavigating = 0
                                restart(nowmaptype, nownavigating)

                            if everybutton.tag==7:
                                navigating_method=0
                                nownavigating=0


                            if everybutton.tag==9:
                                navigating_method=2
                                nownavigating=2

                            if everybutton.tag==10:
                                navigating_method=3
                                nownavigating=3


                            if everybutton.tag==11:
                                navigating_method=4
                                nownavigating=4

                            if everybutton.tag==12:
                                navigating_method=5
                                nownavigating=5

                            if everybutton.tag==13:
                                navigating_method=6
                                nownavigating=6

                            if everybutton.tag==14:
                                navigating_method=7
                                nownavigating=7


                repainting()
        pygame.display.update()

