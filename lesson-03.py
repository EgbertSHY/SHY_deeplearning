import os,pygame
import random
pygame.init()

#設定變數
background = pygame.image.load(os.path.join('image','space.jpeg'))
player = pygame.image.load(os.path.join('image','player.png'))
size = background.get_size()
FPS=60
clock=pygame.time.Clock()        
running=True

#設定畫面及標題
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
pygame.display.set_caption("星際大戰")
pygame.display.set_icon(pygame.image.load(os.path.join('image','icon.png')).convert())

#小飛機
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player,(75,50))
        self.image.set_colorkey((0,0,0))    
        self.rect = self.image.get_rect()
        self.rect.centerx=(size[0]-38)/2
        self.rect.bottom = size[1]
        self.speed=8

    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if self.rect.right > size[0]:
            self.rect.right=size[0]
        if self.rect.left < 0:
            self.rect.left=0
#石頭
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,size[0]-40)
        self.rect.y = random.randrange(-79,-20)
        self.speedy = random.randrange(4,9)
        self.speedx = random.randrange(-3,3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > size[1] or self.rect.right < 0 or self.rect.left > size[0]:
            self.rect.x = random.randrange(0,size[0]-40)
            self.rect.y = random.randrange(-100,-40)
            self.speed=random.randrange(3,10)

#第一步:建立PLAYER
player=Player()
#第二步:建立群組
plane=pygame.sprite.Group()
obstacle=pygame.sprite.Group()
#第三步:將物件放入群組
plane.add(player)

#創造10顆石頭：
for i in range(10):
    rock=Rock()
    obstacle.add(rock)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
               running=False
  
    #更新遊戲物件(sprite)
    plane.update()
    obstacle.update()

    #畫面顯示
    screen.blit(background,(0,0))   
    plane.draw(screen)
    obstacle.draw(screen)
    pygame.display.update()

pygame.quit()