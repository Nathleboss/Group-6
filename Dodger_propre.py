import pygame, sys, random
from pygame.locals import *



BACKGROUNDCOLOR = (106, 200, 223)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
FPS = 100
PLAYERMOVERATE = 5



ADDNEWARBRERATE = 200

# TODO A faire autrement !! on peut sûrement faire avec un colliderect, mais ça nous dit pas pourquoi ça marche pas avec ground.height
hauteur_sol = pygame.image.load("Sol.png").get_height()

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
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def reset_groups():
    all_sprites.empty(); mobs.empty(); bullets.empty(); trees.empty(); coins.empty()
    all_sprites.add(player)
    all_sprites.add(Ground(0))
    all_sprites.add(Ground(1))
    all_sprites.add(Ground(2))

    for i in range(6):  # Nombre de mobs visibles à l'écran en même temps
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    for i in range(1):  # Pareil pour les coins
        c = Coin()
        all_sprites.add(c)
        coins.add(c)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.frames[0]               #pygame.image.load("heli-1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.speed = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.lives = 3
        self.touched = False

    def load_images(self):              #load_images() et animate() pour créer animation des hélices de l'hélicoptère
        self.frame0 = pygame.image.load("heli-1.png")
        self.frame1 = pygame.image.load("heli-2.png")
        self.frame2 = pygame.image.load("heli-3.png")
        self.frame3 = pygame.image.load("heli-4.png")
        self.frames = [self.frame0, self.frame1, self.frame2, self.frame3]

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50 :           #en millisecondes
            self.last_update = now
            self.current_frame = (self.current_frame+1) % len(self.frames)      #1%4=1; 2%4=2; 3%4=3; 4%4=0, 5%4=1 etc...
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.animate()
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
        if self.rect.x < 0:         #ne pas sortir de l'écran
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx + 60, self.rect.bottom - 5)
        all_sprites.add(bullet)
        bullets.add(bullet)
        blaster.set_volume(0.06)
        blaster.play()

    def isInvincible(self):
        pass#if self.touched = True

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
        #if score > 5000:
            #pass

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
        # kill it if touches no enemy and go too far
        if self.rect.right > WINDOWWIDTH:
            self.kill()

class Coin(pygame.sprite.Sprite):               #pourquoi pas faire une superclass qui contient les pièces et les bonus ?
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Coin.png")      #mettre une animation avec plusieurs modèles de coins qui tourne comme hélico ?
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH
        self.rect.y = random.randrange(0,WINDOWHEIGHT-100)
        self.speedx = -3
        self.speedy = random.randrange(-3,3)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #déplacement "sinusoïdale":
        if self.rect.bottom > WINDOWHEIGHT -100 :
            self.speedy=  -3
        if self.rect.top < 50 :
            self.speedy = 3
        if self.rect.left < -self.rect.width or abs(self.rect.top) > WINDOWHEIGHT :       #si la pièce sort sur la gauche ou en haut/bas
            self.rect.x = WINDOWWIDTH
            self.rect.y = random.randrange(0, WINDOWHEIGHT - 100)
            self.speedx = -3
            self.speedy = random.randrange(-3, 3)

class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Arbre.png")
        self.imageSize = random.randint(60, int(WINDOWHEIGHT/2 - hauteur_sol))
        self.image = pygame.transform.scale(self.image, (self.imageSize, self.imageSize))
        self.rect = self.image.get_rect()
        self.rect.x = WINDOWWIDTH+round(self.rect.width)
        self.rect.y = WINDOWHEIGHT-self.rect.height- hauteur_sol
        self.speedx = -1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx

class Ground(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sol.png")
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.x = self.rect.width * self.position
        self.rect.y = WINDOWHEIGHT - self.rect.height
        self.speedx = -1
        #self.height = self.rect.height


    def update(self):
        self.rect.x += self.speedx

        if self.rect.left <= -self.rect.width:
            self.rect.x = WINDOWWIDTH
            self.rect.y = WINDOWHEIGHT - self.rect.height
            self.speedx = -1

    #def get_height(self):
    #    self.hauteur = self.rect.height
    #    return self.hauteur



# initialize pygame and create window + police d'écriture (fonts)
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("LA GUERRE")
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 48)
#Sons
gameOverSound = pygame.mixer.Sound('MissionFailed.wav')
lostLifeSound = pygame.mixer.Sound('Mayday Sound.wav')
coinSound = pygame.mixer.Sound('smw_coin.wav')
pygame.mixer.music.load('Fortunate Son.wav')
blaster = pygame.mixer.Sound('Blaster.wav')

pygame.mixer.music.set_volume(0.08)

# Show the "Start" screen.
Ecran_de_titre = pygame.image.load('Ecran_de_titre.png')
windowSurface.blit(Ecran_de_titre, (0, 0))
#drawText('La guerre', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3),RED)
#drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50,RED)
pygame.display.update()
waitForPlayerToPressKey()

coins_number = 0
topScore = 0

#Création des groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
coins = pygame.sprite.Group()
ground = pygame.sprite.Group()
trees = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

"""
all_sprites.add(Ground(0))
all_sprites.add(Ground(1))
all_sprites.add(Ground(2))

for i in range(6):  # Nombre de mobs visibles à l'écran en même temps
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
for i in range(1):   #Pareil pour les coins
    c = Coin()
    all_sprites.add(c)
    coins.add(c)



#for i in range(10):  # Nombre de mobs visibles à l'écran en même temps
 #   t = Tree()
  #  all_sprites.add(t)
  #  trees.add(t)
"""
                        ###pas besoin de la partie en commentaire vert, présent dans la fonction reset_groups()
# Game loop
running = True
while True:
    score = 0
    coins_number = 0
    pygame.mixer.music.play(-1, 0.0)
    reset_groups()
    arbreAddCounter = 0

    while running:
        score += 1
        # Clock FPS
        mainClock.tick(FPS)
        last_update = 0
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
                    terminate()       #running = False ; pygame.quit()

        arbreAddCounter += 1

        if arbreAddCounter == ADDNEWARBRERATE:
            arbreAddCounter = 0
            t = Tree()
            all_sprites.add(t)
            trees.add(t)

        # Update
        all_sprites.update()

        # collision bullet-mob
        hits_bullet = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_mask)            #True,True ça kill le mob ET la bullet, cette fonction retourne une liste
        for hit in hits_bullet :        #on recrée un mob à chaque fois qu'on en kill un
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        # collisions player-mob
        hits_mob = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
        for hit in hits_mob:                #TODO voir si on change la méthode d'apparition des mob, comme pour les arbres
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        # collisions player-coin + counter coins
        hits_coin = pygame.sprite.spritecollide(player, coins, True, pygame.sprite.collide_mask)
        if hits_coin:
            coinSound.play()
            score += 100                    #est-ce que choper une coin ça donne +100 score ?
        for hit in hits_coin:
            c = Coin()
            all_sprites.add(c)
            coins.add(c)
            coins_number += 1                # si on arrive à genre 10 coins, on a accès au gun ?
        #collisions player-tree
        hits_tree = pygame.sprite.spritecollide(player, trees, True, pygame.sprite.collide_mask)
        #if bad collision for player, then lose a lifepoint
        if hits_mob or hits_tree or player.rect.bottom >= WINDOWHEIGHT-hauteur_sol:
            if hits_mob or hits_tree:
                lostLifeSound.set_volume(0.15)
                lostLifeSound.play()
                for hit in hits_mob:
                    player.lives -= 1               #code invincibility for x seconds after losing a lifepoint
                for hit in hits_tree:
                    player.lives -= 1
            if player.lives < 0 or player.rect.bottom >= WINDOWHEIGHT-hauteur_sol:
                player = Player()           #permet de bien reset le player pour nouvelle game
                if score > topScore:
                    topScore = score
                break

        # Draw / render
        windowSurface.fill(BACKGROUNDCOLOR)
        all_sprites.draw(windowSurface)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0, RED)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40, RED)
        drawText('#Coins: %s' % (coins_number), font, windowSurface, 10, 80, YELLOW)
        drawText('Lives: %s' % (player.lives), font, windowSurface, 10, 120, RED)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    #Écran de game-over
    pygame.mixer.music.stop()
    gameOverSound.set_volume(0.06)
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3), RED)
    drawText('Appuie sur une touche pour rejouer', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50, RED)
    pygame.display.update()
    reset_groups()
    waitForPlayerToPressKey()
    gameOverSound.stop()

#pygame.quit()