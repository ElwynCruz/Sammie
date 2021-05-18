import pygame
import constants
from actor import Player, Doodad

class Level:
  def __init__(self, player: Player, doodads) -> None:
    self.player = player
    self.doodads = doodads
  def getClosestDoodad(self):
    pos = pygame.math.Vector2(self.player.rect.x, self.player.rect.y)
    doodad = min(self.doodads, key=lambda a: pos.distance_to((a.rect.x, a.rect.y)))
    return doodad
  def enableActor(self, doodad):
    pos = pygame.math.Vector2(self.player.rect.x, self.player.rect.y)
    if pos.distance_to(doodad.rect.center) < 64:
      doodad.enable()
  def update(self, window):
    # Draw background
    window.fill(constants.WHITE)
    # then draw the environment (walls, floor tiles, etc)

    # enable closest doodad if applicable
    self.enableActor(self.getClosestDoodad())
    # lastly draw the doodads
    for doodad in self.doodads:
      doodad.update(window)