import pygame
import constants
from actor import Player, Doodad
from level import Level
from task import Task

def main():
  # main program

  # Setup game
  WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
  bounds = WIN.get_rect()
  pygame.display.set_caption("Sammie")
  # create player
  

  # create some doodads
  player = Player(bounds.center, bounds)
  # create levels & tasks
  task = Task(player)
  # set timer
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(constants.FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        task.click()

    keys_pressed = pygame.key.get_pressed()
    task.handleInput(keys_pressed)
    task.update()

    task.draw(WIN)
    # player.draw_ui(WIN)
    pygame.display.update()
  pygame.quit()


if __name__ == "__main__":
  main()
