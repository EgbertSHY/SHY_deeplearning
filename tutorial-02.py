import pygame

running=True
size=width,height=500,750
backgorund=(0,0,0)
background1=(255,255,255)
flag=True
#FPS=60

pygame.init()
screen=pygame.display.set_mode(size)
pygame.display.set_caption("星際大戰")
clock=pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill((0,255,0))    
        self.rect = self.image.get_rect()
        self.rect.x=230
        self.rect.y=710
    #def update(self):

#第一步:建立PLAYER
player=Player()
#第二步:建立群組
group1=pygame.sprite.Group()
#第三步:將物件放入群組
group1.add(player)

while running:
    #clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    #group1.update()
    screen.fill(backgorund)
    #第四步:將群組物件顯示在畫面
    group1.draw(screen)
    pygame.display.update()

pygame.quit()
