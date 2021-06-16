from random import randint
import pygame
import constants
from spritesheet import spritesheet, load_image
from actor import Player, GoodBubble, BadBubble, Actor
from game import Game
# STATE : Manages sprites and actions the player can do
# Ex: Tilemap, Sidescroller
class State:
  def __init__(self, game, player):
    self.game = game
    self.all_sprites = pygame.sprite.LayeredUpdates()
    self.ui = pygame.sprite.LayeredUpdates()
    
    self.player = player
    self.all_sprites.add(self.player) 
    
  def handleInput(self, keys):
    for sprite in self.all_sprites:
      sprite.handleInput(keys) 
  def update(self):
    self.all_sprites.update()
  def draw(self):
    self.all_sprites.draw(self.game.screen)

class Background(pygame.sprite.Sprite):
  def __init__(self, imagePath, group):
    pygame.sprite.Sprite.__init__(self, group)
    self.width = constants.WIDTH
    self.height = constants.HEIGHT
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(constants.BLUE)

class StartScreen(State):
  def __init__(self, game, player):
    State.__init__(self, game, player)
    self.background = Background(constants.BACKGROUND, self.all_sprites)
    
class Button(pygame.sprite.Sprite):
  def __init__(self, group, center, imagePath, rect):
    pygame.sprite.Sprite.__init__(self, group)
    self.image = load_image(imagePath)
    self.rect = self.image.get_rect(center=center)
  
  def onClick(self):
    pass
  def update(self):
    pass

class Task(State):
  def __init__(self, game: Game, player: Player):
    State.__init__(game, player)
    self.image = pygame.Surface([constants.WIDTH, constants.HEIGHT])
    self.background = pygame.Surface([constants.WIDTH, constants.HEIGHT])
    self.floor = pygame.Surface([constants.WIDTH, constants.GRID_HEIGHT])
    self.bubbleSpeedMultiplier = 1
    self.bubbles = pygame.sprite.Group()
    self.env = pygame.sprite.Group()
    self.ui = pygame.sprite.Group()
    self.player = player
    self.run = True
    self.input = None
     
    self.background.fill(constants.BLUE)

    self.clouds = pygame.image.load(constants.CLOUDS)
    rects = [(420,420), (69, 69), (constants.WIDTH-420, 169)]
    for rect in rects:
      self.background.blit(self.clouds, rect)
    # draw floor
    for x in range(int(constants.WIDTH / constants.GRID_WIDTH)+1):
      self.env.add(Actor((constants.GRID_WIDTH * x, constants.HEIGHT - 168), self.player.bounds, constants.GROUND, (0, 0, 32, 32)))
      for y in range(int((constants.HEIGHT - 168) / constants.GRID_HEIGHT) + 1, int(constants.HEIGHT / constants.GRID_HEIGHT) + 1):
        self.env.add(Actor((constants.GRID_WIDTH * x, constants.GRID_HEIGHT * y), self.player.bounds, constants.BENEATH, (0,0,32,32)))

    self.player.setLevel(self.env)
    self.env.draw(self.background)
    self.clickActive = False
    # timer
    self.timer = Timer(self.ui)
    self.stressBar = StressBar(self.ui)
    self.breatheTimer = BreatheTimer(self.stressBar, self.ui)
    #end task
    self.endText = Actor((0, 0), (0,0), constants.END_TEXT, (0,0,64,64), -1)
    self.endText.rect = self.endText.image.get_rect()
    self.endText.rect.center = (constants.WIDTH / 2, 300)
  
  def click(self):
    self.clickActive = True
  def handleInput(self, keys_pressed):
    if self.run:
      self.player.handleInput(keys_pressed)
      self.breatheTimer.handleInput(keys_pressed)

  def update(self):
    if self.run:
      if len(self.bubbles) < 5:
        rand = randint(0,1)
        if rand:
          self.bubbles.add(GoodBubble(self.bubbles, self.bubbleSpeedMultiplier))
        else:
          self.bubbles.add(BadBubble(self.bubbles, self.bubbleSpeedMultiplier))
      playerBubbleCollisions = pygame.sprite.spritecollide(self.player, self.bubbles, True, pygame.sprite.collide_circle)
      for bubble in playerBubbleCollisions:
        if bubble.addStressOnHitPlayer():
          self.stressBar.addStress()
        else:
          self.stressBar.removeStress()
      fallenBubbles = pygame.sprite.groupcollide(self.bubbles, self.env, True, False, collided=pygame.sprite.collide_circle)
      for bubble in fallenBubbles:
        if bubble.addStressOnHitGround():
          self.stressBar.addStress()
          
      if self.clickActive and pygame.mouse.get_pressed()[0]:
        clickPos = pygame.mouse.get_pos()
        for bubble in self.bubbles:
          if bubble.rect.collidepoint(clickPos):
            if bubble.addStressOnClick():
              self.stressBar.addStress()
            bubble.remove(self.bubbles)
      self.bubbles.update()
      self.ui.update()
      self.bubbleSpeedMultiplier = max(1, round(self.stressBar.currentStress / self.stressBar.maxStress * 3))
      self.image.blit(self.background, self.background.get_rect())
      self.bubbles.draw(self.image)
      self.ui.draw(self.image)
      if (self.timer.time_left <= 0 or self.stressBar.currentStress >= self.stressBar.maxStress):
        self.run = False
      self.player.update()
      self.clickActive = False
    else:
      # quit
      # display task end
      self.bubbles.empty()
      self.player.update()
      self.image.blit(self.background, self.background.get_rect())
      self.endText.draw(self.image)
      self.ui.draw(self.image)
  def draw(self, window):
    window.blit(self.image, self.image.get_rect())
    self.player.draw(window)

class Timer(pygame.sprite.Sprite):
  def __init__(self, group):
    pygame.sprite.Sprite.__init__(self, group)
    self.ss = spritesheet.spritesheet(constants.TIMER)
    self.times = self.ss.load_strip((0,0,64,64), 31)[::-1]
    self.time_left = len(self.times)-1
    self.image = self.times[self.time_left]
    self.updateTimer = 0
    self.rect = self.image.get_rect()
    self.rect.center = (constants.WIDTH / 2, 50)
  def update(self):
    if self.updateTimer < 60:
      self.updateTimer += 1
    else:
      self.time_left -= 1
      self.image = self.times[self.time_left]
      self.updateTimer = 0
      

class StressBar(pygame.sprite.Sprite):
  def __init__(self, group):
    pygame.sprite.Sprite.__init__(self, group)
    self.ss = spritesheet.spritesheet(constants.STRESS_BAR)
    self.stressBarIcons = self.ss.load_strip((0,0,64,64), 63)
    self.stressBarIcons = [pygame.transform.scale(image, (192, 128)) for image in self.stressBarIcons]
    self.currentStress = 0
    self.maxStress = len(self.stressBarIcons) - 1
    self.image = self.stressBarIcons[0]
    self.rect = self.image.get_rect()
    self.rect.center = 150, constants.HEIGHT - 84
  def addStress(self):
    # only add if there if it wont go above max
    self.currentStress = min(self.maxStress, self.currentStress + 2)
  def removeStress(self):
    self.currentStress = max(0, self.currentStress - 1)
  def update(self):
    self.image = self.stressBarIcons[self.currentStress]
class BreatheTimer(pygame.sprite.Sprite):
  def __init__(self, stressTarget, group):
    pygame.sprite.Sprite.__init__(self, group)
    self.stress_bar = stressTarget
    self.breathe_ss = spritesheet.spritesheet(constants.BREATHE_SPRITESHEET)
    self.miss_ss = spritesheet.spritesheet(constants.MISS_SPRITESHEET)
    self.breathe_frame = 0
    self.breathe_range = (26, 36)
    self.breathe_icons = self.breathe_ss.load_strip((0, 0, 64, 64), 31)
    self.breathe_icons = self.breathe_icons + self.breathe_icons[::-1] # reverse to get the whole animation
    self.miss_icons = self.miss_ss.load_strip((0,0,64,64), 31, colorkey=-1)
    self.miss_icons = self.miss_icons + self.miss_icons[::-1]
    self.miss_timer = 0
    self.current_icons = self.breathe_icons
    self.image = self.current_icons[0]
    self.rect = self.image.get_rect()
    self.rect.center = (constants.WIDTH - 100, constants.HEIGHT - 84)
    self.breathe_timer = 0
    self.didBreathe = 0
  def canBreathe(self):
    return self.breathe_frame in range(self.breathe_range[0], self.breathe_range[1])
  def handleInput(self, keys_pressed):
    if keys_pressed[pygame.K_SPACE]:
      self.breathe()
  def breathe(self):
    if self.canBreathe():
      # correct
      # play sound
      self.didBreathe = 1
    else:
      # incorrect
      # change image
      if self.miss_timer <= 0:
        self.miss_timer = 30
        self.current_icons = self.miss_icons
        self.stress_bar.addStress()
  def update(self):
    if not self.didBreathe and self.breathe_frame > self.breathe_range[1]:
      # missed breathing range
      self.miss_timer = 30
      self.current_icons = self.miss_icons
      self.stress_bar.addStress()
      self.didBreathe = 1
    if self.miss_timer == 0:
      self.current_icons = self.breathe_icons
      if self.breathe_frame + 1 in range(len(self.current_icons)):
        if self.breathe_timer < 3:
          self.breathe_timer += 1
        else:
          self.breathe_timer = 0
          self.breathe_frame += 1
      else:
        self.breathe_frame = 0
        self.didBreathe = 0
    else:
      self.miss_timer -= 1
    self.image = self.current_icons[self.breathe_frame]
