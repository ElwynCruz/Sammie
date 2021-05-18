import pygame
import constants
from actor import Player, Doodad
from level import Level

def main():
  # main program

  # Setup game
  WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
  bounds = WIN.get_rect()
  pygame.display.set_caption("Sammie")

  # create player
  

  # create some doodads

  doodad_1 = Doodad((200, 200), bounds, constants.UI_PATH, constants.FILLER_DOODAD)
  doodad_2 = Doodad((400, 400), bounds, constants.UI_PATH, constants.FILLER_DOODAD)
  player = Player(bounds.center, bounds, [doodad_1, doodad_2])
  # create levels & tasks
  level_01 = Level(player, [doodad_1, doodad_2])

  # set timer
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(constants.FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
    keys_pressed = pygame.key.get_pressed()
    player.handle_input(keys_pressed)
    level_01.update(WIN)
    player.update(WIN)
    pygame.display.update()
  pygame.quit()


if __name__ == "__main__":
  main()
