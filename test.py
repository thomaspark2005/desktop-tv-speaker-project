#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 13:55:28 2026

Bouncing ball test for pygame

@author: thomaspark
"""

import pygame, sys

width, height = 720, 540

class RalseiObj(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        """Load Ralsei's sprite and set the Rect correctly"""
        self.image = pygame.image.load("testdata/ralsei.png")
        self.rect = self.image.get_rect()
        
    def update(self, speed):
        
        """Move Ralsei"""
        self.rect = self.rect.move(speed)
        
        """Check for edge of screen with Ralsei's rect"""
        if self.rect.left < 0 or self.rect.right > width:
            speed[0] = -speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            speed[1] = -speed[1]
            
        
def main():

    """Initalizing everything"""
    pygame.init()
    
    """Window settings"""
    pygame.display.set_caption("Deltarune Chapter 6")
    
    gameIcon = pygame.image.load("testdata/icon.png")
    pygame.display.set_icon(gameIcon)
    
    """Size of screen"""
    size = width, height
    
    """Speed of Ralsei"""
    speed = [4,4]
    
    BGcolor = 67, 28, 150
    
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode(size)
    
    """Create Ralsei sprite"""
    sprites = pygame.sprite.Group(RalseiObj())
    
    
    """Game loop"""
    gameIsOn = True
    
    while gameIsOn:
        
        """Check if application is closed, close game if so"""
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameIsOn = False
         
        """Move Ralsei"""
        sprites.update(speed)
                
        """Update screen"""
        screen.fill(BGcolor)
        sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)
                
    print("Done")

main() 
pygame.quit()
sys.exit()