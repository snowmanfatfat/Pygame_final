FPS = 60
WIDTH = 1440
HEIGHT = 810

SPEED = 4
BULLET_SPEED = 15
WATERBALL_SPEED = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (242, 133, 0)
RED1 = (255, 87, 87)

import os
def get_path(directory):
    files = {}
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            subfolder = os.path.basename(dirpath)
            if subfolder not in files:
                files[subfolder] = []
            full_path = os.path.join(dirpath, filename)
            files[subfolder].append(full_path)
    return files