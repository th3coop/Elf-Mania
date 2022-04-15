from pathlib import Path
from typing import List, Optional

import pygame

import lib.elfTypes as elfTypes
from lib.spritesheet import Spritesheet


"""A sprite is basically anything that is loaded into the game as an on screen
(in theory could be off screen) asset.  The player's character is a sprite.
NPC's are sprites.  Any prop is a sprite.  It may be able to move or not. It may
have a hit box or not.
"""


class Sprite:
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
            use_sprite_sheet: bool = True):
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
