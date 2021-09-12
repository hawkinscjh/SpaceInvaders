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
# (11) Rewrite game code to class objects to better organize code


import pygame
# Mixer is used for music
from pygame import mixer
import random
import math
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, playerX, playerY, playerX_change, score):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [playerX, playerY]
        self.score = 0

    def show_score(self, x, y):
        # Last tuple value (255, 255, 255) is color of the text being rendered
        score_text = score_font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(self.score, (x, y))

    def player(self, x, y):
        # blit = draw image to screen
        # draw playerImg to given X and Y coordinate on screen
        screen.blit(playerImg, (x, y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, picture_path, enemyX, enemyY, enemyX_change, enemyY_change):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [enemyX, enemyY]

    def enemy(self, x, y, i):
        # blit = draw image to screen
        # draw enemyImg to given X and Y coordinate on screen
        screen.blit(enemyImg_group, (x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, bulletX, bulletY, bulletX_change, bulletY_change, bullet_state):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [bulletX, bulletY]
        self.bullet_state = 'ready'
        self.bullet_sound = pygame.mixer.Sound('shoot.wav')

    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.bullet_sound.play()
        self.bulletX = playerImg.playerX
        bulletImg.fire_bullet(bulletImg.bulletX, bulletImg.bulletY)
        screen.blit(bulletImg, (x + 16, y + 10))
        if pygame.sprite.spritecollide(bulletImg_group, enemyImg_group, True):
            playerImg.score += 1
            print(self.score)


class GameState():
    def __init__(self):
        self.state = 'intro'

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'game_over':
            self.game_over()

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.fill((0, 128, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused()
                    pause_state = True
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    playerX_change = 4
                if event.key == pygame.K_SPACE:
                    if bulletImg.bullet_state == "ready":
                        bulletImg.fire_bullet()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerImg.playerX += playerX_change

        # Create boundaries to keep player from moving off screen
        if playerImg.playerX <= 0:
            playerX = 0
        elif playerImg.playerX >= 736:
            playerX = 736

        # Create boundaries to keep enemy from moving off screen
        for i in range(6):

            # Game Over
            if enemyImg_group.enemyY > 440:
                for j in range(6):
                    enemyImg_group.enemyY = 2000
                game_state.game_over_text()
                break

            # Update enemy's X and Y-coordinate positions
            enemyImg_group.enemyX += enemyImg_group.enemyX_change
            if enemyImg_group.enemyX <= 0:
                enemyImg_group.enemyX_change = 4
                enemyImg_group.enemyY += enemyImg_group.enemyY_change
            elif enemyImg_group.enemyX >= 736:
                enemyImg_group.enemyX_change = -4
                enemyImg_group.enemyY += enemyImg_group.enemyY_change

            # Collision
            collision = bulletImg.isCollision(enemyImg_group.enemyX, enemyImg_group.enemyY, bulletImg.bulletX, bulletImg.bulletY)
            # Reset bullet_state to ready, increase score, and respawn enemy
            if collision:
                explosion_sound = mixer.Sound('invaderkilled.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                playerImg.score += 1
                # print(score_value)

            # Draw the enemy image
            enemy(enemyImg_group.enemyX, enemyImg_group.enemyY, i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            bulletImg.fire_bullet(bulletImg.bulletX, bulletImg.bulletY)
            bulletY -= bulletImg.bulletY_change

        # Draw the player image
        playerImg.player(playerImg.playerX, playerImg.playerY)

        # Draw score to screen
        playerImg.show_score(10, 10)

        # Update display module to show screen changes
        pygame.display.update()

    def paused():
        pause_text = center_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (200, 250))

    def game_over_text():
        over_text = center_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))
        

# Initialize the pygame
pygame.init()
clock = pygame.time.Clock()
game_state = GameState()

# Create screen
# Input height and width of display window (800 pixels wide, 600 pixels height)
screen_width =  800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Background image source from: https://pixabay.com/
background = pygame.image.load("background.png")

# Music
# Background music source from: https://www.classicgaming.cc/
mixer.music.load('spaceinvaders1.mpeg')
# Loop music
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders Clone")
# Icon should be 32x32 pixels and PNG
# Set icon = png name
# Icon image source from https://stock.adobe.com/
icon = pygame.image.load("space_ship.png")
# Load icon into pygame's display module
pygame.display.set_icon(icon)

# Player
# Player image source from https://www.flaticon.com/
playerImg = Player('player.png', 370, 480, 0, 0)
playerImg_group = pygame.sprite.Group()
playerImg_group.add(playerImg)

# Enemy
enemyImg_group = pygame.sprite.Group()
for enemy in range(6):
    new_enemy = Enemy('enemy.png', random.randint(0, 800), 0, 4, 20)
    enemyImg_group.add(new_enemy)

# Bullet
# Bullet image source from https://www.flaticon.com/
bulletImg = Bullet('bullet.png', 0, 480, 0, 10, 'ready')
bulletImg_group = pygame.sprite.Group()
bulletImg_group.add(bulletImg)

score_font = pygame.font.Font('freesansbold.ttf', 32)
center_font = pygame.font.Font('freesansbold.ttf', 64)
ready_text = center_font.render("READY", True, (255, 255, 255))
over_text = center_font.render("GAME OVER", True, (255, 255, 255))

# Game Loop
running = True
while running:
    game_state.state_manager()
    clock.tick(60)
