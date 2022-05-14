import sys, pygame
pygame.init()

size = width, height = 500, 750
background = 0, 0, 0
FPS=60

screen = pygame.display.set_mode(size,pygame.RESIZABLE)
pygame.display.set_caption("星際大戰")

#小飛機
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill((0,255,0))    
        self.rect = self.image.get_rect()
        self.rect.centerx=(width-40)/2
        self.rect.centery=(height-40)/2
        self.speed=8
    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.right > 500:
            self.rect.right=500
        if self.rect.left < 0:
            self.rect.left=0
        if self.rect.top < 0:
            self.rect.top=0
        if self.rect.bottom >750:
            self.rect.bottom=750

    
clock=pygame.time.Clock()
#第一步:建立PLAYER
player=Player()
#第二步:建立群組
group1=pygame.sprite.Group()
#第三步:將物件放入群組
group1.add(player)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                sys.exit()
    #group1.update()
    screen.fill(background)
    #第四步:將群組物件顯示在畫面
    group1.draw(screen)
    group1.update()
    pygame.display.update()


