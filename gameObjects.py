import pygame
import os
import time
from animation import Iter, StopIteration
from spritesheet import Spritesheet


class GameObject:

    def __init__(self, x, y, screen, img_path="", is_sprite_sheet=True, sprite=None):
        """
        img_path = a path to an img...surprise!
        is_sprite_sheet = means the image path is a sprite sheet.  Intialization doesn't really do anything...
        sprite = pygame.Surface.  This is to set a sprite that you've already loaded.  
          Ie. load a single image from a sprite sheet
        """
        if img_path is not "" and sprite is not None:
            raise Exception(
                "You can't supply 'img_path' and 'sprite'.  Pick one")
        self.screen = screen
        self.sprite = sprite
        self.img_path = img_path
        self.sheet = None
        self.scale_value = 2
        if self.img_path is not "":
            if is_sprite_sheet:
                self.sheet = Spritesheet(self.img_path)

        if self.img_path or self.sprite:
            self.load_sprite()

        self.initialize_movement_props()

        # deal with these later when we start moving things...i think use Rects will eliminate the need for a buffer though
        # self.btm_buffer = (20 + self.height)
        # self.right_buffer = (20 + self.width)

        self.pre_offset_pos = (x, y)
        self.acceleration = 1000
        self.deceleration = 1000
        self.location = [x, y]
        self._set_xy(self.location)
        # max(y, self.btm_buffer)
        # [x_speed, y_speed]

    def _set_xy(self, location):
        self.x_pos = location[0]
        self.y_pos = location[1]

    def initialize_movement_props(self,):
        self.move_start_time = 0
        self.move_stopped_time = 0
        self.velocity = 0
        self.last_move_time = 0
        self.accelerating = False

    def load_sprite(self, ):
        # Create sprite
        if not self.sprite:
            self.sprite = pygame.image.load(self.img_path)
        self.scale_image(self.sprite)

    def scale_image(self, image):
        rect = image.get_rect()
        return pygame.transform.scale(
            image, (rect.width * self.scale_value, rect.height * self.scale_value))

    def scale_images(self, images):
        return [self.scale_image(img) for img in images]

    def draw(self):
        self.screen.blit(self.sprite, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):

    def __init__(self, x, y, screen, img_path=None):
        if img_path == None:
            img_path = os.path.join("animations", "ELF ANIMATIONS.png")
        super().__init__(x, y, screen, img_path)
        self.max_speed = 1000
        self.direction = 1
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
        self.load_shooting_animation()

    def load_shooting_animation(self, ):
        self.shoot_sound = pygame.mixer.Sound(
            os.path.join('sounds', 'Shot08.wav'))
        self.shooting = False
        self.shooting_images = self.scale_images(
            self.sheet.load_strip(self.rect, 13, 1, 4)
        )
        self.shoot_iter = Iter(self.shooting_images)

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

    def _calc_velocity(self):
        # do all velocity calculations with positive numbers to keep it simple
        # the "direction" modifier will convert it to `-` if needed
        velocity = abs(self.velocity)
        if self.accelerating:
            print("Accellerating")
            t = time.time() - self.move_start_time
            velocity = (t * self.acceleration)
        else:
            print("Decelerating")
            t = time.time() - self.move_stopped_time
            velocity = velocity - (t * self.deceleration)

        #  don't be slower than 0 and don't be faster than max
        velocity = min(max(0, velocity), self.max_speed)
        return velocity * self.direction

    # Don't care which direction as we can only be accelerating
    # in one direction so which ever one has a moving start time
    # that's the time we want
    def get_moving_time(self):
        t = time.time() - self.last_move_time
        print("t: %s" % t)
        return t

    def calculate_location(self, velocity):
        return [(self.velocity * self.get_moving_time()) + self.x_pos, self.y_pos]

    # Initialize the move but don't do it twice
    def start_move(self):
        if self.move_start_time is 0:
            self.move_start_time = time.time()
            self.move_stopped_time = 0
            self.last_move_time = time.time()
            self.walking = True
            self.accelerating = True

    # Initialize the stop but don't do it twice
    def stop_move(self):
        if self.move_stopped_time is 0:
            self.move_start_time = 0
            self.move_stopped_time = time.time()
            self.accelerating = False

    def walk(self):
        print("walking")
        self.velocity = self._calc_velocity()
        print("self.velocity: %s" % self.velocity)
        self.location = self.calculate_location(self.velocity)
        print("self.location: %s" % self.location)

        self._set_xy(self.location)
        self.last_move_time = time.time()
        print("self.last_move_time: %s" % self.last_move_time)
        if self.velocity is 0:
            self.stop_walk()

    def get_arrow(self):
        print("get_arrow")
        arrowSprite = self.sheet.load_single_sprite(self.rect, 2, 15)
        screen = self.screen

        class Arrow(GameObject):
            def __init__(self, x, y, direction):
                self.SPEED = 100
                self.direction = direction
                super().__init__(x, y, screen, sprite=arrowSprite)

            def move(self):
                self.x_pos += self.SPEED*self.direction
                self.draw()
                print("self.x_pos: %s" % self.x_pos)

        return Arrow(self.x_pos, self.y_pos, self.direction)

    def shoot(self):
        print("shooting")
        if not self.shooting:
            self.shoot_sound.play()
            self.break_for_animation()
            self.shooting = True
            # This should be held by the GAME itself.  Once the arrow leaves the player
            # this playerObject should care about it any more
            self.arrow = self.get_arrow()
            self.draw()
        try:
            self.sprite = self.shoot_iter.next()
            self.arrow.move()
        except StopIteration:
            self.shooting = False
            self.reset_breathing_animation()

    # completely stop the character
    def stop_walk(self,):
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
