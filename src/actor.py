import pygame
import constants
import spritesheet
from random import randint
# ACTOR : any object in the environment with a hitbox

class Actor(pygame.sprite.Sprite):
  def __init__(self, loc, bounds, spritesheetPath, imageLocation, colorkey=None) -> None:
    pygame.sprite.Sprite.__init__(self)
    self.ss = spritesheet.spritesheet(spritesheetPath)
    self.image = self.ss.image_at(imageLocation, colorkey)
    self.rect = self.image.get_rect()
    self.rect.center = loc
    self.bounds = bounds
  def draw(self, window):
    window.blit(self.image, (self.rect.x, self.rect.y))
  def update(self):
    pass

# PLAYER : player in  the environment, controlled by user input

class Player(pygame.sprite.Sprite):
  def __init__(self, game, x, y) -> None:
    self.game = game
    self._layer = constants.PLAYER_LAYER
    self.groups = self.game.all_sprites
    pygame.sprite.Sprite.__init__(self, self.groups)
    self.width = constants.SAMMIE_WIDTH
    self.height = constants.SAMMIE_HEIGHT
    self.walking_ss = spritesheet.spritesheet(constants.WALK_SPRITESHEET)
    self.walking_left = self.walking_ss.load_strip(constants.SAMMIE_DEFAULT, 4)
    self.walking_right = [pygame.transform.flip(image, True, False) for image in self.walking_left]
    self.walking_animation = self.walking_left
    self.walk_timer = 0
    self.image = self.walking_animation[0]
    self.current_animation = 0
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.env = None
    self.velocity = 5
    self.gravity = 3
    self.dx = 0
    self.dy = self.gravity
  # level is a sprite group containing sprites in the environment
  def setLevel(self, level):
    self.env = level
  def handleInput(self, keys_pressed):
    if keys_pressed[pygame.K_a] and self.rect.x > 0:
      self.dx = -self.velocity
    if keys_pressed[pygame.K_d] and self.rect.x + constants.SAMMIE_WIDTH < constants.WIDTH:
      self.dx = self.velocity
    if keys_pressed[pygame.K_w] and self.rect.y > 0:
      self.dy = -self.velocity
    if keys_pressed[pygame.K_s] and self.rect.y + constants.SAMMIE_HEIGHT < constants.HEIGHT:
      self.dy = self.velocity
  def move(self):
    self.rect.x += self.dx
    if self.dx > 0:
      if self.walk_timer < 5:
        self.walk_timer += 1
      else:
        self.walking_animation = self.walking_right
        self.current_animation = self.current_animation + 1 if (self.current_animation + 1 < len(self.walking_animation)) else 0
        self.image = self.walking_animation[self.current_animation]
        self.walk_timer = 0
    elif self.dx < 0:
      # left animation
      if self.walk_timer < 5:
        self.walk_timer += 1
      else:
        self.walking_animation = self.walking_left
        self.current_animation = self.current_animation + 1 if (self.current_animation + 1 < len(self.walking_animation)) else 0
        self.image = self.walking_animation[self.current_animation]
        self.walk_timer = 0
    else: 
      self.image = self.walking_animation[0]
    self.rect.y += self.dy
    collisions = pygame.sprite.spritecollide(self, self.env, False)
    for collision in collisions:
      if self.dy > 0:
        self.rect.bottom = collision.rect.top
      elif self.dy < 0:
        self.rect.top = collision.rect.bottom
    self.dx = 0
    self.dy = self.gravity
  def update(self):
    self.move()
  def draw(self, window):
    window.blit(self.image, (self.rect.x, self.rect.y))

# DOODAD : any actor the player can interact with

class Doodad(Actor):
  def __init__(self, loc, bounds, spritesheetPath, imageLocation) -> None:
    Actor.__init__(self, loc, bounds, spritesheetPath, imageLocation)
    self.enabled = False
  def enable(self):
    self.enabled = True
  def disable(self):
    self.enabled = False
  def update(self):
    # if enabled, show the interact button
    if self.enabled:
      pygame.draw.rect(window, constants.RED, pygame.Rect(self.rect.x - 30, self.rect.y - 30, 32, 32))
  def handle_input(self, keys_pressed):
    pass

class Bubble(pygame.sprite.Sprite):
  def __init__(self, group, speedMultiplier=1):
    pygame.sprite.Sprite.__init__(self, group)
    self.width = 64
    self.height = 64
    self.image = pygame.image.load(constants.BUBBLE)
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.velocity = randint(1, 3) * speedMultiplier
    self.rect = self.image.get_rect()
    self.rect.x = randint(0, constants.WIDTH-self.width)
    self.rect.y = 30
    self.radius = 24
    self.status = True
  def update(self):
    self.rect.y += self.velocity
  def addStressOnClick(self):
    return True
  def addStressOnHitGround(self):
    return True
  def addStressOnHitPlayer(self):
    return False


class BadBubble(Bubble):
  def __init__(self, group, speedMultiplier=1):
    Bubble.__init__(self, group, speedMultiplier)
    self.ss = spritesheet.spritesheet(constants.BUBBLE)
    self.bubbles = self.ss.load_strip((0,0,64,64), 4)[1:3]
    self.image = pygame.transform.scale(self.bubbles[randint(0, len(self.bubbles)-1)], (self.width, self.height))
  def addStressOnClick(self):
    return False
  def addStressOnHitGround(self):
    return False
  def addStressOnHitPlayer(self):
    return True
class GoodBubble(Bubble):
  def __init__(self, group, speedMultiplier=1):
    Bubble.__init__(self, group, speedMultiplier)
    self.ss = spritesheet.spritesheet(constants.BUBBLE)
    self.bubbles = self.ss.load_strip((0,0,64,64), 4)[::3]
    self.image = pygame.transform.scale(self.bubbles[randint(0, len(self.bubbles)-1)], (self.width, self.height))
  def addStressOnClick(self):
    return True
  def addStressOnHitGround(self):
    return True
  def addStressOnHitPlayer(self):
    return False

