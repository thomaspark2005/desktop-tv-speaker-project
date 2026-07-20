#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 18:44:08 2026

@author: thomaspark
"""

import pygame, sys

"""Initalizing everything"""
pygame.init()

"""Fetch monitor resolution"""
info = pygame.display.Info()
monitor_width = info.current_w
monitor_height = info.current_h

width, height = monitor_height * 4 / 3, monitor_height

"""Window settings"""
pygame.display.set_caption("CRT Effect Tests")

gameIcon = pygame.image.load("testdata/icon.png")
pygame.display.set_icon(gameIcon)

"""Size of screen"""
size = width, monitor_height

class afterImage(pygame.sprite.Sprite):
    def __init__(self, source):
        super().__init__()
        
        """Load Ralsei sprite again"""
        """After images help from https://stackoverflow.com/questions/57029253/how-to-add-afterimages-in-pygame"""
        
        """Layer, put the after images under original image"""
        self._layer = 5
        
        """Copy over original image but apply blue filter"""
        self.image = source.image.copy().convert_alpha()
        self.image.fill((100, 100, 200, 100), special_flags=pygame.BLEND_ADD)
        
        """Copy over original image's position at the frame"""
        self.rect = source.rect.copy()     
        
        """How many ms the after image exists for"""
        self.timeout = 150
        
        """After image's transparency"""
        self.alpha = 255
        
    def update(self, speed, dt):
        
        """Subtract internal clock from original time created"""
        self.timeout -= dt
        
        """Subtract alpha level each frame, then set the alpha to it"""
        self.alpha -= 30
        self.image.set_alpha(self.alpha)
        
        """Kill after image sprite when timer is over"""
        if self.timeout <= 0:
            self.kill()
        

class RalseiObj(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        """Load Ralsei's sprite and set the Rect correctly"""
        self._layer = 10
        self.image = pygame.image.load("testdata/ralsei.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        """Initial timer for after images to start spawning"""
        self.afterImage_timeout = 0
        
    def update(self, speed, dt):
        
        """Move Ralsei"""
        self.rect = self.rect.move(speed)
        
        """Check for edge of screen with Ralsei's rect"""
        if self.rect.left < 0 or self.rect.right > width:
            speed[0] = -speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            speed[1] = -speed[1]
            
        """Create after images"""
        self.afterImage_timeout -= dt
        if self.afterImage_timeout <= 0:
            """How often, in ms, an after image is created"""
            self.afterImage_timeout = 25
            self.groups()[0].add(afterImage(self))
        
def main():
    
    """Speed of Ralsei"""
    speed = [5,5]
    
    BGcolor = 20, 20, 20
    
    deltaT, clock = 0, pygame.time.Clock()
    
    screen = pygame.display.set_mode(size)
        
    """Create Ralsei sprite"""
    sprites = pygame.sprite.LayeredUpdates(RalseiObj())
    
    
    """Game loop"""
    gameIsOn = True
    
    while gameIsOn:
        
        """Check if application is closed, close game if so"""
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameIsOn = False
         
        """Update all sprites"""
        sprites.update(speed, deltaT)
                
        """Update screen"""
        screen.fill(BGcolor)
        sprites.draw(screen)
        pygame.display.flip()
        
        deltaT = clock.tick(60)
        """print(str(deltaT))"""
                
main() 
pygame.quit()
sys.exit()