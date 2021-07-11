import unittest
import pygame
import animation
import os

test_data_dir = os.path.abspath("testdata")


class TestAnimation(unittest.TestCase):
    def test_init(self):
        images = ["enemy", "player", "treasure"]
        images_path = os.path.join(test_data_dir, "images")
        ext = ".png"
        pygame_images = []
        for i in images:
            pygame_images.append(pygame.image.load(
                os.path.join(images_path, i+ext)))
        iter = animation.Iter(pygame_images)
        self.assertEqual(5, iter.frame_delay, "Check default frame delay")
        self.assertEqual(False, iter.loop, "Check default loop arg")
