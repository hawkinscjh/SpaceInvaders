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

# Player
# Player image source from https://www.flaticon.com/
playerImg = pygame.image.load("player.png")

# X and Y coordinates dependent on screen size (800 x 600 pixels)
playerX = 370
playerY = 480
playerX_change = 0


# Enemy
# Store values in lists to allow for multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    # Enemy image source from https://www.flaticon.com/
    enemyImg.append(pygame.image.load("enemy.png"))

    # X and Y coordinates dependent on screen size (800 x 600 pixels)
    enemyX.append(random.randint(0, 800))
    enemyY.append(0)
    enemyX_change.append(4)
    enemyY_change.append(20)

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

score_value = 0
# Score font will be freesansbold and size of 32 pixels
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
center_font = pygame.font.Font('freesansbold.ttf', 64)

# Paused font
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


# Game Loop
running = True
while running:

    if pause_state == False:

        # Setup screen's background color using RGB tuple
        # RGB = Red, Green, Blue, from 0 to 255
        screen.fill((0, 128, 0))

        # Background image
        screen.blit(background, (0, 0))

        # Create close button.
        # When pressed, will quit game loop by setting running = False
        # If game detects escape key is pressed, will also quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # If keystroke is pressed, check which key is pressed
            if event.type == pygame.KEYDOWN:
                # Pause game using P button
                if event.key == pygame.K_p:
                    paused()
                    pause_state = True
                    
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    playerX_change = 4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('shoot.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Update player's X-coordinate position (movement)
        playerX += playerX_change

        # Create boundaries to keep player from moving off screen
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Create boundaries to keep enemy from moving off screen
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            # Update enemy's X and Y-coordinate positions
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            # Reset bullet_state to ready, increase score, and respawn enemy
            if collision:
                explosion_sound = mixer.Sound('invaderkilled.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                # print(score_value)
                enemyX[i] = random.randint(0, 800)
                enemyY[i] = 0

            # Draw the enemy image
            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Draw the player image
        player(playerX, playerY)

        # Draw score to screen
        show_score(textX, textY)

        # Update display module to show screen changes
        pygame.display.update()
    if pause_state == True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_state = False
                if event.key == pygame.K_ESCAPE:
                    running = False
