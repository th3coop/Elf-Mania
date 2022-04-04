# Adapted from http://www.pygame.org/wiki/Spritesheet?parent=CookBook
from pathlib import Path
from typing import List, Optional, Tuple

import pygame

import elfTypes


class Spritesheet(object):
    sheet: elfTypes.Surface
    # Defaults to the top, left corner of the sprite sheet
    color_key: pygame.Color

    def __init__(
        self,
        filename: Path,
        color_key_loc: Optional[Tuple[int]] = None
    ):
        self.sheet = pygame.image.load(filename)
        ckl: Tuple[int] = tuple((0, 0))
        if color_key_loc is not None:
            ckl = color_key_loc
        self.color_key = pygame.Color(self.sheet.get_at(ckl))

    def getSprite(
        self,
        rectangle: elfTypes.Rect,
        colorkey: Optional[pygame.Color] = None
    ):
        """
        @rectangle a rectangle representing the size of the sprite to save
            format of tuple (x_pos, y_pos, width, height) OR ((x_pos, y_pos),
            (width, height))

        @colorkey, the color to be made transparent when image is blitted on to
        screen
            passing in -1 will get colour from top left corner
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            print("We are using colorkey")
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def getSprites(
        self,
        rects: List[elfTypes.Rect],
        colorkey: Optional[pygame.Color] = None
    ) -> List[elfTypes.Surface]:
        "Loads multiple images, supply a list of coordinates"
        return [self.getSprite(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def loadStrip(
        self,
        rect: elfTypes.Rect,
        start_row: int,
        rows: int,
        columns: int,
        colorkey: Optional[pygame.Color] = None
    ) -> List[elfTypes.Surface]:
        """
        Load a rects (pygame.Rect)s from the sheet for columns and rows given
        starting from the given row
        """
        rects: List[elfTypes.Rect] = []
        for row in range(0, rows):
            for column in range(0, columns):
                newRect: elfTypes.Rect = (rect[0] + (rect[2] * column),
                                          rect[1] +
                                          (rect[3] * (row + start_row)),
                                          rect[2],
                                          rect[3])
                rects.append(newRect)
        return self.getSprites(rects, colorkey)
