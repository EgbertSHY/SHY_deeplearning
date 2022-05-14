import os,pygame
import random


running = 1
size = [500,300]
FPS = 60

pygame.init()
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
player = pygame.image.load(os.path.join('image','player.png')).convert()
clock = pygame.time.Clock() 


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = player
        self.image_ori.set_colorkey((0,0,0)) 
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2
        self.rect.center = 250,150
        self.speed=8
        self.total_degree = 0
        self.degree = 2

    def update(self):
        self.total_degree += self.degree
        self.total_degree = self.total_degree % 360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        pygame.draw.rect(screen,(255,0,255),self.rect,2)

player = Player()
plane = pygame.sprite.Group()
plane.add(player)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    screen.fill((255,255,255))
    plane.update()
    plane.draw(screen)
    pygame.display.update()

pygame.quit()