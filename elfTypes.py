from typing import List, Tuple, Union

import pygame

Location = Tuple[float, float]
Surface = pygame.surface.Surface
# This Rect mirrors the type that pygame.Rect takes in it's second constructor
Rect = Union[
    pygame.Rect, Tuple[float, float, float, float], List[float]
]
