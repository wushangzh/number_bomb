import os
import random


class GameInitials:
    def __init__(self):
        self.target_num = random.randint(0, 100)

        self.lower_bound = 0
        self.upper_bound = 100

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.res_dir = os.path.join(os.path.dirname(self.current_dir), 'res')
        self.sound_path = os.path.join(self.res_dir, 'bomb.mp3')
