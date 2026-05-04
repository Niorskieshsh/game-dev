import pygame
import os

# STATES
MENU = "menu"
MAP_SELECT = "map_select"
LEVEL_SELECT = "level_select"
GAME = "game"
SETTINGS_MENU = "settings"

# MENU BACKGROUND (FIX)
MENU_BG = "images/ui/bg1.jpg"

# MAPS
MAPS = {
    "map1": "images/maps/bg2.jpg",
    "map2": "images/maps/bg3.jpg",
    "map3": "images/maps/bg4.jpg",
    "map4": "images/maps/bg5.jpg",
    "map5": "images/maps/bg6.jpg"
}

# PLAYER SETTINGS
START_X = 300
START_Y_OFFSET = 220
SCREEN_CENTER_Y = 0

PLAYER_SPEED = 5
PLAYER_RUN_SPEED = 8

GRAVITY = 0.9
JUMP_POWER = -18

ANIMATION_SPEED = 0.15

VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720