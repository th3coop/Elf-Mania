import pygame
import os
import numpy


class GameObject:

    def __init__(self, x, y, img_path):
        self.img_path = img_path
        self.width = 187 # dynamically obtain these two
        self.height = 466
        self.scale = 2
        self.breathing = True
        self.sprite = self.load_sprite()
        self.btm_buffer = (20 + self.height)
        self.right_buffer = (20 + self.width)
        self.pre_offset_pos = (x,y)
        self.x_pos = 100
        self.y_pos = 100 #max(y, self.btm_buffer)

    def load_sprite(self):
        # Create play sprite
        obj = pygame.image.load(self.img_path)
        return pygame.transform.scale(obj, (self.width*self.scale, self.height*self.scale))

    def draw(self, background):
        background.blit(self.sprite, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    SPEED = 10

    def __init__(self, x, y, img_path=None):
        self.sprite_width = 31
        self.sprite_height = 31
        self.top_padding = -9
        if img_path == None:
            img_path = os.path.join("animations","ELF ANIMATIONS.png")
        super().__init__(x, y, img_path)
        
        #These offsets shift the character image to position desired animation
        # step into the current position of the character.  Imagine you're shifting
        # a larger page with many small images on it to only show the desired image.
        self.breath_idx = 0
        self.breath_offset = [(0, self.top_padding),
            (-(self.sprite_width * 1), self.top_padding),
            (-(self.sprite_width * 2), self.top_padding),
            (-(self.sprite_width * 3), self.top_padding),
            ] # (x, -18)
        
        self.jump_idx = 0
        self.jump_offset = [(0, self.top_padding - (self.sprite_height)),
            (-(self.sprite_width * 1), self.top_padding - (self.sprite_height)),
            (-(self.sprite_width * 2), self.top_padding - (self.sprite_height)),
            (-(self.sprite_width * 3), self.top_padding - (self.sprite_height)),
            (0, self.top_padding - (self.sprite_height* 2)),
            (-(self.sprite_width * 1), self.top_padding - (self.sprite_height* 2)),
            (-(self.sprite_width * 2), self.top_padding - (self.sprite_height* 2)),
            (-(self.sprite_width * 3), self.top_padding - (self.sprite_height* 2)),
            ] # (x, -18)
        self.position_animation(self.breath_offset[self.breath_idx])

    # This function will handle any play state changes that need to occur before 
    #  the playert animation changes.
    def break_for_animation(self, ):
        self.breathing = False

    # This function should be called when a particular animation cycle has completed
    def reset_animation(self, ):
        self.breathing = True

    # this function will run indefinitely until pause by calling break_for_animation
    def breath(self, ):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        while self.breathing:
            self.breath_idx += 1
            if self.breath_idx == len(self.breath_offset):
                self.breath_idx = 0
            self.position_animation(self.breath_offset[self.breath_idx])

    def jump(self,):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        self.break_for_animation()
        for i in range(len(0, (self.jump_offset) - 1)):
            self.position_animation(self.jump_offset[i])
        self.reset_animation()

    # offset is a tuple to shift animation image.  Generally should coincide with proper
    # animation position
    def position_animation(self, offset):
        res = numpy.add(self.pre_offset_pos,  numpy.multiply(offset, self.scale))
        self.x_pos = res[0]
        self.y_pos = res[1]
        

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
        super().__init__(x, y, os.path.join("imgs","enemy.png"))

    def move(self, screen_width, multiplier=1):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        if self.x_pos >= (screen_width - self.right_buffer):
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

    # def detect_colision(self)
