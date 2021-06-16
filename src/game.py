import pygame
import constants
from actor import Player
# GAME : manage the game, control which state the game is in
class Game:
  def __init__(self) -> None:
    pygame.init()
    pygame.display.set_caption("Sammie")
    self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    self.bounds = self.screen.get_rect()
    self.clock = pygame.time.Clock()
    self.running = True
    self.state = None
  def new(self):
    self.playing = True
    self.state = StartScreen()
    self.player = Player(self, constants.WIDTH / 2, constants.HEIGHT / 2)
  def loadState(self, state):
    self.state = state
  def events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.playing = False
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: # left click
          for sprite in self.state.clickable_sprites:
            sprite.click()

  def update(self):
    self.state.all_sprites.update()
  def draw(self):
    self.screen.fill(constants.WHITE)
    self.state.all_sprites.draw(self.screen)
    pygame.display.update()
  def run(self):
    while self.playing:
      self.events()
      self.update()
      self.draw()
      self.clock.tick(constants.FPS)
    self.running = False
  