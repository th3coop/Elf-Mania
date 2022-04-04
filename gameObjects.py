import os
import time
from pathlib import Path
from typing import List, Optional

import pygame

import elfTypes
from animation import Iter, StopIteration
from spritesheet import Spritesheet


class GameObject:
    x_pos: float
    y_pos: float
    acceleration: int
    deceleration: int
    location: elfTypes.Location
    pre_offset_pos: elfTypes.Location
    sprite: elfTypes.Surface
    sprite_sheet: Optional[Spritesheet]

    def __init__(
        self,
        x: int,
        y: int,
        img_path: Path,
        use_sprite_sheet: bool = True
    ):
        self.img_path = img_path
        if use_sprite_sheet:
            self.sprite_sheet = Spritesheet(self.img_path)
        else:
            self.loadSprite()
            self.sprite_sheet = None

        self.initializeMovementProps()

        self.scale_value = 2
        # deal with these later when we start moving things...i think use Rects
        # will eliminate the need for a buffer though self.btm_buffer = (20 +
        # self.height) self.right_buffer = (20 + self.width)

        self.pre_offset_pos = (x, y)
        self.acceleration = 1000
        self.deceleration = 100
        self.location = (x, y)
        self._setXY()
        # max(y, self.btm_buffer)
        # [x_speed, y_speed]

    def _setXY(self) -> None:
        self.x_pos = self.location[0]
        self.y_pos = self.location[1]

    def initializeMovementProps(self,):
        self.move_start_time = 0
        self.move_stopped_time = 0
        self.velocity = 0
        self.last_move_time = 0
        self.accelerating = False

    def loadSprite(self) -> None:
        # Create sprite
        self.sprite = pygame.image.load(self.img_path)
        self.scaleImage(self.sprite)

    def scaleImage(self, image: elfTypes.Surface) -> elfTypes.Surface:
        rect = image.get_rect()
        return pygame.transform.scale(
            image,
            (rect.width * self.scale_value, rect.height * self.scale_value)
        )

    def scaleImages(
        self,
        images: List[elfTypes.Surface]
    ) -> List[elfTypes.Surface]:
        return [self.scaleImage(img) for img in images]

    def draw(self, screen: elfTypes.Surface):
        screen.blit(self.sprite, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    rect: elfTypes.Rect
    sprite_sheet: Spritesheet

    def __init__(self, x: int, y: int, img_path: Optional[Path] = None):
        img_path = img_path or Path(os.path.join(
            "animations", "ELF ANIMATIONS.png"))
        super().__init__(x, y, img_path,)
        self.max_speed = 1000
        self.direction = 0
        # These are specific to ELF ANIMATION.PNG
        self.sprite_width = 31
        self.sprite_height = 31
        # top_padding apparent gap at top of file that is uneven with gaps
        # between rows of images I could be setting sprite_[width/height] wrong
        # but those should be even you'd think
        self.top_padding = 4.5
        # rect is the pygame.Rect dimension of individual sprites in your
        #  spritesheet defaults to top left corner of sheet
        self.rect = (0, 0, self.sprite_width, self.sprite_height)
        self.loadBreathingAnimation()
        self.loadJumpAnimation()
        self.loadWalkAnimation()

    def loadBreathingAnimation(self, ):
        self.breath_images = self.scaleImages(
            self.sprite_sheet.loadStrip(self.rect, 0, 1, 4)
        )
        self.breath_iter = Iter(self.breath_images, True)

        self.sprite = self.breath_iter.next()
        self.breathing = True

    def loadJumpAnimation(self, ):
        self.jump_sound = pygame.mixer.Sound(os.path.join(
            'sounds', 'Retro_8-Bit_Game-Jump_Lift_TakeOff_06.wav'))
        self.jump_idx = 0
        self.jumping = False
        self.jump_images = self.scaleImages(
            self.sprite_sheet.loadStrip(self.rect, 1, 2, 4))
        self.jump_iter = Iter(self.jump_images)

    def loadWalkAnimation(self, ):
        self.walk_sound = pygame.mixer.Sound(os.path.join(
            'sounds', 'one-foot-step.wav'))
        self.walking = False
        self.walk_images = self.scaleImages(
            self.sprite_sheet.loadStrip(self.rect, 3, 1, 4))
        self.walk_iter = Iter(self.walk_images, True)

    # This function will handle any play state changes that need to occur before
    #  the playert animation changes.
    def breakForAnimation(self, ):
        self.breathing = False

    # This function should be called when a particular animation cycle has
    # completed
    def resetBreathingAnimation(self, ):
        self.breathing = True
        self.sprite = self.breath_iter.next()

    def breath(self):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        self.sprite = self.breath_iter.next()

    def _calcVelocity(self):
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
    def getMovingTime(self):
        t = time.time() - self.last_move_time
        print("t: %s" % t)
        return t

    def calculateLocation(self) -> elfTypes.Location:
        return tuple(
            ((self.velocity * self.getMovingTime()) + self.x_pos, self.y_pos)
        )

    # Initialize the move but don't do it twice
    def startMove(self):
        if self.move_start_time == 0:
            self.move_start_time = time.time()
            self.move_stopped_time = 0
            self.last_move_time = time.time()
            self.walking = True
            self.accelerating = True

    # Initialize the stop but don't do it twice
    def stopMove(self):
        if self.move_stopped_time == 0:
            self.move_start_time = 0
            self.move_stopped_time = time.time()
            self.accelerating = False

    def walk(self):
        print("walking")
        self.velocity = self._calcVelocity()
        print("self.velocity: %s" % self.velocity)
        self.location = self.calculateLocation()
        print("self.location: %s, %s" % self.location)

        self._setXY()
        self.last_move_time = time.time()
        print("self.last_move_time: %s" % self.last_move_time)
        if self.velocity == 0:
            self.stopWalk()

    # completely stop the character
    def stopWalk(self,):
        self.direction = 0
        self.walking = False
        self.resetBreathingAnimation()

    def jump(self,):
        # assumes character as already been positioned in idx 0 in __init__.
        #  Perhaps not good coupling of the two functions.
        if not self.jumping:
            self.jump_sound.play()
            self.breakForAnimation()
        self.jumping = True
        try:
            self.sprite = self.jump_iter.next()
        except StopIteration:
            self.jumping = False
            self.resetBreathingAnimation()

        # print("self.y_pos: %s" %self.y_pos)
        # print("self.jump_idx: %s" %self.jump_idx)

    # def move(self, direction: int, max_height: int):
    #     # Y increase as you go down so to move UP on the
    #     # screen you must decrement Y
    #     if direction > 0:
    #         self.y_pos -= self.SPEED
    #     elif direction < 0:
    #         self.y_pos += self.SPEED
    #     if self.y_pos >= max_height - self.btm_buffer:
    #         self.y_pos = max_height - self.btm_buffer

    # def collisionDetected(self, other_body):
    #     if (self.y_pos + self.height) < other_body.y_pos:
    #         return False
    #     elif self.y_pos > (other_body.y_pos + other_body.height):
    #         return False
    #     if self.x_pos > (other_body.x_pos + other_body.width):
    #         return False
    #     elif (self.x_pos + self.width) < other_body.x_pos:
    #         return False
    #     return True


# class EnemyCharacter(GameObject):
#     SPEED = 5

#     def __init__(self, x, y):
#         # How many spaces to move per move
#         super().__init__(x, y, os.path.join("imgs", "enemy.png"))

#     def move(self, screen_width, multiplier=1):
#         if self.x_pos <= 20:
#             self.SPEED = abs(self.SPEED)
#         if self.x_pos >= (screen_width - self.right_buffer):
#             self.SPEED = -abs(self.SPEED)
#         self.x_pos += self.SPEED

#     # def detect_colision(self)
