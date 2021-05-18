import pygame
import constants
import spritesheet

# ACTOR : any object in the environment with a hitbox

class Actor(pygame.sprite.Sprite):
  def __init__(self, loc, bounds, spritesheetPath, imageLocation) -> None:
    pygame.sprite.Sprite.__init__(self)
    self.ss = spritesheet.spritesheet(spritesheetPath)
    self.image = pygame.transform.scale(self.ss.image_at(imageLocation),  (constants.ACTOR_WIDTH, constants.ACTOR_HEIGHT))
    self.rect = self.image.get_rect()
    self.rect.center = loc
    self.bounds = bounds
  def draw(self, window):
    window.blit(self.image, (self.rect.x, self.rect.y))
    pygame.draw.rect(window, constants.RED, self.rect, 2)
  def update(self, window):
    self.draw(window)

# PLAYER : player in  the environment, controlled by user input

class Player(Actor):
  def __init__(self, loc, bounds, env) -> None:
    Actor.__init__(self, loc, bounds, constants.SPRITESHEET_PATH, constants.SAMMIE_DEFAULT)
    self.velocity = 5
    self.dx = 0
    self.dy = 0
     
    # list of all the sprites in our environment 
    self.env = env
  def handle_input(self, keys_pressed):
    if keys_pressed[pygame.K_a] and self.rect.x > 0:
      self.dx = -self.velocity
    if keys_pressed[pygame.K_d] and self.rect.x + constants.SAMMIE_WIDTH < constants.WIDTH:
      self.dx = self.velocity
    if keys_pressed[pygame.K_w] and self.rect.y > 0:
      self.dy = -self.velocity
    if keys_pressed[pygame.K_s] and self.rect.y + constants.SAMMIE_HEIGHT < constants.HEIGHT:
      self.dy = self.velocity
  
  def canMove(self):
    nextRec = pygame.Rect(self.rect)
    nextRec.x += self.dx
    nextRec.y += self.dy
    for actor in self.env:
      if nextRec.colliderect(actor.rect):
        return False
    return True
  def move(self):
    self.rect.x += self.dx
    self.rect.y += self.dy
    self.dx = 0
    self.dy = 0
  def update(self, window):
    if self.canMove():
      self.move()
    Actor.draw(self, window)
  
# DOODAD : any actor the player can interact with

class Doodad(Actor):
  def __init__(self, loc, bounds, spritesheetPath, imageLocation) -> None:
    Actor.__init__(self, loc, bounds, spritesheetPath, imageLocation)
    self.enabled = False
  def enable(self):
    self.enabled = True
  def disable(self):
    self.enabled = False
  def update(self, window):
    # if enabled, show the interact button
    if self.enabled:
      pygame.draw.rect(window, constants.RED, pygame.Rect(self.rect.x - 30, self.rect.y - 30, 32, 32))
    Actor.draw(self, window)
  def handle_input(self, keys_pressed):
    pass
  
