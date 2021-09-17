# Future changes to make:
# (1) Have enemies spawn and move uniformly
# (2) --Completed -- When all enemies are defeated, move on to Level 2 -- Completed --
# (3) Make Level 2 slightly harder than Level 1
# (4) After Level 2, move on to Level 3
# (5) Make Level 3 a boss battle of some kind
# (6) -- Completed -- Implement a pause feature -- Completed --
# (7) Improve points: Maybe double points for 3 hits without a miss?
# (8) Allow enemies to randomly drop bombs
# (9) A way to track lives (3 lives is typical, then game over)

from os import spawnl
import pygame, sys
# Mixer is used for music
from pygame import mixer
import sys
import random
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, x_change, score=0, lives=3):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.x_change = x_change
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = score
        self.lives = lives

    def playerMovement(self):
        self.pos_x += self.x_change
        self.rect.center = (self.pos_x, self.pos_y)
        # Create boundaries to keep player from moving off screen
        if self.pos_x <= 32:
            self.pos_x = 32
        elif self.pos_x >= 768:
            self.pos_x = 768

    def show_score(self, x, y):
        # Last tuple value (255, 255, 255) is color of the text being rendered
        score = score_font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (x, y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, x_change, y_change):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x_change = x_change
        self.y_change = y_change

    def enemyMovement(self):
        # Update enemy's X and Y-coordinate positions
        self.pos_x += self.x_change
        self.rect.center = (self.pos_x, self.pos_y)
        # Create boundaries to keep enemy from moving off screen
        if self.pos_x <= 32:
            self.x_change = -self.x_change
            self.pos_y += self.y_change
        elif self.pos_x >= 768:
            self.x_change = -self.x_change
            self.pos_y += self.y_change

    def spawnEnemies_1(self):
        x = 32
        for newEnemy in range(5):
            newEnemy = Enemy('enemy.png', 32 + x, 32, 4, 40)
            enemyGroup.add(newEnemy)
            x += 96
        x = 32
        for newEnemy in range(5):
            newEnemy = Enemy('enemy.png', 32 + x, 96, 4, 40)
            enemyGroup.add(newEnemy)
            x += 96
        x = 32
        for newEnemy in range(5):
            newEnemy = Enemy('enemy.png', 32 + x, 160, 4, 40)
            enemyGroup.add(newEnemy)
            x += 96

class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, x_change, y_change):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.pos_x = player.pos_x
        self.pos_y = pos_y
        self.x_change = x_change
        self.y_change = y_change
        self.bullet_state = 'ready'

    def bulletMovement(self, enemyGroup, bulletGroup):
        # Update enemy's X and Y-coordinate positions
        self.pos_x += self.x_change
        self.rect.center = (self.pos_x, self.pos_y)
        # Bullet movement
        if self.pos_y <= 0:
            self.kill()
            self.bullet_state = "ready"
        if self.bullet_state == "fire":
            self.fire()
            self.pos_y -= self.y_change
        # Check collision of bullet with enemy sprite
        if pygame.sprite.groupcollide(enemyGroup, bulletGroup, True, True):
            player.score += 1
            # Collision
            # Reset bullet_state to ready, increase score, and respawn enemy
            explosion_sound = mixer.Sound('invaderkilled.wav')
            explosion_sound.play()
            self.pos_y = player.pos_y
            self.bullet_state = "ready"

    def fire(self):
        if self.bullet_state == "ready":
            bullet_sound = mixer.Sound('shoot.wav')
            bullet_sound.play()
            self.pos_x = player.pos_x


class GameState():
    def __init__(self, level_tracker=1):
        self.state = 'intro'
        self.level_tracker = 1

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.state = 'level_1'

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(ready_text, (screen_width/2 - 118, screen_height/2 - 40))

        pygame.display.flip()

    def level_1(self):

        # Keep track of level for when the game is paused
        self.level_tracker = 1
        
        # Draw background to screen
        screen.blit(background, (0,0)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.state = 'paused'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.x_change = -8
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.x_change = 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
            # Press R to restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                enemyGroup.empty()
                bulletGroup.empty()
                playerGroup.empty()
                addPlayer()
                addEnemies_1()
                playerGroup.draw(screen)
                bulletGroup.draw(screen)
                enemyGroup.draw(screen)
                player.score = 0
                self.level_tracker = 1
                self.state = 'intro'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet('bullet.png', player.pos_x, player.pos_y, 0, 10)
                # Only allow one bullet being fired at a time.
                for bullet in bulletGroup:
                    bullet.kill()
                bulletGroup.add(bullet)
                bullet.bullet_state = 'fire'                   
 
        # Update player's X-coordinate position (movement)
        player.playerMovement()

        # Up date bullet's Y-coordinate position (movement)
        for bullet in bulletGroup:
            bullet.bulletMovement(enemyGroup, bulletGroup)
        
        # Update enemy's X and Y-coordinate positions (movement)
        for newEnemy in enemyGroup:
            newEnemy.enemyMovement()

            # Game Over
            if newEnemy.pos_y > 440:
                print(player.lives)
                if player.lives == 1:
                    self.state = 'game_over'
                else:
                    player.lives -= 1
                    enemyGroup.empty()
                    bulletGroup.empty()
                    playerGroup.empty()
                    addPlayer()
                    addEnemies_1()
                    playerGroup.draw(screen)
                    bulletGroup.draw(screen)
                    enemyGroup.draw(screen)
                    player.score = 0
                    self.level_tracker = 1
                    self.state = 'intro'
        # Need to reset the level. Right now it just stays in the same state, so of course my lives run out
        # quickly and game over.
    
        if player.score >= 15:
            self.state = 'level_2_intro'           

        # Drawing
        player.show_score(10,10)
        playerGroup.draw(screen)
        bulletGroup.draw(screen)
        enemyGroup.draw(screen)
        
        # Update display module to show screen changes
        pygame.display.update()

    def level_2(self):

        # Remove enemies from previous level
        for enemy in enemyGroup:
            enemy.kill()

        # Keep track of level for when the game is paused
        self.level_tracker = 2
        
        # Draw background to screen
        screen.blit(background, (0,0)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.state = 'paused'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.x_change = -8
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.x_change = 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
            # Press R to restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                enemyGroup.empty()
                bulletGroup.empty()
                playerGroup.empty()
                addPlayer()
                addEnemies_1()
                playerGroup.draw(screen)
                bulletGroup.draw(screen)
                enemyGroup.draw(screen)
                player.score = 0
                self.level_tracker = 1
                self.state = 'intro'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet('bullet.png', player.pos_x, player.pos_y, 0, 12)
                # Only allow one bullet being fired at a time.
                for bullet in bulletGroup:
                    bullet.kill()
                bulletGroup.add(bullet)
                bullet.bullet_state = 'fire'                
 
        # Update player's X-coordinate position (movement)
        player.playerMovement()

        # Up date bullet's Y-coordinate position (movement)
        for bullet in bulletGroup:
            bullet.bulletMovement(enemyGroup_2, bulletGroup)
        
        # Update enemy's X and Y-coordinate positions (movement)
        for newEnemy in enemyGroup_2:
            newEnemy.enemyMovement()
            # Game Over
            if newEnemy.pos_y > 440:
                if player.lives == 1:
                    self.state = 'game_over'
                else:
                    player.lives -= 1
                    enemyGroup.empty()
                    bulletGroup.empty()
                    playerGroup.empty()
                    addPlayer()
                    addEnemies_1()
                    playerGroup.draw(screen)
                    bulletGroup.draw(screen)
                    enemyGroup.draw(screen)
                    player.score = 0
                    self.level_tracker = 1
                    self.state = 'intro'
        
        if player.score >= 30:
            self.state = 'you_won'           

        # Drawing
        player.show_score(10,10)
        playerGroup.draw(screen)
        bulletGroup.draw(screen)
        enemyGroup_2.draw(screen)
        
        # Update display module to show screen changes
        pygame.display.update()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(over_text, (screen_width/2, screen_height/2))
        pygame.display.flip()

    def paused(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if self.level_tracker == 1:
                    self.state = 'level_1'
                elif self.level_tracker == 2:
                    self.state = 'level_2'
        screen.blit(pause_text, (screen_width/2, screen_height/2))
        pygame.display.flip()

    def you_won(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(won_text, (screen_height/2, screen_width/2))
        pygame.display.flip()

    def level_2_intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.state = 'level_2'

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(level_2_text, (screen_width/2, screen_height/2))

        pygame.display.flip()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'level_1':
            self.level_1()
        if self.state == 'game_over':
            self.game_over()
        if self.state == 'paused':
            self.paused()
        if self.state == 'you_won':
            self.you_won()
        if self.state == 'level_2_intro':
            self.level_2_intro()
        if self.state == 'level_2':
            self.level_2()

# General setup
pygame.init()
clock = pygame.time.Clock()
game_state = GameState()

# Game screen
screen_width =  800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('background.png')
# Title and Icon
pygame.display.set_caption("Space Invaders Clone")
# Icon image source from https://stock.adobe.com/
icon = pygame.image.load("space_ship.png")
pygame.display.set_icon(icon)
# Background sound source from: https://www.classicgaming.cc/
mixer.music.load('spaceinvaders1.mpeg')
# Loop music
mixer.music.play(-1)

# Font and text for intro
center_font = pygame.font.Font('freesansbold.ttf', 64)
ready_text = center_font.render("READY", True, (255, 255, 255))
over_text = center_font.render("GAME OVER", True, (255, 255, 255))
pause_text = center_font.render("PAUSED", True, (255, 255, 255))
won_text = center_font.render("YOU WON", True, (255, 255, 255))
level_2_text = center_font.render("Level 2", True, (255, 255, 255))
score_font = pygame.font.Font('freesansbold.ttf', 32)

# Player
# Player image source from https://www.flaticon.com/
playerGroup = pygame.sprite.Group()
def addPlayer():
    global player
    player = Player('player.png', 370, 568, 0)
    playerGroup.add(player)
addPlayer()

# Bullet
# Bullet image source from https://www.flaticon.com/
bullet = Bullet('bullet.png', player.pos_x, player.pos_y, 0, 10)
bulletGroup = pygame.sprite.Group()

# Enemy for Level 1
# Enemy image source from https://www.flaticon.com/
#global enemyGroup
enemyGroup = pygame.sprite.Group()
def addEnemies_1():
    x = 32
    for newEnemy in range(5):
        newEnemy = Enemy('enemy.png', 32 + x, 32, 4, 40)
        enemyGroup.add(newEnemy)
        x += 64
    x = 32
    for newEnemy in range(5):
        newEnemy = Enemy('enemy.png', 32 + x, 96, 4, 40)
        enemyGroup.add(newEnemy)
        x += 64
    x = 32
    for newEnemy in range(5):
        newEnemy = Enemy('enemy.png', 32 + x, 160, 4, 40)
        enemyGroup.add(newEnemy)
        x += 64

addEnemies_1()

# Enemy for Level 2
global enemyGroup_2
enemyGroup_2 = pygame.sprite.Group()
x = 32
for newEnemy in range(5):
    newEnemy = Enemy('enemy.png', 32 + x, 32, 6, 80)
    enemyGroup_2.add(newEnemy)
    x += 64
x = 32
for newEnemy in range(5):
    newEnemy = Enemy('enemy.png', 32 + x, 96, 6, 80)
    enemyGroup_2.add(newEnemy)
    x += 64
x = 32
for newEnemy in range(5):
    newEnemy = Enemy('enemy.png', 32 + x, 160, 6, 80)
    enemyGroup_2.add(newEnemy)
    x += 64

# Main game loop
def main():
    while True:
        game_state.state_manager()
        clock.tick(60)

main()