from glob import glob
import pygame,random,copy
from parameter import *
from agent import Pacman,Ghost
from util import Map,Direction,checkconnecting,Button



def input_file():
    map_input=open("./map/map.txt",'r')
    tempmap=[]
    for lines in map_input.readlines():
        mapline=lines.split(" ")
        tempmap.append(list(map(int,mapline)))
    map_input.close()
    return tempmap

def imageinit():
    global apple_image,block_image,ghost_image,capsule_image
    global pacman_image_left,pacman_image_north,pacman_image_right,pacman_image_south
    global pacman_image_left_inv,pacman_image_north_inv,pacman_image_right_inv,pacman_image_south_inv
    global pacman_image_leftsmaller,pacman_image_northsmaller,pacman_image_rightsmaller,pacman_image_southsmaller
    global pacman_image_leftsmaller_inv,pacman_image_northsmaller_inv,pacman_image_rightsmaller_inv,pacman_image_southsmaller_inv
    global pacman_image_none,pacman_image_none_inv
    global ghost_left,ghost_north,ghost_right,ghost_south,ghost_scared
    
    apple_image=pygame.image.load('img/dot.jpg')
    block_image=pygame.image.load('img/block.jpg')
    capsule_image=pygame.image.load('img/pellet.jpg')
    
    pacman_image_right=pygame.image.load('img/pacman_right.png')
    pacman_image_left=pygame.image.load('img/pacman_left.png')
    pacman_image_north=pygame.image.load('img/pacman_north.png')
    pacman_image_south=pygame.image.load('img/pacman_south.png')
    pacman_image_none=pygame.image.load('img/pacman_none.png')
    
    pacman_image_right_inv=pygame.image.load('img/pacman_right_inv.png')
    pacman_image_left_inv=pygame.image.load('img/pacman_left_inv.png')
    pacman_image_north_inv=pygame.image.load('img/pacman_north_inv.png')
    pacman_image_south_inv=pygame.image.load('img/pacman_south_inv.png')
    pacman_image_none_inv=pygame.image.load('img/pacman_none_inv.png')

    pacman_image_rightsmaller=pygame.image.load('img/pacman_right_smaller.png')
    pacman_image_leftsmaller=pygame.image.load('img/pacman_left_smaller.png')
    pacman_image_northsmaller=pygame.image.load('img/pacman_north_smaller.png')
    pacman_image_southsmaller=pygame.image.load('img/pacman_south_smaller.png')
    
    pacman_image_rightsmaller_inv=pygame.image.load('img/pacman_right_smaller_inv.png')
    pacman_image_leftsmaller_inv=pygame.image.load('img/pacman_left_smaller_inv.png')
    pacman_image_northsmaller_inv=pygame.image.load('img/pacman_north_smaller_inv.png')
    pacman_image_southsmaller_inv=pygame.image.load('img/pacman_south_smaller_inv.png')
    
    ghost_right=pygame.image.load('img/ghost_right.jpg')
    ghost_left=pygame.image.load('img/ghost_left.jpg')
    ghost_north=pygame.image.load('img/ghost_north.jpg')
    ghost_south=pygame.image.load('img/ghost_south.jpg')
    ghost_scared=pygame.image.load('img/scared_ghost.png')
    
def fontinit():
    global font16,font32,font24,font28,font16_height
    font16=pygame.font.SysFont("consolas",16)
    font24=pygame.font.SysFont("consolas",24)
    font32=pygame.font.SysFont("consolas",32)
    font28=pygame.font.SysFont("consolas",28)
    font16_height=font16.get_linesize()
    
def initset():
    global main_screen
    global windows_width,windows_height
    global autospeed
    # navigating method : 0 for play, 1 for greedy, 2 for DFS
    
    pygame.init()
    pygame.display.set_caption("PACMAN")
    windows_width=block_size*map_width
    windows_height=block_size*map_height
    main_screen=pygame.display.set_mode((2*mapboarder_buffer+windows_width,windows_height/2+2*mapboarder_buffer+120))
    
    #signal 25, for flush 
    pygame.time.set_timer(25,100)
    
    #signal 26, for automating frequency
    # pygame.time.set_timer(26,autospeed)
    
    #signal 27, for moving (automatic)
    pygame.time.set_timer(27,autospeed)
    
    #signal 29,for clicking
    
    
def agentinit(temptype=0): #maptype
    global system_default_ghost_num
    tempsize=[map_height,map_width]
    if temptype==0:
        system_default_ghost_num=2
        pacman_obj=Pacman(11,18,-1)
        map_obj=Map(map_height,map_width,input_file())
        for i in range(system_default_ghost_num):
            ghost_obj=Ghost(system_default_ghost_vector[i][0],system_default_ghost_vector[i][1],0,system_default_ghost_vector[i][2])
    scores=0    
    
    
    
    
def setbutton():
    global score_text,textRect,win_text,winRect,ticks_text,tickRect,step_text,stepRect,invtime_text,invtimeRect
    global manualbutton,resetbutton,mazebutton,smallbutton,mazetwobutton
    global minimaxbutton,defaultbutton,rulebutton1,rulebutton2,defaulttwobutton
    global Q_LearningButton,SarsaButton
    
    
    #Score
    score_text=font16.render(" SCORE="+str(scores) + "  ",True,(255,255,255),(0,114,187))
    #Time
    tick_text = font16.render(" TIME=" + str(game_ticks) + "  ", True, (255, 255, 255), (0,114,187))
    
    textRect=score_text.get_rect()
    textRect.center=(265, 10)

    tickRect = tick_text.get_rect()
    tickRect.center = (350, 10)

    #Start
    resetbutton=Button("START", font16, (0, 260), (300, 50), (0, 0, 0), (255, 255, 255), (0, 114, 187), True, 6)
    
    #Manual
    manualbutton=Button("MANUAL", font16, (300, 260), (300, 50), (0, 0, 0), (255, 255, 255), (0, 114, 187), True, 7)


    #Naive
    rulebutton1=Button("*NAIVE",font16,(200, 360),(200,50),(0, 0, 0),(255,255,255),(0,114,187),True,9)

    #Sophisticated
    rulebutton2=Button("*SOPHISTICATED", font16, (400, 360), (200, 50), (0, 0, 0), (255, 255, 255), (0, 114, 187), True, 10)


    #BFS
    Q_LearningButton=Button("*GREEDY-BFS",font16,(0, 310),(200,50),(0, 0, 0),(255,255,255),(0,114,187),True,11)

    #Heuristic
    SarsaButton=Button("*HEURISTIC",font16,(0, 360),(200,50),(0, 0, 0),(255,255,255),(0,114,187),True,12)

    #DFS
    Q_LearningButton = Button("*GREEDY-DFS", font16, (200, 310), (200, 50), (0, 0, 0), (255, 255, 255), (0, 114, 187), True, 11)

    #DP
    SarsaButton = Button("*DP", font16, (400, 310), (200, 50), (0, 0, 0), (255, 255, 255), (0, 114, 187), True, 12)