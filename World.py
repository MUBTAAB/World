import pygame
import os
import numpy as np
import gc
import math
import os
import random
import RndShp
import sys

from pygame.locals import *

if int(sys.argv[1]) != 0:
    # TODO: Make RndShp.py callable, because for some reason the first run is always laggy
    if not os.path.exists('Sprites'):
        os.makedirs('Sprites')

    for i in range(int(sys.argv[1])):
        RndShp.shape_p1('Sprites/p_{}.png'.format(i))

# Universal mathematical functions
def GetDegree(deg):
  deg = math.radians(deg%90)
  return(np.array([math.sin(deg), math.cos(deg)]))
  

def AngleTwoPoints(p1, p2):
  xDiff = p2.x - p1.x
  yDiff = p2.y - p1.y
  dto = math.degrees(math.atan2(yDiff, xDiff))
  dto = dto if dto > 0 else dto+360
  
  return(dto)
  
  
def ReAngle(angle):
  if angle < 0:
      angle = 360-abs(angle)
      
  elif angle > 360:
    angle = angle-360
  
  return(angle)

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

class SceneBase:
    def __init__(self, x, y ,contents):
        self.next = self

        self.contents = contents
        self.x = x
        self.y = y

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene, contents = {}):
    pygame.init()
    
    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode((width, height), flags)
    screen.set_alpha(None) 



    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
	
        # Event filtering 
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)


class WorldObject:
    def __init__(self, x, y, cathegory = None):
        self.x = x
        self.y = y
        self.cathegory = cathegory

    def CheckCollision(self, other):
        if i.x == self.x and i.y == self.y:
            return(True)
        else:
            return(False)
	
    def CheckColliding(self, world):
        colliding = []
        for i in world.contents:
            if CheckCollision(other = i):
                colliding.append(other)

        return(colliding)

    def CheckoutSideWorld(self, World): 
        if (self.x < 0 or self.x > World.y or  
            self.y < 0 or self.y > World.x):
            
            return(True)

        else:
            return(False) 
   
    def Draw(self):
        pass

	
    def Step(self, world):
        pass

class Creature(WorldObject):
    def __init__(self, x, y, sprite, cathegory = None, energy = 100):
        WorldObject.__init__(self, x, y, cathegory)
        self.sprite = get_image(sprite)
        self.energy = energy
   
    def Draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def Step(self, world):

        if self.CheckoutSideWorld(world):
            world.Destroy(self)   

        self.energy -= 1
        if self.energy <= 0:
            world.Destroy(self) 

class Alphoid_1(Creature):
   def __init__(self, x, y, sprite, cathegory = None, energy = 1000):
       Creature.__init__(self, x, y, sprite, cathegory, energy)
       self.timer1 = np.random.randint(10,200)
       self.xway = np.random.randint(-2,3)
       self.yway = np.random.randint(-2,3)

   def Step(self, world):
       super(Alphoid_1, self).Step(world)

       if self.timer1 >= 0:
           self.timer1 -= 1
       else:
           self.timer1 = 100
           self.xway = np.random.randint(-2,3)
           self.yway = np.random.randint(-2,3)
       
       self.x += self.xway
       self.y += self.yway 

class Directional_Alphoid(Creature):
    def __init__(self, x, y, sprite, cathegory = None, energy = 1000, direction = None, speed = 1, turnspeed = 1, target = None):
        Creature.__init__(self, x, y, sprite, cathegory, energy)
        self.timer1 = np.random.randint(10,200)
        self.speed = speed
        self.direction = np.randon.randint(0,360) if direction == None else direction
        self.target = WorldObject(np.random.randint(0,100), np.random.randint(0,100))

# TODO: Simplify this block! 
    def TurnTowards(self, p2):
        dto = AngleTwoPoints(self,p2)
    
        if self.direction == dto:
            return(True)
    
        if self.direction > dto:
            if (360-self.direction)+dto < self.direction-dto:
                self.direction = ReAngle(self.direction+self.TurningSpeed)
            else: 
                self.direction = ReAngle(self.direction-self.TurningSpeed)
          
        else: # if self.direction < dto
            if (360-dto)+self.direction < dto-self.direction:
                self.direction = ReAngle(self.direction-self.TurningSpeed)
            else: 
                self.direction = ReAngle(self.direction+self.TurningSpeed) 

    def Step(self, world):
        super(Directional_Alphoid, self).Step(world)
        
        self.TurnTowards(self.target)

# The rest is code where you implement your game using the Scenes model 
class TitleScene(SceneBase):
    def __init__(self, x, y, contents = {}):
        SceneBase.__init__(self, x, y, contents)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter 
                self.SwitchToScene(GameScene(x = self.x, y = self.y, contents = self.contents))
    
    def Update(self):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen 
        screen.fill((255, 0, 0))


class GameScene(SceneBase):
    def __init__(self, x, y, contents = {}):
        SceneBase.__init__(self, x, y, contents)
        
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        if self.contents == {}:
            return

        for key, value in self.contents.items():
            for i in value:
                i.Step(world = self)
    
    def Render(self, screen):
        # The game scene is just a blank blue screen 
        screen.fill((0, 0, 0))

        if self.contents == {}:
            return

        for key, value in self.contents.items():
            for i in value:
                i.Draw(screen = screen)        
	
    def Destroy(self, WorldObject):
        self.contents[WorldObject.cathegory].remove(WorldObject)
        gc.collect()

d_contents = {'creatures': [Alphoid_1(np.random.randint(0,840)
                           , np.random.randint(0,680)
                           , sprite = random.choice(['Sprites/{}'.format(i) for i in os.listdir('Sprites') if '.png' in i])
                           , cathegory = 'creatures') for i in range(100)]}

run_game(840, 680, 120, TitleScene(840, 680, d_contents))
#GameScene(contents = d_contents).Update()


