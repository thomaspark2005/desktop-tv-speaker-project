#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 18:44:08 2026

@author: thomaspark
"""

import pygame, sys, random

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

"""Size of app screen"""
size = width, height
screen = pygame.display.set_mode(size)

"""Classes"""

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
        self.timeout = 250
        
        """After image's transparency"""
        self.alpha = 255
        
    def update(self, speed, dt):
        
        """Subtract internal clock from original time created"""
        self.timeout -= dt
        
        """Subtract alpha level each frame, then set the alpha to it"""
        self.alpha -= 16
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
            
"""
CRT Effect Functions

Adapted/taken from https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1
"""

def apply_CRT_effects():
    apply_scanlines()
    apply_flicker()
    apply_glow()
    """apply_pixelation()"""
    """add_glitch_effect(screen)"""
    """add_color_separation(screen)"""
    
def apply_scanlines():
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y in range(0, height, 4):
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))

    screen.blit(scanline_surface, (0, 0))

def apply_pixelation():
    pixelation = 4
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // pixelation, height // pixelation))
    screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))

def apply_flicker():
    if random.randint(0, 40) == 0:
        flicker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        flicker_surface.fill((255, 255, 255, 5))
        screen.blit(flicker_surface, (0, 0))
        
def apply_glow():
    glow_surf = pygame.transform.smoothscale(screen, (width // 4, height // 4))
    glow_surf = pygame.transform.smoothscale(glow_surf, (width, height))
    glow_surf.set_alpha(100)
    screen.blit(glow_surf, (0, 0))
    
def add_glitch_effect(glitch_surface):
    shift_amount = 40
    if random.random() < 0.1:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pygame.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))
    
def add_color_separation(glitch_surface):
    color_shift = 2
    if random.random() < 0.05:
        for i in range(3):
            x_offset = random.randint(-color_shift, color_shift)
            y_offset = random.randint(-color_shift, color_shift)
            color_shift_surface = glitch_surface.copy()
            color_shift_surface.fill((0, 0, 0))
            color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
            screen.blit(color_shift_surface, (0, 0), special_flags=pygame.BLEND_ADD)    
    
def main():
    
    """Speed of Ralsei"""
    speed = [5,5]
    
    BGcolor = 32, 32, 32
    
    deltaT, clock = 0, pygame.time.Clock()
            
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
        apply_CRT_effects()
        pygame.display.flip()
        
        deltaT = clock.tick(60)
        """print(str(deltaT))"""
                
main() 
pygame.quit()
sys.exit()