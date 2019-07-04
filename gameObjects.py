import pygame
import os
import time
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

        self.initialize_movement_props()

        self.scale_value = 2
        # deal with these later when we start moving things...i think use Rects will eliminate the need for a buffer though
        # self.btm_buffer = (20 + self.height)
        # self.right_buffer = (20 + self.width)

        self.pre_offset_pos = (x, y)
        self.acceleration = 3
        self.location = [x,y]
        self.x_pos = self.location[0]
        self.y_pos = self.location[1]# max(y, self.btm_buffer)
        # [x_speed, y_speed]

    def initialize_movement_props(self,):
        self.left_move_start_time = 0
        self.left_move_stop_time = 0 
        self.left_moving_time = 0 

        self.right_move_start_time = 0
        self.right_move_stop_time = 0 
        self.right_moving_time = 0 

    def load_sprite(self, ):
        # Create sprite
        self.sprite = pygame.image.load(self.img_path)
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

    def __init__(self, x, y, img_path=None):
        if img_path == None:
            img_path = os.path.join("animations", "ELF ANIMATIONS.png")
        super().__init__(x, y, img_path,)
        self.max_speed = 100
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

    def _calc_direction_velocity(self, direction):
        velocity = 0.0
        # is accelerating
        if not getattr(self, "%s_move_start_time"%(direction)) is 0:
            t = time.time() - getattr(self, "%s_move_start_time"%(direction))
            veloctiy = (t * self.acceleration) + getattr(self, "%s_velocity"%(direction))
        # is stopping
        if not getattr(self, "%s_move_stop_time"%(direction)) is 0 and getattr(self, "%s_velocity"%(direction)) > 0:
            t = time.time() - getattr(self, "%s_move_stop_time"%(direction))
            veloctiy = (t * -(self.acceleration)) + getattr(self, "%s_velocity"%(direction))
        return min(max(0, velocity), self.max_speed)

    # Don't care which direction as we can only be accelerating
    # in one direction so which ever one has a moving start time
    # that's the time we want
    def get_moving_direction_time(self):
        return max(time.time() - self.left_move_start_time, time.time() - self.right_move_start_time,)

    def calculate_location(self):
        left_vel = self._calc_direction_velocity("left")
        right_vel = self._calc_direction_velocity("right")
        total_velocity = right_vel - left_vel
        return [total_velocity * self.get_moving_direction_time(), self.y_pos]

    def _start_move(self, direction):
        self.stop_direction("right")  if direction is "right" else self.stop_direction("left") 
        setattr(self, "%s_move_start_time"%(direction), time.time())
        
    def stop_direction(self, direction):
        setattr(self, "%s_move_start_time" %(direction), 0)
        setattr(self, "%s_move_stop_time" %(direction), time.time())
        
    def walk(self, direction):
        self.stop_direction(direction)
        self.location = self.calculate_location()
        # if not self.walking:
        #     self.walking = True
        #     self.break_for_animation()
        # self.walk_sound.play()
        # self.sprite = self.walk_iter.next()

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
