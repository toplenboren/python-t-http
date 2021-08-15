import time
from time import sleep

from progress.bar import Bar

class ProgressBar:
    def __init__(self):
        self.current = 0
        self.max = 100
        self.bar = None

    def start(self):
        print('')
        self.bar = Bar('Downloading', max=self.max)

    def set(self, percentage):
        percentage = int(percentage)
        if self.current != percentage:
            self.bar.next()
            self.current = percentage

    def finish(self):
        self.bar.finish()