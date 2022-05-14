import os,pygame
import random
pygame.init()

#設定變數
background = pygame.image.load(os.path.join('image','space.jpeg'))
player = pygame.image.load(os.path.join('image','player.png'))
#rock_img = pygame.image.load(os.path.join('image','rock3.png'))
bullet_img = pygame.image.load(os.path.join('image','bullet.png'))
rock_imgs=[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join('image',f'rock{i}.png')))
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
        self.image = pygame.transform.scale(player,(50,40))
        self.image.set_colorkey((0,0,0))    
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
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
            
    def shoot(self):
        bullet=Bullet(self.rect.centerx-5,self.rect.top-30)
        bullets.add(bullet)
#石頭
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image_ori = rock_img
        self.image_ori = random.choice(rock_imgs)
        self.image = self.image_ori.copy()        
        self.rect = self.image.get_rect()
        self.radius = self.rect.width*0.9/2
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.x = random.randrange(0,size[0]-40)
        self.rect.y = random.randrange(-79,-20)
        self.speedy = random.randrange(4,9)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-3,3)

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > size[1] or self.rect.right < 0 or self.rect.left > size[0]:
            self.rect.x = random.randrange(0,size[0]-40)
            self.rect.y = random.randrange(-100,-40)
            self.speed=random.randrange(3,10)
   
    #石頭動畫(旋轉)
    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

#子彈
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

#第一步:建立PLAYER
player=Player()
#第二步:建立群組
plane=pygame.sprite.Group()
obstacle=pygame.sprite.Group()
bullets=pygame.sprite.Group()
#第三步:將物件放入群組
plane.add(player)

#創造10顆石頭：
for i in range(10):
    rock=Rock()
    obstacle.add(rock)

#運行主程式
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                running=False
            if event.key == pygame.K_SPACE:   
                player.shoot()
    #更新遊戲物件(sprite)
    plane.update()
    obstacle.update()
    bullets.update()
    hits = pygame.sprite.spritecollide(player,obstacle,False,pygame.sprite.collide_circle)  #碰撞偵測方式
    if hits:
        running = False
        pygame.time.delay(1000)
    hits = pygame.sprite.groupcollide(obstacle,bullets,True,True)
    for i in hits:
        rock = Rock()
        obstacle.add(rock)
        
    #畫面顯示
    screen.blit(background,(0,0))   
    plane.draw(screen)
    obstacle.draw(screen)
    bullets.draw(screen)
    pygame.display.update()

pygame.quit()


