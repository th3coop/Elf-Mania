from typing import List

import pygame

Surface = pygame.surface.Surface


class StopIteration(Exception):
    pass


class Iter():
    frame_delay = 0

    def __init__(
            self,
            images: List[Surface], loop: bool = False, frame_delay: int = 5):
        # number of ticks to wait to iterate to next image
        self.frame_delay = frame_delay
        self.frame = frame_delay
        self.idx = 0
        self.loop = loop
        self.images = images

    def next(self, ):
        if self.frame <= 0:
            self.frame = self.frame_delay
            self.idx += 1
        self.frame -= 1

        if self.idx == len(self.images):
            self.idx = 0
            self.frame = self.frame_delay
            if not self.loop:
                raise StopIteration
        return self.images[self.idx]
