#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:34:45 2026

This is the main script that animates the TV face

@author: thomaspark2005
"""

import pygame, sys, random

"""Initalizing everything"""
pygame.init()

"""Fetch monitor resolution"""
info = pygame.display.Info()
monitor_width = info.current_w
monitor_height = info.current_h

"""Set width to be 4/3rds of the monitor's height"""
width = 800
height = 480

"""Window settings"""
pygame.display.set_caption("TV Speaker")

"""Icon setup"""
gameIcon = pygame.image.load("testdata/icon.png")
pygame.display.set_icon(gameIcon)

"""Size of app screen"""
size = width, height
screen = pygame.display.set_mode(size)

"""Global variables"""

isBlinking = False
afterImageFlag = True

"""
Face state variable:

0 = normal, blinking
1 = singing

"""
faceState = 0

"""Classes"""

"""
afterImage class

Purpose: makes copies of a sprite as it moves, giving the illusion of phosphor burn in
"""
class afterImage(pygame.sprite.Sprite):
    
    """Constructor, needs a source sprite to take from"""
    def __init__(self, source):
        super().__init__()
        
        """After images help from https://stackoverflow.com/questions/57029253/how-to-add-afterimages-in-pygame"""
        
        """Layer, put the after images under original image"""
        self._layer = 5
        
        """Copy over original image but apply blue filter"""
        self.image = source.image.copy().convert_alpha()
        self.image.fill((0, 0, 200, 100), special_flags=pygame.BLEND_ADD)
        
        """Copy over original image's position at the frame"""
        self.rect = source.rect.copy()     
        
        """How many ms the after image exists for"""
        self.timeout = 100
        
        """After image's initial transparency"""
        self.alpha = 255
        
    """Update function which runs each frame, needs input of dt"""
    def update(self, speed, dt):
        
        """Subtract internal clock from original time created"""
        self.timeout -= dt
        
        """Subtract alpha level each frame, then set the alpha to it"""
        self.alpha -= 32
        self.image.set_alpha(self.alpha)
        
        """Kill sprite after image sprite when timer is over"""
        if self.timeout <= 0:
            self.kill()
        
"""
Test object for various functions
"""
class TestFaceObj(pygame.sprite.Sprite):
    
    """Constructor"""
    def __init__(self):
        super().__init__()
        
        """Load Test Face image"""
        self._layer = 10
        self.image = pygame.image.load("sprites/testface.png").convert_alpha()
        
        """Scale by 1/2"""
        self.image = pygame.transform.scale_by(self.image, 0.5)
        
        """Set the Rect correctly"""
        self.rect = self.image.get_rect()
        
        """Move to center"""
        self.rect.center = screen.get_rect().center
        
        """Initial timer for after images to start spawning"""
        self.afterImage_timeout = 0
        
    """Update function which runs each frame, needs speed"""
    def update(self, speed, dt):
        
        """Move TestFace with speed"""
        self.rect = self.rect.move(speed)
        
        """
        Check for edge of screen with TestFace's rect
        Redirect test face's movement
        """
        if self.rect.left < 0 or self.rect.right > width:
            speed[0] = -speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            speed[1] = -speed[1]
            
        """Create after images"""
        self.afterImage_timeout -= dt
        if self.afterImage_timeout <= 0:
            """How often, in ms, an after image is created"""
            self.afterImage_timeout = 25
            """Create after image sprite using constructor"""
            self.groups()[0].add(afterImage(self))

"""
Eye class

Purpose: holds logic for eyes, including sprites, blinking, and necessary updates
"""
class Eye(pygame.sprite.Sprite):
    
    """Class shared variables"""
    
    """Blinking variables"""
    blink_duration = 20
    blink_elapsed = 0
        
    """Load eye sprites and scale them down by 1/2"""
    eyeSprite_dot = pygame.transform.scale_by(pygame.image.load("sprites/eyes/eyes_dot.png").convert_alpha(), 0.5)
    eyeSprite_closedDown = pygame.transform.scale_by(pygame.image.load("sprites/eyes/eyes_closed-down.png").convert_alpha(), 0.5)

    """shrink sprites"""
    
    """Constructor and object variables"""
    def __init__(self, objName):
        super().__init__()
        
        """Name of Eye, either left or right"""
        self.name = objName
        
        """Sprite layer"""
        self._layer = 10
                
        """Set initial sprite of eye, dot"""
        self.image = Eye.eyeSprite_dot
        
        """Set the Rect correctly"""
        self.rect = self.image.get_rect()
        
        """Initial placement of eyes"""
        self.rect.center = screen.get_rect().center
        
        """Initial timer for after images to start spawning"""
        self.afterImage_timeout = 0
        
        """Variables to store eye sprites"""
        self.prev_eye_sprite = 0
        
        """Store previous location before sprite change"""
        self.prev_topleft = (0,0)
        
    """Update function which runs every frame"""
    def update(self, speed, dt):
        
        """Bring down global variables"""
        global isBlinking
        global afterImageFlag
        
        if isBlinking:
            """Check if elapsed blinking time is lesser than blinking duration"""
            if Eye.blink_elapsed < Eye.blink_duration:
                """Check if current image is not the blinking eye"""
                if self.image is not Eye.eyeSprite_closedDown:
                    
                    """Save previous topleft of previous rect and previous eye image"""
                    self.prev_topleft = self.rect.topleft
                    self.prev_eye_sprite = self.image
                    
                    """Set image to blinking eye"""
                    self.image = Eye.eyeSprite_closedDown
                    
                    """Reset rect"""
                    self.rect = self.image.get_rect()
                    
                    """Position eyes if depending on which one they are"""
                    """These functions use the previous topleft boxes to be more adaptive :)"""
                    if self.name == "Left":
                        self.rect.topleft = (self.prev_topleft[0] - 90, self.prev_topleft[1])
                    else:
                        self.rect.topleft = (self.prev_topleft[0] - 10, self.prev_topleft[1])
            else:
                """When duration has ran through, set image to previous eye sprite and previous rect"""
                self.image = self.prev_eye_sprite
                self.rect = self.image.get_rect()
                """Reset position of eyes"""
                self.rect.topleft = self.prev_topleft
                    
        """Create after images"""
        if afterImageFlag:
            """Subtract afterimage creation with delta t"""
            self.afterImage_timeout -= dt
            if self.afterImage_timeout <= 0:
                """How often, in ms, an after image is created"""
                self.afterImage_timeout = 25
                self.groups()[0].add(afterImage(self))
        
      
class Mouth(pygame.sprite.Sprite):
    """Constructor"""
    def __init__(self):
        super().__init__()
        
        """Sprite layer"""
        self._layer = 10
        
        """Load mouth sprites"""
        self.mouthSprite_D = pygame.image.load("sprites/mouth/mouth_D.png").convert_alpha()
        
        """Set initial sprite of mouth, D"""
        self.image = self.mouthSprite_D
               
        """Scale by 1/2"""
        self.image = pygame.transform.scale_by(self.image, 0.5)
        
        """Set the Rect correctly"""
        self.rect = self.image.get_rect()
                        
        """Initial timer for after images to start spawning"""
        self.afterImage_timeout = 0
        
    """Update function which runs every frame, needs dt"""
    def update(self, speed, dt):
            
        """Create after images"""
        self.afterImage_timeout -= dt
        if self.afterImage_timeout <= 0:
            """How often, in ms, an after image is created"""
            self.afterImage_timeout = 25
            self.groups()[0].add(afterImage(self))
    
"""Animation functions"""

"""Other functions"""
    
"""
CRT Effect Functions

Adapted/taken from https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1
"""

def apply_CRT_effects():
    apply_flicker()
    apply_glow()
    apply_pixelation()
    
    apply_scanlines()
    
    """add_glitch_effect(screen)"""
    
def apply_scanlines():
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y in range(0, height, 4):
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))

    screen.blit(scanline_surface, (0, 0))

def apply_pixelation():
    pixelation = 2
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
    
"""Main function"""
def main():
    
    """Bring down global variables"""
    global isBlinking        
    global faceState
    
    """Test speed"""
    speed = [0,0]
    
    """Color of the bckground"""
    BGcolor = 32, 32, 32
    
    """Set delta t to 0, set up game clock"""
    deltaT, clock = 0, pygame.time.Clock()
            
    """Create sprite group"""
    sprites = pygame.sprite.LayeredUpdates()
    
    """Create face sprites and add them to group"""
    LeftEye = Eye("Left")
    RightEye = Eye("Right")
    RealMouth = Mouth()
    sprites.add(LeftEye, RightEye, RealMouth)
    
    """Place face sprites in initial positions"""
    LeftEye.rect.topleft = (316, 131)
    RightEye.rect.topleft = (449, 131)
    RealMouth.rect.center = screen.get_rect().center
    RealMouth.rect.top = 220
    
    """Game loop, run this code every frame"""
    gameIsOn = True
    
    while gameIsOn:
        
        """Check if application is closed, close game if so"""
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameIsOn = False
                
        """Blink animation, run if random number roll succeeds, if face is not blinking, and if the face is in a neutral state"""
        if (random.randint(0, 100) == 0) and (not isBlinking) and (faceState == 0):
            isBlinking = True
            Eye.blink_timer = 0
        
        """Update blink_elapsed out here"""
        if isBlinking:
            Eye.blink_elapsed += 1
            
        """Update all sprites"""
        sprites.update(speed, deltaT)
        
        """Check if blink_elapsed is greater than blink_duration"""
        if (Eye.blink_elapsed >= Eye.blink_duration) and isBlinking:
            """End blinking state"""
            isBlinking = False
            Eye.blink_elapsed = 0
                
        """Draw bg, sprites, and CRT effects to screen"""
        screen.fill(BGcolor)
        sprites.draw(screen)
        apply_CRT_effects()
        
        """4:3 boundary"""
        pygame.draw.rect(screen, "blue", (80, 0 , 640, 480), 1)
        
        """Draw all sprites' rects for ease"""
        """for sp in sprites:
            pygame.draw.rect(screen, (255, 0, 0), sp.rect, 1) """
            
        pygame.display.flip()
        
        deltaT = clock.tick(60)
        print(str(deltaT))

"""Run main"""                
main()

"""Quit if program finishes"""
pygame.quit()
sys.exit()