

class StopIteration(Exception):
    pass


class Animation():
    # number of ticks to wait to iterate to next image
    FRAME_DELAY = 10

    def __init__(self, images):
        self.images = images

    #  Loop tells the iterator to keep cycling through
    #  the animation rather than raising StopIteration exception
    def iter(self, loop=False):
        return Iter(self.images, loop)


class Iter(Animation):
    def __init__(self, images, loop):
        self.idx = 0
        self.loop = loop
        self.frame = self.FRAME_DELAY
        self.images = images

    def next(self, ):
        if self.frame == 0:
            self.frame = self.FRAME_DELAY
            self.idx += 1
        self.frame -= 1

        if self.idx == len(self.images):
            self.idx = 0
            self.frame = self.FRAME_DELAY
            if not self.loop:
                raise StopIteration
        return self.images[self.idx]
