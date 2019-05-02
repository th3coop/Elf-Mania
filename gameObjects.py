import pygame
import os
from animation import Iter, StopIteration
from spritesheet import Spritesheet


class GameObject:

    def __init__(self, x, y, img_path, use_sprite_sheet=True):
        self.img_path = img_path

        if use_sprite_sheet:
            self.sheet = Spritesheet(self.img_path)
        else:
            self.load_sprite()
            self.sheet = None

        self.scale_value = 2
        # deal with these later when we start moving things...i think use Rects will eliminate the need for a buffer though
        # self.btm_buffer = (20 + self.height)
        # self.right_buffer = (20 + self.width)

        self.pre_offset_pos = (x, y)
        self.x_pos = x
        self.y_pos = y  # max(y, self.btm_buffer)

    def load_sprite(self, ):
        # Create sprite
        self.sprite = pygame.image.load(self.img_path).convert_alpha()
        self.scale_image(self.sprite)

    def scale_image(self, image):
        rect = image.get_rect()
        return pygame.transform.scale(
            image, (rect.width * self.scale_value, rect.height * self.scale_value))

    def scale_images(self, images):
        return [self.scale_image(img) for img in images]

    def draw(self, screen):
        screen.blit(self.sprite, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    SPEED = 10

    def __init__(self, x, y, img_path=None):
        if img_path == None:
            img_path = os.path.join("animations", "ELF ANIMATIONS.png")
        super().__init__(x, y, img_path,)

        # These are specific to ELF ANIMATION.PNG
        self.sprite_width = 31
        self.sprite_height = 31
        # top_padding apparent gap at top of file that is uneven with gaps between rows of images
        # I could be setting sprite_[width/height] wrong but those should be even you'd think
        self.top_padding = 4.5
        # rect is the pygame.Rect dimension of individual sprites in your spritesheet
        #  defaults to top left corner of sheet
        self.rect = (0, 0, self.sprite_width, self.sprite_height)

        self.load_breathing_animation()
        self.load_jump_animation()
        self.load_walk_animation()

    def load_breathing_animation(self, ):
        self.breath_images = self.scale_images(
            self.sheet.load_strip(self.rect, 0, 1, 4))
        self.breath_iter = Iter(self.breath_images, True)

        self.sprite = self.breath_iter.next()
        self.breathing = True

    def load_jump_animation(self, ):
        self.jump_sound = pygame.mixer.Sound(os.path.join(
            'sounds', 'Retro_8-Bit_Game-Jump_Lift_TakeOff_06.wav'))
        self.jump_idx = 0
        self.jumping = False
        self.jump_images = self.scale_images(
            self.sheet.load_strip(self.rect, 1, 2, 4))
        self.jump_iter = Iter(self.jump_images)

    def load_walk_animation(self, ):
        self.walk_sound = pygame.mixer.Sound(os.path.join(
            'sounds', 'one-foot-step.wav'))
        self.walking = False
        self.walk_images = self.scale_images(
            self.sheet.load_strip(self.rect, 3, 1, 4))
        self.walk_iter = Iter(self.walk_images, True)

    # This function will handle any play state changes that need to occur before
    #  the playert animation changes.
    def break_for_animation(self, ):
        self.breathing = False

    # This function should be called when a particular animation cycle has completed
    def reset_breathing_animation(self, ):
        self.breathing = True
        self.sprite = self.breath_iter.next()

    def breath(self, ):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        self.sprite = self.breath_iter.next()

    def walk(self, ):
        if not self.walking:
            self.walking = True
            self.break_for_animation()
        self.walk_sound.play()
        self.sprite = self.walk_iter.next()

    def stop_walk(self, ):
        self.walking = False
        self.reset_breathing_animation()

    def jump(self,):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        if not self.jumping:
            self.jump_sound.play()
            self.break_for_animation()
        self.jumping = True
        try:
            self.sprite = self.jump_iter.next()
        except StopIteration:
            self.jumping = False
            self.reset_breathing_animation()

        # print("self.y_pos: %s" %self.y_pos)
        # print("self.jump_idx: %s" %self.jump_idx)

    def move(self, direction, max_height):
        # Y increase as you go down so to move UP on the
        # screen you must decrement Y
        pass

    def collision_detected(self, other_body):
        pass
        # if (self.y_pos + self.height) < other_body.y_pos:
        #     return False
        # elif self.y_pos > (other_body.y_pos + other_body.height):
        #     return False
        # if self.x_pos > (other_body.x_pos + other_body.width):
        #     return False
        # elif (self.x_pos + self.width) < other_body.x_pos:
        #     return False
        # return True
