'''
Created on 2021 Sep 9

@author: Max
'''
import time, random

from pygame.locals import *
import pygame, sys

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
 
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN_BOTTOM = 0
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("background.jpg")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Ball Drop")


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) 
        
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 380), 0)


class Basket(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Basket.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if(self.rect.x >= (SCREEN_WIDTH - 145)):
            self.rect.x -= 5;
            
        elif(self.rect.x <= -5):
            self.rect.x += 5;
        
        else: 
            if pressed_keys[pygame.K_a]:
                self.rect.move_ip(-SPEED, 0)
        
            if pressed_keys[pygame.K_d]:
                self.rect.move_ip(SPEED, 0)


class Wall(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("wall.png")
        self.rect = self.image.get_rect()
        self.rect.center = (0, 680)


B2 = Basket()
B1 = Ball()
W1 = Wall()

balls = pygame.sprite.Group()
balls.add(B1)
walls = pygame.sprite.Group()
walls.add(W1)
all_sprites = pygame.sprite.Group()
all_sprites.add(B2)
all_sprites.add(B1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
 
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        
    if pygame.sprite.spritecollideany(W1, balls):
        pygame.mixer.Sound('gameover.wav').play()
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
           
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(4)
        pygame.quit()
        sys.exit()
 
    ball_hit = pygame.sprite.spritecollideany(B2, balls)
    if ball_hit:
        pygame.mixer.Sound('swish.wav').play()
        ball_hit.rect.center = (random.randint(30, 380), 0)
        SCORE += 1
         
    pygame.display.update()
    FramePerSec.tick(FPS)

