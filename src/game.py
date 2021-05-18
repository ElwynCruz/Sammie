import pygame
import constants
class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.bounds = self.screen.get_rect()
        pygame.display.set_caption("Sammie")
        self.clock = pygame.time.Clock()
        self.run = True
        self.level = None
    def load_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.doodads = pygame.sprite.Group()
        self.player = Player(self.bounds.center, self.bounds, self.doodads)
    def draw_window(self):
        self.screen.fill(constants.WHITE)
        for object in self.objects:
          self.screen.blit()