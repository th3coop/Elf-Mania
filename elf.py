import os
import tkinter
from pathlib import Path

import pygame

import player

# Window Options
root = tkinter.Tk()
# not sure if these calls are high DPI friendly.
OS_SCREEN_WIDTH = root.winfo_screenwidth()
OS_SCREEN_HEIGHT = root.winfo_screenheight()
# not sure what i want to do here.  Full screen is maybe too big?
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400
SCREEN_TITLE = "ELF MANIA"

# Color vars, RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("courier", 30)


class Game:

    TICK_RATE: int = 60
    is_game_over: bool = False
    did_win: bool = False
    round: int

    def __init__(self, background_img_path: Path, title: str):
        pygame.init()
        self.background_img_path = background_img_path
        self.load_screen()
        self.load_background()
        self.theme_song = pygame.mixer.Sound(os.path.join(
            'sounds', 'Hypnotic NES.wav'))
        self.title = title
        # Screen game screen
        self.player = player.PlayerCharacter(
            # 839, 215)
            200, 200)  # easier for debugging
        # Set how often held keys repeat their events
        pygame.key.set_repeat(10, 10)  # start after 10ms and repeat after 10ms

        # Set the title of the screen
        pygame.display.set_caption(self.title)

    def load_screen(self, ):
        # This set_mode must happen before anything graphical happens
        self.game_screen = pygame.display.set_mode(  # easier for debugging
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.game_screen = pygame.display.set_mode(
        #     (0, 0), pygame.FULLSCREEN | pygame.RESIZABLE | pygame.NOFRAME)

    def load_background(self,):
        self.background_img = pygame.image.load(
            self.background_img_path).convert_alpha()
        self.background_rect = self.background_img.get_rect()

    def draw_background(self, ):
        self.game_screen.fill(WHITE)
        self.game_screen.blit(self.background_img, (0, 0))

    def show_msg(self, txt: str, duration: int = 1):
        text = font.render(txt, False, RED, BLACK)
        self.game_screen.blit(text, (300, 350))
        pygame.display.update()
        clock.tick(duration)

    def draw_screen(self):
        # print("drawing game")
        # Clear screen
        self.draw_background()
        # Draw their new pos
        self.player.draw(self.game_screen)
        pygame.display.flip()

    def run_game_loop(self):
        self.theme_song.play(loops=-1, fade_ms=100)
        while not self.is_game_over:
            if self.player.breathing:
                self.player.breath()
            if self.player.jumping:
                self.player.jump()
            if self.player.walking:
                self.player.walk()
            # Create the event loop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.is_game_over = True
                    if event.key == pygame.K_UP:
                        print("up")
                        # don't jump again if it's already jumping
                        if not self.player.jumping:
                            self.player.jump()
                    # What if it's up AND down?  powerjump? Don't limit yourself
                    # homie. Be crazy.  Elfs are crazy.  Be an elf.
                    elif event.key == pygame.K_DOWN:
                        print("down")
                    if event.key == pygame.K_LEFT:
                        print("left")
                        self.player.direction = -1
                        self.player.startMove()
                    elif event.key == pygame.K_RIGHT:
                        print("right")
                        self.player.direction = 1
                        self.player.startMove()

                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        pass
                    elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        print("stop left and right")
                        self.player.stopMove()
                if event.type == pygame.QUIT:
                    self.is_game_over = True
            self.draw_screen()
            # move the self.player
            # self.player.move(direction, self.height)

            # Update all game graphics
            pygame.display.update()
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


if __name__ == '__main__':
    new_game = Game(Path(os.path.join(
        "imgs", "backgrounds", "fantasy-2048-x-1536_full.png")), SCREEN_TITLE)
    new_game.run_game_loop()
    pygame.quit()
    quit()
