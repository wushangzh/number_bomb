import os
import random


class GameInitials:
    def __init__(self):
        self.target_num = random.randint(0, 100)

        self.lower_bound = 0
        self.upper_bound = 100


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'res')
SOUND_PATH = os.path.join(RES_DIR, 'bomb.mp3')
