FPS = 60
WIDTH = 1440
HEIGHT = 810

SPEED = 4
BULLET_SPEED = 15
WATERBALL_SPEED = 12
FIREATK_SPEED = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (242, 133, 0)
RED1 = (255, 87, 87)
BLUE = (0, 0, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_GRAY = (50, 50, 50, 10)
LIGHT_GRAY = (200, 200, 200)
LIGHT_YELLOW = (255, 255, 153)

import os
import pygame

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

# a = get_path(".")
# codes = [code.replace(".\\", "") for code in a["."]]
# codes = " ".join(codes)
# print(codes)
# pyreverse -o png -p MyProject boss.py building.py buttons.py explosion.py fire.py fireball.py game.py ground.py main.py mana.py player.py power.py projectile.py rock.py setting.py setting_menu.py soundset.py start_menu.py tutorial.py ultimate.py
