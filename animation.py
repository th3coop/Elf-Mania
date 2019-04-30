

class StopIteration(Exception):
    pass


class Iter():
    FRAME_DELAY = 0

    def __init__(self, images, loop=False, frame_delay=5):
        # number of ticks to wait to iterate to next image
        self.FRAME_DELAY = frame_delay
        self.frame = frame_delay
        self.idx = 0
        self.loop = loop
        self.images = images

    def next(self, ):
        if self.frame <= 0:
            self.frame = self.FRAME_DELAY
            self.idx += 1
        self.frame -= 1

        if self.idx == len(self.images):
            self.idx = 0
            self.frame = self.FRAME_DELAY
            if not self.loop:
                raise StopIteration
        return self.images[self.idx]
