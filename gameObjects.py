import pygame
import os
import numpy
from spritesheet import Spritesheet


class GameObject:

    def __init__(self, x, y, img_path, use_sprite_sheet=True):
        self.img_path = img_path

        if use_sprite_sheet:
            self.sheet = Spritesheet(self.img_path)
            self.sprite = None
        else:
            self.sprite = self.load_sprite()
            self.sheet = None

        self.scale_value = 2
        # deal with these later when we start moving things...i think use Rects will eliminate the need for a buffer though
        # self.btm_buffer = (20 + self.height)
        # self.right_buffer = (20 + self.width)

        self.pre_offset_pos = (x, y)
        self.x_pos = 100
        self.y_pos = 100  # max(y, self.btm_buffer)

    def load_sprite(self, ):
        # Create sprite
        self.sprite = pygame.image.load(self.img_path).convert()
        self.scale_img()

    def scale_image(self, image):
        rect = image.get_rect()
        return pygame.transform.scale(
            image, (rect.width * self.scale_value, rect.height * self.scale_value))

    def scale_images(self, images):
        return [self.scale_image(img) for img in images]

    def draw(self, background):
        background.blit(self.sprite, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    SPEED = 10

    def __init__(self, x, y, img_path=None):
        if img_path == None:
            img_path = os.path.join("animations", "ELF ANIMATIONS.png")
        super().__init__(x, y, img_path,)

        # These are specific to ELF ANIMATION.PNG
        self.sprite_width = 31
        self.sprite_height = 31
        self.top_padding = 4.5
        # top_padding apparent gap at top of file that is uneven with gaps between rows of images
        # I could be setting sprite_[width/height] wrong but those should be even you'd think

        self.load_breathing_animation()
        self.load_jump_animation()

    def load_breathing_animation(self, ):
        self.breath_idx = 0
        self.breath_offsets = [(0, self.top_padding),
                               ((self.sprite_width * 1), self.top_padding),
                               ((self.sprite_width * 2), self.top_padding),
                               ((self.sprite_width * 3), self.top_padding),
                               ]  # (x, -18)
        # convert the offset list to include the width and height to represent a pygame.Rect
        rects = [(pos[0], pos[1], self.sprite_width, self.sprite_height)
                 for pos in self.breath_offsets]
        self.breath_images = self.scale_images(
            self.sheet.get_sprites(rects, pygame.Color("white")))

        self.sprite = self.breath_images[self.breath_idx]
        # Place the sprite in it's starting position
        self.pos = self.sprite.get_rect().move(0, 100)
        self.breathing = True

    def load_jump_animation(self, ):
        self.jump_idx = 0
        self.jump_offsets = [(0, self.top_padding - (self.sprite_height)),
                             ((self.sprite_width * 1),
                              self.top_padding - (self.sprite_height)),
                             ((self.sprite_width * 2),
                              self.top_padding - (self.sprite_height)),
                             ((self.sprite_width * 3),
                              self.top_padding - (self.sprite_height)),
                             (0, self.top_padding - (self.sprite_height * 2)),
                             ((self.sprite_width * 1), self.top_padding -
                              (self.sprite_height * 2)),
                             ((self.sprite_width * 2), self.top_padding -
                              (self.sprite_height * 2)),
                             ((self.sprite_width * 3), self.top_padding -
                              (self.sprite_height * 2)),
                             ]  # (x, -18)
        self.jumping = False
        rects = [(pos[0], pos[1], self.sprite_width, self.sprite_height)
                 for pos in self.jump_offsets]
        self.jump_images = self.scale_images(
            self.sheet.get_sprites(rects, pygame.Color("white")))

    # This function will handle any play state changes that need to occur before
    #  the playert animation changes.
    def break_for_animation(self, ):
        self.breathing = False

    # This function should be called when a particular animation cycle has completed
    def reset_breathing_animation(self, ):
        self.breathing = True
        self.sprite = self.breath_images[0]

    def move(self, direction, speed):
        pass

    def breath(self, ):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        self.breath_idx += 1
        if self.breath_idx == len(self.breath_images):
            self.breath_idx = 0
        self.sprite = self.breath_images[self.breath_idx]
        pygame.time.delay(100)

    def jump(self,):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        self.break_for_animation()
        self.jumping = True
        if self.jump_idx == len(self.jump_images):
            self.jumping = False
            self.jump_idx = 0
            self.reset_breathing_animation()
        self.sprite = self.jump_images[self.jump_idx]
        self.jump_idx += 1
        pygame.time.delay(100)

        # print("self.y_pos: %s" %self.y_pos)
        # print("self.jump_idx: %s" %self.jump_idx)

    def move(self, direction, max_height):
        # Y increase as you go down so to move UP on the
        # screen you must decrement Y
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        if self.y_pos >= max_height - self.btm_buffer:
            self.y_pos = max_height - self.btm_buffer

    def collision_detected(self, other_body):
        if (self.y_pos + self.height) < other_body.y_pos:
            return False
        elif self.y_pos > (other_body.y_pos + other_body.height):
            return False
        if self.x_pos > (other_body.x_pos + other_body.width):
            return False
        elif (self.x_pos + self.width) < other_body.x_pos:
            return False
        return True


class EnemyCharacter(GameObject):
    SPEED = 5

    def __init__(self, x, y):
        # How many spaces to move per move
        super().__init__(x, y, os.path.join("imgs", "enemy.png"))

    def move(self, screen_width, multiplier=1):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        if self.x_pos >= (screen_width - self.right_buffer):
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

    # def detect_colision(self)
