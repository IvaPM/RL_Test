import time

class CachedFunction:
    def __init__(self, cached):
        self.countdown_time = time.time()+3*60
        self.counter = 1
        self.cached = cached

    def increase_counter(self):
        self.counter += 1

