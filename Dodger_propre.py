import pygame, sys, random
from pygame.locals import *

BACKGROUNDCOLOR = (106, 201, 223)
TEXTCOLOR = (255, 0, 0)
BLACK = (0, 0, 0)
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
FPS = 60
PLAYERMOVERATE = 5

lives = 3


def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("heli-1.png")  # pygame.Surface((50,50))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.speed = 0
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.x < 0:
            self.rect.left = 0


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane_image.png")
        self.imageSize = random.randint(100, 300)
        self.image = pygame.transform.scale(self.image, (self.imageSize, self.imageSize))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH
        self.rect.y = random.randrange(-20, WINDOWHEIGHT / 2 - self.rect.height)
        # self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-5, -1)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < -self.rect.width:  # si l'ennemi dépasse la fenêtre à gauche, on le remet à un endroit random à droite
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(-20, WINDOWHEIGHT / 2 - self.rect.height)
            self.speedx = random.randint(-5, -1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # kill it if touches no ennemy and go too far
        if self.rect.right > WINDOWWIDTH:
            self.kill()


# initialize pygame and create window + police d'écriture (fonts)
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(("MY GAME"))
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 48)
#Sons
gameOverSound = pygame.mixer.Sound('roblox.wav')
pygame.mixer.music.load('Fortunate Son.wav')
pygame.mixer.music.set_volume(0.08)

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):  # Nombre de mobs visibles à l'écran en même temps
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while True:
    score = 0
    pygame.mixer.music.play(-1, 0.0)

    while running:
        score += 1
        # Clock FPS
        mainClock.tick(FPS)
        # Process input (event)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # collision bullet-mob
        hits_bullet = pygame.sprite.groupcollide(mobs,bullets,True,True)
        for hit in hits_bullet :        #on recrée un mob à chaque fois qu'on en kill un
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        # collision player-mob
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_mask)
        if hits:
            lives -= 1
            if lives <= 0:
                running = False
        # Draw / render
        windowSurface.fill(BACKGROUNDCOLOR)
        all_sprites.draw(windowSurface)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    #Écran de game-over
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()

#pygame.quit()