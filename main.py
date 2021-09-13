import pygame, sys, random, math
# Mixer is used for music
from pygame import mixer
from pygame.constants import KEYDOWN


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, x_change):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.x_change = x_change
        self.pos_x = pos_x
        self.pos_y = pos_y

    def playerDraw(self, pos_x, pos_y):
        # blit = draw image to screen
        # draw playerImg to given X and Y coordinate on screen
        screen.blit(playerPic, (pos_x, pos_y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, x_change, y_change):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.x_change = x_change
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.y_change = y_change

    def enemyDraw(self, pos_x, pos_y):
        # blit = draw image to screen
        # draw playerImg to given X and Y coordinate on screen
        screen.blit(enemyPic, (pos_x, pos_y))


class GameState():
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(ready_text, (screen_width/2 - 118, screen_height/2 - 40))
        #crosshair_group.draw(screen)
        #crosshair_group.update()
        pygame.display.flip()

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.x_change = -4
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.x_change = 4
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   player.x_change = 0

        # Update player's X-coordinate position (movement)
        player.pos_x += player.x_change

        # Create boundaries to keep player from moving off screen
        if player.pos_x <= 0:
            player.pos_x = 0
        elif player.pos_x >= 736:
            player.pos_x = 736

        # Create boundaries to keep enemy from moving off screen
            # Game Over
        if newEnemy.pos_y > 440:
            newEnemy.pos_y = 2000
            self.state = 'game_over'

        # Update enemy's X and Y-coordinate positions
        newEnemy.pos_x += newEnemy.x_change
        if newEnemy.pos_x <= 0:
            newEnemy.x_change = 4
            newEnemy.pos_y += newEnemy.y_change
        elif newEnemy.pos_x >= 736:
            newEnemy.x_change = -4
            newEnemy.pos_y += newEnemy.y_change

        # Drawing
        screen.blit(background, (0,0))
        #enemy_group.draw(screen)
        #player_group.draw(screen)
        player.playerDraw(player.pos_x, player.pos_y)
        newEnemy.enemyDraw(newEnemy.pos_x, newEnemy.pos_y)
        player.update()

        # Update display module to show screen changes
        pygame.display.update()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(over_text, (screen_width/2 - 118, screen_height/2 - 40))
        #crosshair_group.draw(screen)
        #crosshair_group.update()
        pygame.display.flip()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'game_over':
            self.game_over()

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

# Player
# Player image source from https://www.flaticon.com/
playerPic = pygame.image.load('player.png')
player = Player('player.png', 370, 480, 0)
#player_group = pygame.sprite.Group()
#player_group.add(playerImg)

# Enemy
# Enemy image source from https://www.flaticon.com/
enemyPic = pygame.image.load('enemy.png')
enemyGroup = pygame.sprite.Group()
for enemy in range(6):
    newEnemy = Enemy('enemy.png', random.randrange(0, screen_width), random.randrange(0, 150), 4, 20)
    enemyGroup.add(newEnemy)


# Main game loop
while True:
    game_state.state_manager()
    clock.tick(60)