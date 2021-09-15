import pygame, sys, random, math
# Mixer is used for music
from pygame import mixer


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, x_change, score=0):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.x_change = x_change
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = score

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
            self.x_change = 4
            self.pos_y += self.y_change
        elif self.pos_x >= 768:
            self.x_change = -4
            self.pos_y += self.y_change      


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

    def bulletMovement(self):
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
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.state = 'main_game'

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(ready_text, (screen_width/2 - 118, screen_height/2 - 40))

        pygame.display.flip()

    def main_game(self):
        
        # Draw background to screen
        screen.blit(background, (0,0)) 
        # Bullet
        # Bullet image source from https://www.flaticon.com/
        #bulletGroup = pygame.sprite.Group()

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet('bullet.png', player.pos_x, player.pos_y, 0, 10)
                # Only allow one bullet being fired at a time.
                for bullet in bulletGroup:
                    bullet.kill()
                bulletGroup.add(bullet)
                bullet.bullet_state = 'fire'
                
                # Update display module to show screen changes
                
 
        # Update player's X-coordinate position (movement)
        player.playerMovement()

        # Up date bullet's Y-coordinate position (movement)
        for bullet in bulletGroup:
            bullet.bulletMovement()
        
        # Update enemy's X and Y-coordinate positions (movement)
        for newEnemy in enemyGroup:
            newEnemy.enemyMovement()  
    
        if player.score >= 5:
            self.state = 'game_over'
        # Game Over
        if newEnemy.pos_y > 440:
            self.state = 'game_over'

        # Drawing
        player.show_score(10,10)
        playerGroup.draw(screen)
        bulletGroup.draw(screen)
        enemyGroup.draw(screen)
        
        # Update display module to show screen changes
        pygame.display.update()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Drawing
        screen.blit(background, (0,0))
        screen.blit(over_text, (screen_width/2 - 118, screen_height/2 - 40))
        pygame.display.flip()

    def paused(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.state = 'main_game'
        screen.blit(pause_text, (screen_width/2 - 118, screen_height/2 - 40))
        pygame.display.flip()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'game_over':
            self.game_over()
        if self.state == 'paused':
            self.paused()

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

# Player
# Player image source from https://www.flaticon.com/
player = Player('player.png', 370, 568, 0)
playerGroup = pygame.sprite.Group()
playerGroup.add(player)

# Bullet
# Bullet image source from https://www.flaticon.com/
bullet = Bullet('bullet.png', player.pos_x, player.pos_y, 0, 10)
bulletGroup = pygame.sprite.Group()

# Enemy
# Enemy image source from https://www.flaticon.com/
enemyGroup = pygame.sprite.Group()
x = 32
for newEnemy in range(6):
    newEnemy = Enemy('enemy.png', 32 + x, 32, 8, 40)
    enemyGroup.add(newEnemy)
    x += 96

score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)

# Main game loop
while True:
    game_state.state_manager()
    clock.tick(60)