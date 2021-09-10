# Future changes to make:
# (1) Have enemies spawn and move uniformly
# (2) When all enemies are defeated, move on to Level 2
# (3) Make Level 2 slightly harder than Level 1
# (4) After Level 2, move on to Level 3
# (5) Make Level 3 a boss battle of some kind
# (6) -- Completed -- Implement a pause feature -- Completed --
# (7) Improve points: Maybe double points for 3 hits without a miss?
# (8) Allow enemies to randomly drop bombs
# (9) A way to track lives (3 lives is typical, then game over)
# (10) Game over when an enemy runs into you, not when they move just to 480 Y-axis

import pygame
# Mixer is used for music
from pygame import mixer
import random
import math


#class GameState():
#    def __init__(self):
#        self.state = main_game'
#
#    def main_game(self):

class Player():
    def __init__(self, playerX, playerY, playerX_change, image):
        # Player
        # Player image source from https://www.flaticon.com/
        self.image = pygame.image.load("player.png")

        # X and Y coordinates dependent on screen size (800 x 600 pixels)
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0

class Enemy():
    def __init__(self, enemyX, enemyY, enemyX_change, enemyY_change, image, num_of_enemies):
        # Enemy
        # Store values in lists to allow for multiple enemies
        self.image = []
        self.enemyX = []
        self.enemyY = []
        self.enemyX_change = []
        self.enemyY_change = []
        self.num_of_enemies = 6

        for i in range(num_of_enemies):
            # Enemy image source from https://www.flaticon.com/
            self.image.append(pygame.image.load("enemy.png"))

            # X and Y coordinates dependent on screen size (800 x 600 pixels)
            self.enemyX.append(random.randint(0, 800))
            self.enemyY.append(0)
            self.enemyX_change.append(4)
            self.enemyY_change.append(20)

class bullet():
    def __init__(self, bulletX, bulletY, bullet)
    # Bullet
    # Bullet image source from https://www.flaticon.com/
    bulletImg = pygame.image.load("bullet.png")

    # X and Y coordinates dependent on screen size (800 x 600 pixels)
    bulletX = 0
    bulletY = 480           # Player top is at 480 pixels, and bullet will shoot from top of player
    bulletX_change = 0
    bulletY_change = 10

    # Ready state = Bullet is hidden from screen
    # Fire state = Bullet is unhidden and moving
    bullet_state = "ready"


# Initialize the pygame
pygame.init()

# Create screen
# Input height and width of display window (800 pixels wide, 600 pixels height)
screen = pygame.display.set_mode((800, 600))

# Background image source from: https://pixabay.com/
background = pygame.image.load("background.png")

# Background sound source from: https://www.classicgaming.cc/
mixer.music.load('spaceinvaders1.mpeg')
# Loop music
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders Clone")

# Icon must be 32x32 pixels and PNG
# Set icon = png name
# Icon image source from https://stock.adobe.com/
icon = pygame.image.load("space_ship.png")

# Load icon into pygame's display module
pygame.display.set_icon(icon)

score_value = 0
# Score font will be freesansbold and size of 32 pixels
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Font for larger letters
center_font = pygame.font.Font('freesansbold.ttf', 64)

# Pause state starts out False. Pressing P will trigger pause_state = True
pause_state = False


def paused():
    pause_text = center_font.render("PAUSED", True, (255, 255, 255))
    # Print to middle of the screen
    screen.blit(pause_text, (200, 250))


def game_over_text():
    over_text = center_font.render("GAME OVER", True, (255, 255, 255))
    # Print to middle of the screen
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    # Last tuple value (255, 255, 255) is color of the text being rendered
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # blit = draw image to screen
    # draw playerImg to given X and Y coordinate on screen
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit = draw image to screen
    # draw enemyImg to given X and Y coordinate on screen
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # x+16 for bullet to appear at center of playerImg, y+10 for bullet to appear from top of player
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 20:
        return True
    else:
        return False

# Game loop
running = True
level_1_loop = True
while level_1_loop:

    