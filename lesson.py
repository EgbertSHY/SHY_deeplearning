import pygame
import random
import os
#宣告全域變數
running=True
size = width, height = 640, 480
background=(0,0,0)
FPS=60

#遊戲初始化&建立視窗
pygame.init()
screen=pygame.display.set_mode(size,pygame.RESIZABLE,32)
pygame.display.set_caption("星際大戰")
clock=pygame.time.Clock()

#載入圖片
background_img=pygame.image.load(os.path.join("img","background.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
rock_img=pygame.image.load(os.path.join("img","rock2.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()

#創建遊戲物件
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img        
        self.rect = self.image.get_rect()
        self.rect.centerx=width/2
        self.rect.centery=height-60
        self.speed=8
    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        """ if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed """
        if self.rect.right>width:
            self.rect.right=width
        if self.rect.left<0:
            self.rect.left=0
        """ if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>height:
            self.rect.bottom=height """
    def shoot(self):
        bullet=Bullet(self.rect.x+15,self.rect.y-30)
        allsprite.add(bullet)
        bullets.add(bullet)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img        
        self.rect = self.image.get_rect()
        self.rect.x=random.randrange(0,width-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedx=random.randrange(-4,4)
        self.speedy=random.randrange(2,8)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x > width or self.rect.right <0 or self.rect.y > height :
            self.rect.x=random.randrange(0,width-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-4,4)
            self.speedy=random.randrange(2,8)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=10
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill() 

allsprite=pygame.sprite.Group()
bullets=pygame.sprite.Group()
rocks=pygame.sprite.Group()
player=Player()
allsprite.add(player)
for i in range(8):
    rock=Rock()
    allsprite.add(rock)
    rocks.add(rock)

#遊戲迴圈
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()
    #更新物件
    allsprite.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for i in hits:
        rock=Rock()
        allsprite.add(rock)
        rocks.add(rock)
    hits=pygame.sprite.spritecollide(player,rocks,False)
    if hits:
        running=False
    #畫面顯示
    screen.fill(background)
    screen.blit(background_img,(0,0))
    allsprite.draw(screen)
    pygame.display. update()

pygame.quit()