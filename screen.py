#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:34:45 2026

This is the main script that animates the TV face

@author: thomaspark2005
"""

import pygame, sys, random

# =============================================================================
# Initialization
# =============================================================================

# Initalizing pygame
pygame.init()

# Fetch monitor resolution
info = pygame.display.Info()
monitor_width = info.current_w
monitor_height = info.current_h

# TODO finalize size of screen
# Set width to be 4/3rds of the monitor's height
width = 800
height = 480

# Application window label
# TODO Come up with catchy name for this thing
pygame.display.set_caption("TV Speaker")

# TODO Make a custom icon
# Icon setup
icon = pygame.image.load("testdata/icon.png")
pygame.display.set_icon(icon)

# Size of app screen
size = width, height
screen = pygame.display.set_mode(size)

# Font and surface for debug text
font = pygame.font.Font(None, 20)
text1 = pygame.surface.Surface((0,0))
text2 = pygame.surface.Surface((0,0))
text3 = pygame.surface.Surface((0,0))

# Other global variables

afterImageFlag = True

changeLeftEye = False
changeRightEye = False
changeMouth = False
LeftEyeNum = 0
RightEyeNum = 0
MouthNum = 0

# =============================================================================
# Classes
# =============================================================================

class afterImage(pygame.sprite.Sprite):
    """Pygame sprite class which represents an after image of a preexisting sprite."""
    
    def __init__(self, source):
        """
        Initialize the after image sprite with correct variables.

        :param source: a sprite from which an after image is created
        """
        # Initialize pygame sprite
        super().__init__()
        
        # After images help from https://stackoverflow.com/questions/57029253/how-to-add-afterimages-in-pygame
        
        # Layer, put the after images under original image
        self._layer = 5
        
        # Copy over original image
        self.image = source.image.copy().convert_alpha()
        # Make after image slighty transparent, slightly blue
        self.image.fill((0, 0, 200, 100), special_flags=pygame.BLEND_ADD)
        
        # Copy over original image's position on the screen
        self.rect = source.rect.copy()     
        
        # How many ms the after image exists for, in frames
        self.timeout = 120
        
        # After image's initial transparency
        self.alpha = 255
        
    def update(self, dt):
        """
        Update function for the after image sprite.

        :param dt: time between each frame (delta t)
        """
        # Subtract internal clock by delta t
        self.timeout -= dt
        
        # Subtract alpha level each frame, then set the sprite's alpha to it
        self.alpha -= 48
        self.image.set_alpha(self.alpha)
        
        # Kill sprite after image sprite when timer has counted down
        if self.timeout <= 0:
            self.kill()
        
class TestFaceObj(pygame.sprite.Sprite):
    """An object to test what the face should look like in various states."""
    def __init__(self):
        """Constructor for test object."""
        
        # Initialize pygame sprite
        super().__init__()
        
        # Load Test Face image
        # TODO Load another face in
        self._layer = 10
        self.image = pygame.image.load("sprites/testface.png").convert_alpha()
        
        # Scale by 1/2
        self.image = pygame.transform.scale_by(self.image, 0.5)
        
        # Set the Rect correctly
        self.rect = self.image.get_rect()
        
        # Move to center
        self.rect.center = screen.get_rect().center
        
        # Initial timer for after images to start spawning
        self.afterImage_timeout = 0
        
    def update(self, dt, afterImageGroup):
        """Update function which runs each frame.
        
        :param dt: Change in time since last frame
        :param afterImageGroup: Sprite group containing after images for each sprite
        """
        # """Move TestFace with speed"""
        # self.rect = self.rect.move(speed)
        
        # """
        # Check for edge of screen with TestFace's rect
        # Redirect test face's movement
        # """
        # if self.rect.left < 0 or self.rect.right > width:
        #     speed[0] = -speed[0]
        # if self.rect.top < 0 or self.rect.bottom > height:
        #     speed[1] = -speed[1]
            
        # Create after images
        self.afterImage_timeout -= dt
        if self.afterImage_timeout <= 0:
            # How often, in ms, an after image is created
            self.afterImage_timeout = 25
            # Create after image sprite using constructor
            afterImageGroup.add(afterImage(self))

class Eye(pygame.sprite.Sprite):
    """Holds logic for eyes, including sprites, blinking, and necessary updates."""
    
    # Blinking variables
    blink_duration = 20
    blink_elapsed = 0
        
    # All eye objects have access to the spriteImages dictionary which holds ImageContainers for the eyes
    spriteImages = {}
    
    def __init__(self, objName):
        """
        Constructor for Eye object.
        
        :param objName: Name for the object, most best used as a key in the distDict dictionary, so name it the same as your object
        """
        # Initialize pygame sprite
        super().__init__()
        
        # Name of Eye, either left or right
        self.name = objName
        
        # Sprite layer
        self._layer = 10
                
        # Load eye sprites into shared spriteImages dictionary (only needs to run once)
        if not Eye.spriteImages:
            Eye.spriteImages = Eye.loadSpriteImages()
        
        # Set initial sprite of eye, dot
        self.currImageContainer = Eye.spriteImages["dot"]
        self.image = self.currImageContainer.image
        
        # Set the Rect correctly
        self.rect = self.image.get_rect()
        
        # Initial placement of eyes
        self.rect.center = screen.get_rect().center
        
        # Initial timer for after images to start spawning
        self.afterImage_timeout = 0
        
        # Variable to store previous eye sprite image's name
        self.prev_ImageName = ""
        
        # Used when edits to the normal center of the sprite are needed (i.e. when the sprite image is changed)
        self.changeFromCenter = (0,0)
        
    def loadSpriteImages():
        """
        Loads images for the Eye object as ImageContainer objects.
        
        Returns:
            Dictionary with keys being the name of the image and the value being the requested ImageContainer
        """
        # Eye sprites
        # .
        eyes_dot = ImageContainer("dot", "sprites/eyes/eyes_dot.png", 0.5, (0,0), (0,0), (0,0))
        # u
        eyes_closedDown = ImageContainer("closedDown", "sprites/eyes/eyes_closed-down.png", 0.5, (-20,0), (20,0), (0,0))
        # ^
        eyes_closedUp = ImageContainer("closedUp", "sprites/eyes/eyes_closed-up.png", 0.5, (-20,0), (20,0), (0,0))
        
        # Create dictionary to return
        images = {
            "dot" : eyes_dot,
            "closedDown" : eyes_closedDown,
            "closedUp" : eyes_closedUp
            }
        
        return images
        
    def setChangeDependingOnEyes(self):
        """Updates the Eye object's changeFromCenter tuple based on if they are the Left or Right eye"""
        # Position eyes if depending on which one they are
        # Change the position the eyes in relation to the usual center calculated at Face initialization
        if self.name == "LeftEye":
            self.changeFromCenter = self.currImageContainer.LeftEyeOffset
        elif self.name == "RightEye":
            self.changeFromCenter = self.currImageContainer.RightEyeOffset
        else:
            # Failsafe in case Eyes are not named LeftEYe or RightEye
            print("What, do you have a third eye?")
            
    def changeImageTo(self, imageName):
        """
        Changes self.image to be the requested image and updates the offsets needed for placement.
        
        :param imageName: Name of the new image for the Eye sprite
        """
        # Load requested ImageContainer and pull info from it
        self.currImageContainer = Eye.spriteImages[imageName]
        self.image = self.currImageContainer.image
        self.rect = self.image.get_rect()
        # Pull and change offsets
        self.setChangeDependingOnEyes()
        
    def afterImgUpdate(self, dt, afterImageGroup):
        """
        Specfically updates the after images, so that the Face can correct the face sprites' positions first.
        
        :param dt: Change in time since last frame
        :param afterImageGroup: Main loop's sprite group containing after images for each sprite
        """
        # Create after images if flag is set
        if afterImageFlag:
            # Subtract afterimage creation with delta t
            self.afterImage_timeout -= dt
            if self.afterImage_timeout <= 0:
                # How often, in ms, an after image is created
                self.afterImage_timeout = 25
                afterImageGroup.add(afterImage(self))
    
    def update(self, isBlinking):
        """
        Update function which runs each frame.
        
        :param dt: Change in time since last frame
        :param afterImageGroup: Sprite group containing after images for each sprite
        :param isBlinking: Flag which determines whether eye should be blinking
        """ 
        # Blinking operation
        if isBlinking:
            # Check if elapsed blinking time is lesser than blinking duration
            if Eye.blink_elapsed < Eye.blink_duration:
                
                # Check if current image is not the blinking eye
                if self.image is not Eye.spriteImages["closedDown"].image:
                    
                    # Store current eye image name to go back to later
                    self.prev_ImageName = self.currImageContainer.name
                    
                    # Set image to blinking eye image
                    self.changeImageTo("closedDown")
            else:
                # When blinking duration has ran through, set image to previous eye sprite,  previous rect, and previous offsets
                self.changeImageTo(self.prev_ImageName)
                
        # TODO: Debug feature
        global changeLeftEye, changeRightEye, LeftEyeNum, RightEyeNum
        if changeLeftEye and (self.name == "LeftEye"):
            LeftEyeNum += 1
            if LeftEyeNum > 2:
                LeftEyeNum = 0
            newEye = list(Eye.spriteImages.values())[LeftEyeNum]
            self.changeImageTo(newEye.name)
            changeLeftEye = False
            
        if changeRightEye and (self.name == "RightEye"):
            RightEyeNum += 1
            if RightEyeNum > 2:
                RightEyeNum = 0
            newEye = list(Eye.spriteImages.values())[RightEyeNum]
            self.changeImageTo(newEye.name)
            changeRightEye = False
                          
class Mouth(pygame.sprite.Sprite):
    """Holds logic for mouth, including sprites and necessary updates."""
    
    spriteImages = {}
    
    def __init__(self, objName):
        """
        Constructor for Mouth object.
        
        :param objName: Name for the object, most best used as a key in the distDict dictionary, so name it the same as your object
        """
        # Initialize pygame sprite
        super().__init__()
        
        # Sprite name
        self.name = objName
        
        # Sprite layer 
        self._layer = 10
        
        # Load mouth sprites
        Mouth.spriteImages = Mouth.loadSpriteImages()
        
        # Set initial sprite of mouth, D shape
        self.image = Mouth.spriteImages["D"].image
                       
        # Set the Rect correctly
        self.rect = self.image.get_rect()
                        
        # Initial timer for after images to start spawning
        self.afterImage_timeout = 0
        
        # Used when edits to the normal center of the sprite are needed (i.e. when the sprite image is changed)
        self.changeFromCenter = (0,0)
                
    def loadSpriteImages():
        """
        Loads images for the Mouth object as ImageContainer objects.
        
        Returns:
            Dictionary with keys being the name of the image and the value being the requested ImageContainer
        """
        # Mouth sprites
        mouth_D = ImageContainer("D", "sprites/mouth/mouth_D.png", 0.5, (0,0), (0,0), (0,0))
        mouth_O = ImageContainer("O", "sprites/mouth/mouth_O.png", 0.5, (0,0), (0,0), (0,0))
        mouth_Zero = ImageContainer("zero", "sprites/mouth/mouth_Zero.png", 0.5, (0,0), (0,0), (0,0))
        mouth_dot = ImageContainer("dot", "sprites/mouth/mouth_dot.png", 0.5, (0,0), (0,0), (0,0))
        mouth_smileClosed = ImageContainer("smileClosed", "sprites/mouth/mouth_(.png", 0.5, (0,0), (0,0), (0,0))
        
        # Create dictionary to return
        images = {
            "D" : mouth_D,
            "O" : mouth_O,
            "zero" : mouth_Zero,
            "dot" : mouth_dot,
            "smileClosed" : mouth_smileClosed
            }
        
        return images 
    
    def changeImageTo(self, imageName):
        """
        Changes self.image to be the requested image and updates the offsets needed for placement.
        
        :param imageName: Name of the new image for the Mouth sprite
        """
        # Load requested ImageContainer and pull info from it
        self.currImageContainer = Mouth.spriteImages[imageName]
        self.image = self.currImageContainer.image
        self.rect = self.image.get_rect()
        # Pull and change offsets
        self.changeFromCenter = self.currImageContainer.MouthOffset
        
    def afterImgUpdate(self, dt, afterImageGroup):
        """
        Specfically updates the after images, so that the Face can correct the face sprites' positions first.
        
        :param dt: Change in time since last frame
        :param afterImageGroup: Main loop's sprite group containing after images for each sprite
        """
        # Create after images if flag is set
        if afterImageFlag:
            # Subtract afterimage creation with delta t
            self.afterImage_timeout -= dt
            if self.afterImage_timeout <= 0:
                # How often, in ms, an after image is created
                self.afterImage_timeout = 25
                afterImageGroup.add(afterImage(self))
        
    def update(self, isBlinking):
        """Update function which runs each frame.
        
        :param dt: Change in time since last frame
        :param afterImageGroup: Sprite group containing after images for each sprite
        :param isBlinking: Unused here
        """
        # TODO: Debug feature
        global changeMouth, MouthNum
        if changeMouth:
            MouthNum += 1
            if MouthNum > 4:
                MouthNum = 0
            newEye = list(Mouth.spriteImages.values())[MouthNum]
            self.changeImageTo(newEye.name)
            changeMouth = False
    
class ImageContainer():
    """
    Contains both an image for a sprite and its associated offsets from the center.
        
    These containers should not have duplicates.
    
    Instance variables:
        - name (string)
        - spriteImage (pygame.image)
        - LeftEyeOffset  (x,y tuple)
        - RightEyeOffset (x,y tuple)
        - MouthOffset (x,y tuple)
    """
    def __init__(self, objName, imagePathname, scaleAmt, leftTuple, rightTuple, mouthTuple):
        """
        Constructor for ImageContainer object.
        
        :param objName: Name of this container; i.e. the name of the image
        :param imagePathname: Where sprite's image is located in the files
        :param scaleAmt: How 
        """
        # Set name
        self.name = objName
        # Try to load image found in source
        try:
            self.image = pygame.transform.scale_by(pygame.image.load(imagePathname).convert_alpha(), scaleAmt)
        except pygame.error as e:
            # If we get an error, print error message and quit program
            print("Error! Pygame details: " + str(e))
            pygame.quit()
            sys.exit()
        # Offsets
        self.LeftEyeOffset = leftTuple
        self.RightEyeOffset = rightTuple
        self.MouthOffset = mouthTuple
        
    def updateScaleAmount(self, scaleAmt):
        """
        Sets scale for sprite image.
        
        :param leftTuple: New offset for the LeftEye
        :param rightTuple: New offset for the RightEye
        :param mouthTuple: New offset for Mouth
        """
        self.spriteImage = pygame.transform.scale_by(self.spriteImage, scaleAmt)
    
    def updateOffsets(self, leftTuple, rightTuple, mouthTuple):
        """
        Sets offsets for sprite image.
        
        :param leftTuple: New offset for the LeftEye
        :param rightTuple: New offset for the RightEye
        :param mouthTuple: New offset for Mouth
        """
        self.LeftEyeOffset = leftTuple
        self.RightEyeOffset = rightTuple
        self.MouthOffset = mouthTuple

class Face():
    """
    Main object of the screen.
    
    Has 2 eye objects and a mouth object.
    
    Animates the face and keeps track of its position via Vector2 objects.
    """
    
    def __init__(self, faceSpriteGroup):
        """
        Constructor for Face object.
        
        :param faceSpriteGroup: Group in which the sprites need to be put into
        """
        # Face parts belong in this group
        self.faceSprites = faceSpriteGroup

        # Create face parts
        LeftEye = Eye("LeftEye")
        RightEye = Eye("RightEye")
        RealMouth = Mouth("RealMouth")
        
        # Add parts to given sprite group
        self.faceSprites.add(LeftEye, RightEye, RealMouth)
        
        # Face sprite inital placements
        LeftEye.rect.topleft = (316, 131)
        RightEye.rect.topleft = (449, 131)
        
        RealMouth.rect.center = screen.get_rect().center
        RealMouth.rect.top = 220
        
        # Face variables
        self.isBlinking = False
        
        # TODO Implement this
        # Face state variable:
        # 0 = normal, blinking
        # 1 = moving, not blinking
        # 2 = singing
        self.faceState = 0
        
        # Movement variables
        self.movementDuration = 1.0
        self.elapsedTime = 0.0
        self.isMoving = False
        
        # Set currentPosition of face as (center of the mouth, midpoint between LeftEye's top and RealMouth's bottom)
        self.currPos = pygame.math.Vector2(RealMouth.rect.centerx, (LeftEye.rect.top + (RealMouth.rect.top + RealMouth.rect.height))/2)
        
        # Other positions needed for movement
        # TODO: edit this so that its not random
        self.targetPos = pygame.math.Vector2(random.randint(80, 640), random.randint(0, 480))
        self.startPos = self.currPos.copy()
        
        # Dictionary definitions
        self.distDict = {}
        
        # For each sprite in the group, calculate its distance to the center of the face, then update the dictionary
        for sp in self.faceSprites:
            self.distDict.update({sp.name: self.calculateCenterDistance(sp)})
        
    def calculateCenterDistance(self, faceSprite):
        """
        Calculates distance from a given faceSprite's rect's center to the center of the face, returns a tuple of distances in the x and y axes.
        
        This should be run during initialization and whenever a face part's distance changes!
        """
        # Subtract the sprite's center x from the face's center x, same for y's
        dist = (faceSprite.rect.center[0] - self.currPos[0], faceSprite.rect.center[1] - self.currPos[1])
        return dist
        
    def setDestination(self, xDest, yDest):
        """
        Sets the target position of the face to the given x and y.
        
        :param xDest: Target x-coordinate
        :param yDest: Target y-coordinate
        """
        self.targetPos.update(xDest, yDest)
        
    def startMoving(self):
        """Sets the correct variables to ensure that the face begins to move."""
        self.isMoving = True
        self.elapsedTime = 0.0
        self.startPos = self.currPos.copy()
        
    def moveTo(self, xDest, yDest, duration):
        """
        Moves the face to the desired coordinates in an specified duration of time.
        
        :param xDest: Target x-coordinate
        :param yDest: Target y-coordinate
        :param duration: Time, in seconds, movement will occur over
        """
        global text1
        
        self.targetPos.update(xDest, yDest)
        self.startMoving()
        self.movementDuration = duration
        
        # TODO: Remove this or comment out
        # Print debugging info to screen
        text1 = font.render("Going to (" + str(xDest) + ", " + str(yDest) + ") in " + str(duration) + " seconds.", True, "white")
        
    def drawPositions(self):
        """Draws the current, previous, and destination Vector2s associated with this face object."""
        pygame.draw.circle(screen, "yellow", self.currPos, 10)
        pygame.draw.circle(screen, "green", self.targetPos, 10)
        pygame.draw.circle(screen, "red", self.startPos, 10)
        
    def drawFace(self):
        """Draws the face's sprites to the screen after they've been updated."""
        self.faceSprites.draw(screen)
        
    def update(self, dt, afterImageSpriteGroup):
        """
        Update function which runs each frame.
        
        :param dt: Change in time since last frame
        :param afterImageSpriteGroup: Sprite group containing after images for each sprite
        """
        # Blink animation, run if random number roll succeeds, if face is not blinking, and if the face is in a neutral state
        if (random.randint(0, 100) == 0) and (not self.isBlinking) and (self.faceState == 10):
            self.isBlinking = True
            Eye.blink_timer = 0
            
        # Update blink_elapsed out here before sprite updates
        if self.isBlinking:
            Eye.blink_elapsed += 1
            
        # Let all face sprites update 
        self.faceSprites.update(self.isBlinking)
        
        # Check if blink_elapsed is greater than blink_duration
        if (Eye.blink_elapsed >= Eye.blink_duration) and self.isBlinking:
            # End blinking state
            self.isBlinking = False
            Eye.blink_elapsed = 0
        
        # Move center towards target via easing function
        if self.isMoving:
            # Divide dt by 1000 to get it in terms of seconds
            self.elapsedTime += (dt / 1000.0)
            
            # Bound t to be in between 0 and 1
            t = min(self.elapsedTime/self.movementDuration, 1.0)
            
            # Apply using the ease in and out function, return proper t value
            smooth_t = ease_in_and_out(t)
            
            # Use lerp to move center to target with correct movement
            self.currPos = self.startPos.lerp(self.targetPos, smooth_t)
        
            # When t is finished, stop movement
            if t >= 1.0:
                self.isMoving = False
                
            # Update sprites' positions to go with center
            for sp in self.faceSprites:
                # Update the sprite's rect's center to be a constant distance as defined in the distDict + whatever change the sprite image requires
                sp.rect.center = (self.currPos.x + self.distDict[sp.name][0] + sp.changeFromCenter[0], self.currPos.y + self.distDict[sp.name][1] + sp.changeFromCenter[1])
                    
        # Let all face sprites update their after images after enforcing their positions
        for sp in self.faceSprites:
            sp.afterImgUpdate(dt, afterImageSpriteGroup)
                  
                
# =============================================================================
# Animation functions
# =============================================================================

def ease_in_and_out(t):
    """
    Smoothstep easing function.

    Returns t^2 * (3 - 2 * t).
    """
    return t * t * (3 - 2 * t)

# =============================================================================
# CRT Effect Functions
#
# Adapted/taken from https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1
# =============================================================================

def apply_CRT_effects():
    """Applies all CRT screen effects, in the following order."""
    apply_flicker()
    apply_glow()
    apply_pixelation()
    apply_scanlines()
    
    # add_glitch_effect(screen)
    
def apply_scanlines():
    """
    Creates semi-translucent scanlines on the screen.
    
    This needs to be drawn last or else other objects will appear in front of them.
    """
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y in range(0, height, 4):
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))

    screen.blit(scanline_surface, (0, 0))

def apply_pixelation():
    """
    Pixelates the screen further than it already is.
    
    It does this via shrinking the screen by the pixelation variable and displaying it back to the screen.
    """
    pixelation = 2
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // pixelation, height // pixelation))
    screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))

def apply_flicker():
    """Randomly allows a solid, opaque white screen to be drawn sometimes, imitating screen flicker."""
    if random.randint(0, 40) == 0:
        flicker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        flicker_surface.fill((255, 255, 255, 5))
        screen.blit(flicker_surface, (0, 0))
        
def apply_glow():
    """Makes elements glow by copying the screen, shrinking it, and then displaying it over the current screen."""
    glow_surf = pygame.transform.smoothscale(screen, (width // 4, height // 4))
    glow_surf = pygame.transform.smoothscale(glow_surf, (width, height))
    glow_surf.set_alpha(100)
    screen.blit(glow_surf, (0, 0))
    
def add_glitch_effect(glitch_surface):
    """Add visual glitches to the screen by randomly shifting some of the lines of the screen."""
    shift_amount = 40
    if random.random() < 0.1:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pygame.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))

# Debug options
def debugVisuals(FaceObj, spriteGroup, afterImageGroup):
    """Displays helpful visual info for debugging."""
    # 4:3 boundary
    pygame.draw.rect(screen, "blue", (80, 0 , 640, 480), 1)
    
    # Face boundary
    pygame.draw.rect(screen, "orange", (160, 80, 480, 320), 1)
    
    # Vector2s visualized
    # FaceObj.drawPositions(FaceObj)

    # Draw all sprites' rects for ease
    # for sp in spriteGroup:
    #     pygame.draw.rect(screen, (255, 0, 0), sp.rect, 1)
    #     pygame.draw.circle(screen, "purple", sp.rect.center, 10)
        
    # for sp in afterImageGroup:
    #     pygame.draw.rect(screen, (0,139,0), sp.rect, 1)
    
    # pygame.draw.circle(screen, (192, 255, 0), (screen.get_rect().centerx, 220), 10)
    # pygame.draw.circle(screen, (192, 255, 0), (screen.get_rect().centerx, 260), 10)
    
    # for sp in spriteGroup:
    #     if isinstance(sp, Eye):
    #         pygame.draw.circle(screen, "blue", sp.rect.center, 10)
                   
    """Print debugging info"""
    screen.blit(text1, (0, 0))
        
# =============================================================================
# Main()
# =============================================================================
def main():
    """Main program loop."""
    # Color of the background
    BGcolor = 32, 32, 32
    
    # Set delta t to 0, set up game clock
    deltaT, clock = 0, pygame.time.Clock()
            
    # Create sprite group
    sprites = pygame.sprite.LayeredUpdates()
    # Create sprite group for after images
    afterImages = pygame.sprite.LayeredUpdates()
    
    # Create face
    MainFace = Face(sprites)
    
    # Game loop, run this code every frame
    gameIsOn = True
    while gameIsOn:
        
        # Get delta T (time in ms between each frame)
        deltaT = clock.tick(60)

        # Listen for events first
        events = pygame.event.get()
        for e in events:
            # Check if application is closed, close game if so
            if e.type == pygame.QUIT:
                gameIsOn = False
                
            # TODO: Change this to not be debuggy
            # TODO: Key strokes will be changed to be reading from pins on the RaspPy
            if e.type == pygame.KEYDOWN:
                # If spacebar is pressed, randomly change the destination of the face
                if e.key == pygame.K_SPACE:
                    MainFace.setDestination(random.randint(160, 540), random.randint(80, 400))
                    MainFace.startMoving()
                    
                # TODO: This is just for fun, delete later
                
                global changeLeftEye
                global changeRightEye
                global changeMouth
                
                # Use i to change LeftEye sprite
                if e.key == pygame.K_i:
                    changeLeftEye = True
                # Use o to change RightEye sprite
                if e.key == pygame.K_o:
                    changeRightEye = True
                # Use p to change Mouth sprite
                if e.key == pygame.K_p:
                    changeMouth = True
        
        # Attract mode ideas
        if not MainFace.isMoving:
            # Random, slow movement
            MainFace.moveTo(random.randint(160, 540), random.randint(80, 400), random.uniform(1.0, 5.0))
            # Sinusoidal movement
            # if(MainFace.currPos.x <= 400):
            #     MainFace.moveTo(600, 300, 1.0)
            # else:
            #     MainFace.moveTo(200, 300, 1.0)
        
        # Update all sprites, including after images
        MainFace.update(deltaT, afterImages)
        afterImages.update(deltaT)
                                  
        # Draw bg, after images, sprites, and CRT effects to screen, in that order
        screen.fill(BGcolor)
        afterImages.draw(screen)
        MainFace.drawFace()
        apply_CRT_effects()
                
        # Debugging features
        debugVisuals(Face, sprites, afterImages)
                
        # Needed for display
        pygame.display.flip()
                
# =============================================================================
# Program execution
# =============================================================================

# Run main                
main()

# Quit if program finishes
pygame.quit()
sys.exit()