#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 13:55:28 2026

Bouncing ball test for pygame

@author: thomaspark
"""

import pygame, sys, random

pygame.init()

pygame.display.set_caption("Deltarune Chapter 6")

gameIcon = pygame.image.load("testdata/icon.png")
pygame.display.set_icon(gameIcon)

size = width, height = 720, 540

speed = [4,4]
color = 67, 28, 150

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

ball = pygame.image.load("testdata/ralsei.png")
ballrect = ball.get_rect()

gameIsOn = True

while gameIsOn:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            gameIsOn = False
            
    ballrect = ballrect.move(speed)
    
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height - 10:
        speed[1] = -speed[1]
            
    screen.fill(color)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    
    clock.tick(60)
            
print("Zamn")
 
pygame.quit()
sys.exit()