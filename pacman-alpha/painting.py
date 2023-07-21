from parameter import *
import pygame
import srcload
from util import Map,Button
import math
from agent import Ghost,Pacman

def paintingbuttonborder(tempbutton:Button):
    tempposition=tempbutton.getposition()
    tempsize=tempbutton.getsize()
    templine=tempbutton.getline()
    pygame.draw.line(srcload.main_screen,templine,tempposition,(tempposition[0]+tempsize[0],tempposition[1]),width=2)
    pygame.draw.line(srcload.main_screen,templine,tempposition,(tempposition[0],tempposition[1]+tempsize[1]),width=2)
    pygame.draw.line(srcload.main_screen,templine,(tempposition[0],tempposition[1]+tempsize[1]),(tempposition[0]+tempsize[0],tempposition[1]+tempsize[1]),width=2)
    pygame.draw.line(srcload.main_screen,templine,(tempposition[0]+tempsize[0],tempposition[1]),(tempposition[0]+tempsize[0],tempposition[1]+tempsize[1]),width=2)

def repainting():
    global ifwin
    srcload.main_screen.fill((0,0,0))
    
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    temppacman=Pacman.pacmanobject
    tempghostvec=Ghost.ghostvector
    #painting map
    if True:
        for i in range(map_height):
            for j in range(map_width):
                if tempmap.get_value(i,j)==1:
                    srcload.main_screen.blit(srcload.block_image,(j*20+mapboarder_buffer,i*20+mapboarder_buffer,20,20))
                elif tempmap.get_value(i,j)==0 and tempmap.get_ifeaten(i,j)==1 and tempmap.get_ifcapsule(i,j)==False:
                    srcload.main_screen.blit(srcload.apple_image,(j*20+mapboarder_buffer,i*20+mapboarder_buffer,20,20))
                elif tempmap.get_value(i,j)==0 and tempmap.get_ifeaten(i,j)==1:
                    srcload.main_screen.blit(srcload.capsule_image,(j*20+mapboarder_buffer,i*20+mapboarder_buffer,20,20))
    
    #painting pacman
    # flushpacman()
    if temppacman.getmouthopen()==2:
        # print("flash"+str(pacman_flash_x)+" "+str(pacman_flash_y))
        if temppacman.getpreviousorient()==3:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_left_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_left,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        elif temppacman.getpreviousorient()==1:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_right_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_right,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        elif temppacman.getpreviousorient()==2:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_north_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_north,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        elif temppacman.getpreviousorient()==0:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_south_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_south,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        else:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_none_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_none,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
    elif temppacman.getmouthopen()==1:
        if temppacman.getpreviousorient()==3:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_leftsmaller_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_leftsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        elif temppacman.getpreviousorient()==1:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_rightsmaller_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_rightsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        elif temppacman.getpreviousorient()==2:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_northsmaller_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_northsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        elif temppacman.getpreviousorient()==0:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_southsmaller_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_southsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        else:
            if temppacman.invtime>0:
                srcload.main_screen.blit(srcload.pacman_image_none_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
            else:
                srcload.main_screen.blit(srcload.pacman_image_none,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
    else:
        if temppacman.invtime>0:
            srcload.main_screen.blit(srcload.pacman_image_none_inv,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        else:
            srcload.main_screen.blit(srcload.pacman_image_none,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
    #painting ghost

    for ghostobj in Ghost.ghostvector:
        tempghostpos=ghostobj.getposition()
        if ghostobj.if_scared==0:
            if ghostobj.getorient()<=0:
                srcload.main_screen.blit(srcload.ghost_south,(ghostobj.ghost_flash_y*block_size+mapboarder_buffer,ghostobj.ghost_flash_x*block_size+mapboarder_buffer))
            if ghostobj.getorient()==1:
                srcload.main_screen.blit(srcload.ghost_right,(ghostobj.ghost_flash_y*block_size+mapboarder_buffer,ghostobj.ghost_flash_x*block_size+mapboarder_buffer))
            if ghostobj.getorient()==2:
                srcload.main_screen.blit(srcload.ghost_north,(ghostobj.ghost_flash_y*block_size+mapboarder_buffer,ghostobj.ghost_flash_x*block_size+mapboarder_buffer))
            if ghostobj.getorient()==3:
                srcload.main_screen.blit(srcload.ghost_left,(ghostobj.ghost_flash_y*block_size+mapboarder_buffer,ghostobj.ghost_flash_x*block_size+mapboarder_buffer))
        else:
            srcload.main_screen.blit(srcload.ghost_scared,(ghostobj.ghost_flash_y*block_size+mapboarder_buffer,ghostobj.ghost_flash_x*block_size+mapboarder_buffer))


    
    #painting score
    score_text=srcload.font16.render(" SCORE="+str(tempmap.get_score()) + "  ",True,(255,255,255),(0,114,187))
    #painting time
    tick_text = srcload.font16.render(" TIME=" + '%d' % (tempmap.get_ticks() / 10) + "  ", True, (255, 255, 255),(0,114,187))

    srcload.main_screen.blit(score_text, srcload.textRect)

    srcload.main_screen.blit(tick_text,srcload.tickRect)
    
    for everybutton in Button.buttonobject:
        tempposition=everybutton.getposition()
        tempsize=everybutton.getsize()
        pygame.draw.rect(srcload.main_screen,everybutton.getbg(),(tempposition[0],tempposition[1],tempsize[0],tempsize[1]))
        srcload.main_screen.blit(everybutton.buttonobj,everybutton.buttonrect)
        paintingbuttonborder(everybutton)
    
    