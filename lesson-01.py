import os,pygame
pygame.init()

#相關變數
running=True
FPS=60

#設定視窗及背景資訊
background = pygame.image.load(os.path.join('image','space.jpeg'))
size = background.get_size()
types=pygame.RESIZABLE
screen = pygame.display.set_mode(size,types)
pygame.display.set_caption("星際大戰")
pygame.display.set_icon(pygame.image.load(os.path.join('image','icon.png')).convert())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                running=False
    screen.blit(background,(0,0))
    pygame.display.flip()

pygame.quit()


