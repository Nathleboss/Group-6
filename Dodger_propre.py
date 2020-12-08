import pygame, sys, random
from pygame.locals import *

BACKGROUNDCOLOR = (106, 200, 223)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
FPS = 100
PLAYERMOVERATE = 5
ADDNEWTREERATE = 350

saveScore = open("saveScore.txt", 'r')
try:
    topScore = int(saveScore.read())
except:
    topScore = 0


def terminate():
    pygame.quit()
    sys.exit()


def drawText(text, font, surface, x, y, TEXTCOLOR):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def reset_groups():
    all_sprites.empty();
    mobs.empty();
    bullets.empty();
    trees.empty();
    coins.empty();
    malus.empty()
    all_sprites.add(player)
    all_sprites.add(Ground(0))
    all_sprites.add(Ground(1))
    all_sprites.add(Ground(2))

    for i in range(6):  # numbers of mobs visible at the same time in the screen
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    for i in range(1):  # same for coins
        c = Coin()
        all_sprites.add(c)
        coins.add(c)
    for i in range(1):  # same for malus
        m = Malus()
        all_sprites.add(m)
        malus.add(m)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.lives = 3
        self.max_lives = self.lives  # constant value = 3, necessary for the health bar

    def load_images(self):  # load_images() et animate() to create animation of the helicopter's propellers
        self.frame0 = pygame.image.load("heli-1.png").convert_alpha()
        self.frame1 = pygame.image.load("heli-2.png").convert_alpha()
        self.frame2 = pygame.image.load("heli-3.png").convert_alpha()
        self.frame3 = pygame.image.load("heli-4.png").convert_alpha()
        self.frames = [self.frame0, self.frame1, self.frame2, self.frame3]

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:  # in milliseconds
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # 1%4=1; 2%4=2; 3%4=3; 4%4=0, 5%4=1 etc...
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.animate()
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if not confused:
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
            if keystate[pygame.K_UP]:
                self.speedy = -5
            if keystate[pygame.K_DOWN]:
                self.speedy = 4  # because of gravity, to get 1 + 4 = 5
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        else:
            if keystate[pygame.K_LEFT]:
                self.speedx = 5
            if keystate[pygame.K_RIGHT]:
                self.speedx = -5
            if keystate[pygame.K_UP]:
                self.speedy = 5
            if keystate[pygame.K_DOWN]:
                self.speedy = -5
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.x < 0:  # can't get out of the screen
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        # gravity
        self.rect.y += 1

    def shoot(self):
        bullet = Bullet(self.rect.centerx + 60, self.rect.bottom - 5)
        all_sprites.add(bullet)
        bullets.add(bullet)
        blaster.set_volume(0.06)
        blaster.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if score < 2500:
            self.image = pygame.image.load("plane_image.png")
            self.imageSize = random.randint(100, 300)
            self.image = pygame.transform.scale(self.image, (self.imageSize, self.imageSize))
            self.rect = self.image.get_rect()
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(-25, WINDOWHEIGHT / 2 - self.rect.height)
            self.speedx = random.randrange(-5, -1)
        else:
            self.image = pygame.image.load("OVNI.png")
            self.imageSize = random.randint(100, 300)
            self.image = pygame.transform.scale(pygame.image.load("OVNI.png"),
                                                (int(self.imageSize / 1.5), int(self.imageSize / 3)))
            self.rect = self.image.get_rect()
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(-5, WINDOWHEIGHT / 2 - self.rect.height)
            self.speedx = random.randrange(-6, -2)

    def update(self):
        if self.rect.left < -self.rect.width:  # if a mob gets past the left border of the screen, we teleport it to the right randomly
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(-25, WINDOWHEIGHT / 2 - self.rect.height)
            self.speedx = random.randint(-5, -1)
            if score > 2500:  # level 2, we can improve by adding more levels
                self.image = pygame.transform.scale(pygame.image.load("OVNI.png"),
                                                    (int(self.imageSize / 1.5), int(self.imageSize / 3)))
                self.rect = self.image.get_rect()
                self.rect.x = WINDOWWIDTH
                self.rect.y = random.randrange(0, WINDOWHEIGHT / 2 - self.rect.height)
                self.speedx = random.randint(-6, -2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += self.speedx


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
        # kill it if touches no enemy and go too far
        if self.rect.right > WINDOWWIDTH:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Coin.png")  # we could make animations to make the coin rotate
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH
        self.rect.y = random.randrange(0, WINDOWHEIGHT - 100)
        self.speedx = -3
        self.speedy = random.randrange(-3, 3)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # "sinusoidal" movement:
        if self.rect.bottom > WINDOWHEIGHT - 100:
            self.speedy = -3
        if self.rect.top < 50:
            self.speedy = 3
        if self.rect.left < -self.rect.width:  # if the coin gets past the left border of the screen
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(0, WINDOWHEIGHT - 100)
            self.speedx = -3
            self.speedy = random.randrange(-3, 3)


class Malus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.frames[0]
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH
        self.rect.y = random.randrange(0, WINDOWHEIGHT - 100)
        self.speedx = -3
        self.speedy = random.randrange(-3, 3)
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = 0

    def load_images(self):
        self.frame0 = pygame.transform.scale(pygame.image.load("malus_confusion.png").convert_alpha(), (40, 40))
        self.frame1 = pygame.transform.scale(pygame.image.load("malus_confusion2.png").convert_alpha(), (40, 40))
        self.frame2 = pygame.transform.scale(pygame.image.load("malus_confusion3.png").convert_alpha(), (40, 40))
        self.frame3 = pygame.transform.scale(pygame.image.load("malus_confusion4.png").convert_alpha(), (40, 40))
        self.frames = [self.frame0, self.frame1, self.frame2, self.frame3]

    def animate(self):  # rotation
        now = pygame.time.get_ticks()
        if now - self.last_update > 250:  # in milliseconds
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # 1%4=1; 2%4=2; 3%4=3; 4%4=0, 5%4=1 etc...
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pygame.transform.scale(self.image, (40, 40))
        self.animate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # "sinusoidal" movement:
        if self.rect.bottom > WINDOWHEIGHT - 100:
            self.speedy = -3
        if self.rect.top < 10:
            self.speedy = 3
        if self.rect.left < -self.rect.width:  # si le malus sort sur la gauche
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(0, WINDOWHEIGHT - 100)
            self.speedx = -3
            self.speedy = random.randrange(-3, 3)


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Arbre.png")
        self.imageSize = random.randint(60, int(WINDOWHEIGHT / 2 - ground_height))
        self.image = pygame.transform.scale(self.image, (self.imageSize, self.imageSize))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH + round(self.rect.width)
        self.rect.y = WINDOWHEIGHT - self.rect.height - ground_height
        self.speedx = -1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx


class Ground(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sol.png")
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.x = self.rect.width * self.position
        self.rect.y = WINDOWHEIGHT - self.rect.height
        self.speedx = -1

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left <= -self.rect.width:
            self.rect.x = WINDOWWIDTH
            self.rect.y = WINDOWHEIGHT - self.rect.height
            self.speedx = -1


# initialize pygame and create window + fonts
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("LA GUERRE")
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 48)

# Sounds
gameOverSound = pygame.mixer.Sound('MissionFailed.wav')
lostLifeSound = pygame.mixer.Sound('Mayday Sound.wav')
coinSound = pygame.mixer.Sound('smw_coin.wav')
pygame.mixer.music.load('Fortunate Son.wav')
blaster = pygame.mixer.Sound('Blaster.wav')
pygame.mixer.music.set_volume(0.08)

# Show the "Start" screen.
Start_screen = pygame.image.load('Ecran_de_titre.png')
windowSurface.blit(Start_screen, (0, 0))
pygame.display.update()
waitForPlayerToPressKey()

coins_number = 0

# Creation of groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
coins = pygame.sprite.Group()
malus = pygame.sprite.Group()
ground = pygame.sprite.Group()
trees = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

ground_height = pygame.image.load(
    "Sol.png").get_height()  # TODO, not optimal and coherent with the rest of the code, but it works.
confused = False

# Game loop
while True:
    score = 0
    coins_number = 0
    pygame.mixer.music.play(-1, 0.0)
    reset_groups()
    treeAddCounter = 0
    running = True
    confused = False

    while running:
        score += 1
        # Clock FPS
        mainClock.tick(FPS)
        now = pygame.time.get_ticks()
        # Process input (event)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_ESCAPE:
                    terminate()

        treeAddCounter += 1

        if treeAddCounter == ADDNEWTREERATE:
            treeAddCounter = 0
            t = Tree()
            all_sprites.add(t)
            trees.add(t)

        # Update
        all_sprites.update()

        # collision bullet-mob
        hits_bullet = pygame.sprite.groupcollide(mobs, bullets, True, True,
                                                 pygame.sprite.collide_mask)  # putting True kills the mob AND the bullet, returns a list
        for hit in hits_bullet:  # each time we kill a mob, we recreate one
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        # collisions player-mob
        hits_mob = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
        for hit in hits_mob:  # alternative way of apparition
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        # collisions player-coin + counter coins
        hits_coin = pygame.sprite.spritecollide(player, coins, True, pygame.sprite.collide_mask)
        if hits_coin:
            coinSound.play()
            score += 100
        for hit in hits_coin:
            c = Coin()
            all_sprites.add(c)
            coins.add(c)
            coins_number += 1

        # collisions player-malus
        hits_malus = pygame.sprite.spritecollide(player, malus, True, pygame.sprite.collide_mask)
        if hits_malus:
            confused = True
            malus_hit_time = pygame.time.get_ticks()

        if confused:
            if now - malus_hit_time > 1000:  # in milliseconds
                confused = False

        for hit in hits_malus:
            m = Malus()
            all_sprites.add(m)
            malus.add(m)

        # collisions player-tree
        hits_tree = pygame.sprite.spritecollide(player, trees, True, pygame.sprite.collide_mask)
        # if bad collision for player, then lose a lifepoint
        if hits_mob or hits_tree or player.rect.bottom >= WINDOWHEIGHT - ground_height + 10:
            if hits_mob or hits_tree:
                lostLifeSound.set_volume(0.15)
                lostLifeSound.play()
                for hit in hits_mob:
                    player.lives -= 1  # TODO code invincibility for x seconds after losing a lifepoint, report
                for hit in hits_tree:
                    player.lives -= 1
            if player.lives <= 0 or player.rect.bottom >= WINDOWHEIGHT - ground_height:
                player = Player()  # necessary to reset appropriately
                if score > topScore:
                    topScore = score
                    with open("saveScore.txt", 'w') as file:
                        file.write(str(topScore))
                break

        # Draw / render
        if confused:
            windowSurface.fill((random.randint(0, 255), 0, 0))
        if not confused:
            if score < 2500:
                windowSurface.fill(BACKGROUNDCOLOR)
            else:
                windowSurface.blit(pygame.image.load("space_background.png"), (0, 0))
        all_sprites.draw(windowSurface)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0, RED)
        drawText('(+ %s)' % (coins_number * 100), font, windowSurface, 200, 0, YELLOW)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40, RED)
        drawText('#Coins: %s' % (coins_number), font, windowSurface, 10, 80, YELLOW)
        pygame.draw.rect(windowSurface, RED, (player.rect.x + 30, player.rect.y - 15, 150, 10))
        pygame.draw.rect(windowSurface, GREEN,
                         (player.rect.x + 30, player.rect.y - 15, player.lives * 150 / player.max_lives, 10))
        # *after* drawing everything, flip the display
        pygame.display.flip()

    # GameOver screen
    pygame.mixer.music.stop()
    gameOverSound.set_volume(0.06)
    gameOverSound.play()
    pygame.display.flip()
    if score < 2500:
        windowSurface.blit(pygame.image.load("Ecran_de_fin_jour.png"), (0, 0))
    else:
        windowSurface.blit(pygame.image.load("Ecran_de_fin_nuit.png"), (0, 0))
    drawText('Score: %s' % (score), font, windowSurface, (WINDOWWIDTH / 3) + 60, (WINDOWHEIGHT / 3) + 30, RED)
    drawText('Top Score: %s' % (topScore), font, windowSurface, (WINDOWWIDTH / 3) + 30, (WINDOWHEIGHT / 3) + 80, RED)
    pygame.display.update()
    reset_groups()
    waitForPlayerToPressKey()
    gameOverSound.stop()
