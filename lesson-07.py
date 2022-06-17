import os,pygame
from numpy import polyder
import random
pygame.init()
pygame.mixer.init()

#載入圖片
background = pygame.image.load(os.path.join('image','space.jpeg'))
player = pygame.image.load(os.path.join('image','player.png'))
player_mini = pygame.transform.scale(player, (25,25))
player_mini.set_colorkey((0,0,0))
bullet_img = pygame.image.load(os.path.join('image','bullet.png'))
rock_imgs=[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join('image',f'rock{i}.png')))
expl_animation = {}
expl_animation['lg'] = []
expl_animation['sm'] = []
expl_animation['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join('image',f'expl{i}.png'))
    expl_img1 = pygame.image.load(os.path.join('image',f'player_expl{i}.png'))
    expl_img.set_colorkey((0,0,0))
    expl_img1.set_colorkey((0,0,0))
    expl_animation['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_animation['sm'].append(pygame.transform.scale(expl_img, (30,30)))
    expl_animation['player'].append(pygame.transform.scale(expl_img1, (75,75)))

#設定變數
size = background.get_size()
FPS=60
clock=pygame.time.Clock()        
running=True
score = 0

#載入音效
shoot_sound = pygame.mixer.Sound(os.path.join('sound','shoot.wav'))
explo_sound = [pygame.mixer.Sound(os.path.join('sound','expl0.wav')), pygame.mixer.Sound(os.path.join('sound','expl1.wav'))]
pygame.mixer.music.load((os.path.join('sound','background.ogg')))
die_sound = pygame.mixer.Sound((os.path.join('sound','rumble.ogg')))
pygame.mixer.music.set_volume(0.6)

#設定畫面及標題
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
pygame.display.set_caption("星際大戰")
pygame.display.set_icon(pygame.image.load(os.path.join('image','icon.png')).convert())

font_name = pygame.font.match_font('arial')

#顯示分數副函式
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
#顯示生命條副函式
def draw_health(surf, hp, x, y):
    rect_length = 100
    rect_height = 10
    fill = (hp/100)*rect_length
    health_rect = pygame.Rect(x, y, rect_length, rect_height)
    fill_rect = pygame.Rect(x, y, fill, rect_height)
    pygame.draw.rect(surf, (0,255,0), fill_rect)
    pygame.draw.rect(surf, (255,255,255), health_rect, 2)
#顯示飛機剩餘幾命副函式
def draw_lifes(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

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
        self.health = 100
        self.lifes = 3
        self.hidden = False
        self.hide_time = 0

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx=(size[0]-38)/2
            self.rect.bottom = size[1]
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
        if self.hidden == False:
            bullet=Bullet(self.rect.centerx-5,self.rect.top-30)
            bullets.add(bullet)
            shoot_sound.play()
    
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (size[0]/2, size[1]+500)
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
#爆炸效果
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_animation[self.size]):
                self.kill()
            else:
                self.image = expl_animation[self.size][self.frame]
        """ self.frame +=1
        if self.frame == len(expl_animation[self.size]):
            self.kill()
        else:
            self.image = expl_animation[self.size][self.frame] """

#第一步:建立PLAYER
player=Player()
#第二步:建立群組
effect_sprite = pygame.sprite.Group()
plane=pygame.sprite.Group()
obstacle=pygame.sprite.Group()
bullets=pygame.sprite.Group()
#第三步:將物件放入群組
plane.add(player)

#創造10顆石頭：
for i in range(10):
    rock=Rock()
    obstacle.add(rock)

pygame.mixer.music.play(-1)

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
    effect_sprite.update()
    plane.update()
    obstacle.update()
    bullets.update()
    hits = pygame.sprite.spritecollide(player,obstacle,True,pygame.sprite.collide_circle)  #碰撞偵測方式
    for i in hits:
        rock = Rock()
        obstacle.add(rock)
        explo_sound[0].play()
        expl = Explosion(i.rect.center, 'sm')
        effect_sprite.add(expl)
        player.health -= i.radius
        if player.health <= 0:
            player_expl = Explosion(player.rect.center, 'player')
            effect_sprite.add(player_expl)
            die_sound.play()
            player.lifes -= 1
            player.health = 100
            player.hide()
        
    if player.lifes == 0 and not(player_expl.alive()):
        running = False

    hits = pygame.sprite.groupcollide(obstacle,bullets,True,True)
    for i in hits:
        score += round(i.radius)
        explo_sound[1].play()
        expl = Explosion(i.rect.center, 'lg')
        effect_sprite.add(expl)
        rock = Rock()
        obstacle.add(rock) 
        
    #畫面顯示   
    screen.blit(background,(0,0))  
    effect_sprite.draw(screen) 
    plane.draw(screen)
    obstacle.draw(screen)
    bullets.draw(screen)
    draw_text(screen, str(score), 22, size[0]/2, 10)
    draw_health(screen, player.health, 5, 10)
    draw_lifes(screen, player.lifes, player_mini, size[0]-100, 10)
    pygame.display.update()

pygame.quit()


