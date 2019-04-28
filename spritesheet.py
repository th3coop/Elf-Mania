# Adapted from http://www.pygame.org/wiki/Spritesheet?parent=CookBook
import pygame


class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def get_sprite(self, rectangle, colorkey=None):
        """
        @rectangle a rectangle representing the size of the sprite to save
            format of tuple (x_pos, y_pos, width, height)
            OR
            ((x_pos, y_pos), (width, height))

        @colorkey, the color to be made transparent when image is blitted on to screen
            passing in -1 will get colour from top left corner
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            if not isinstance(colorkey, pygame.Color):
                raise ValueError("'colorkey' was not a 'pygame.Color' object.")
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def get_sprites(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.get_sprite(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, start_row, rows, columns, colorkey=None):
        """
        Load a rects (pygame.Rect)s from the sheet for columns and rows given
        starting from the given row
        """
        rects = []
        for row in range(0, rows):
            for column in range(0, columns):
                newRect = (rect[0] + (rect[2] * column),
                           rect[1] + (rect[3] * (row + start_row)),
                           rect[2],
                           rect[3])
                rects.append(newRect)
        return self.get_sprites(rects, colorkey)
