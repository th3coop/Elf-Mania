# Pygame development 1
# Start the basic game set uo
# Set up the display

import pygame
import gameObjects
import random
import os

# Window Options
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 50
SCREEN_TITLE = "CROSSY RPG"

# Color vars, RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)


class Game:

    TICK_RATE = 60
    is_game_over = False
    did_win = False

    def __init__(self, background_img_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.pygame = pygame
        self.player = gameObjects.PlayerCharacter(
            0, 0, clock, self)
        # Screen game screen
        self.game_screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set the title of the screen
        pygame.display.set_caption(self.title)

    def show_msg(self, txt, duration=1):
        text = font.render(txt, False, RED, BLACK)
        self.game_screen.blit(text, (300, 350))
        pygame.display.update()
        clock.tick(duration)

    def generate_enemies(self, round):
        i = 0
        self.enemies = []
        while i < round:
            enemy = gameObjects.EnemyCharacter(random.randint(0, self.width),
                                               random.randint(0, self.height))
            enemy.SPEED *= (self.round/2)
            self.enemies.append(enemy)
            i += 1

    def draw_screen(self):
        # print("drawing game")
        # Clear screen
        self.game_screen.fill(WHITE)
        # Draw their new pos
        self.player.draw(self.game_screen)

    def run_game_loop(self):
        direction = 0
        
        while not self.is_game_over:
            self.player.breath()  
            # Create the event loop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        print("up")
                        self.player.jump()
                    elif event.key == pygame.K_DOWN:
                        print("down")
                    elif event.key ==  pygame.K_LEFT or event.key ==  pygame.K_RIGHT:
                        print("left and right")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                elif event.type == pygame.QUIT:
                    self.is_game_over = True
            self.draw_screen()
            # move the self.player
            # self.player.move(direction, self.height)

            # Update all game graphics
            self.pygame.display.update()
            clock.tick(self.TICK_RATE)

        if self.did_win:
            self.draw_screen()
            pygame.display.update()
            self.show_msg("Round {} Bitches!!!".format(self.round))
            self.did_win = False
            self.is_game_over = False
            self.run_game_loop()
        else:
            return


pygame.init()

new_game = Game(os.path.join("imgs","background.png"), SCREEN_TITLE,
                SCREEN_HEIGHT, SCREEN_WIDTH)
new_game.run_game_loop()


pygame.quit()
quit()
