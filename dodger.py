import pygame, random, sys
from pygame.locals import *


WINDOWWIDTH = 900
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 0, 0)
BACKGROUNDCOLOR = (106, 201, 223)
FPS = 60
BADDIEMINSIZE = 70
BADDIEMAXSIZE = 140
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 20
ADDNEWARBRERATE = 100
PLAYERMOVERATE = 5
Player_Health = 10

def IfTimeHasPassed(t):
    now = pygame.time.get_ticks()
    last_update = 0
    if now - last_update > t:
        last_update = now
        return True


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            #Player_Health -=1
            return True
    return False

def playerHasHitArbre(playerRect,arbres):
    for a in arbres:
        if playerRect.colliderect(a['rect']):
           # Player_Health -=1
            #if pygame.sprite.collide_mask(a['mask'],playerMask):
                     #TODO masks !!!!
            return True
        return False


class Mob(pygame.sprite.Sprite):
    def __init__(self, image, MinSize, MaxSize, MinSpeed, MaxSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.imageSize = random.randint(MinSize, MaxSize)
        self.image = pygame.transform.scale(image, (self.imageSize, self.imageSize))
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WINDOWWIDTH+ self.imageSize,WINDOWWIDTH+ self.imageSize)
        self.rect.y = random.randrange(0,WINDOWHEIGHT/2-self.imageSize)
        self.speedx = random.randrange(-MinSpeed,-MaxSpeed)

    def update(self):
        self.rect.x = self.speedx




def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('roblox.wav')
pygame.mixer.music.load('Fortunate Son.wav')
pygame.mixer.music.set_volume(0.08)

# Set up images.
heli1Image = pygame.image.load('heli-1.png')
heli1_width, heli1_height = heli1Image.get_width(), heli1Image.get_height()
heli1_required_height = 150
playerImage = pygame.transform.scale(heli1Image, (heli1_required_height, round(heli1_required_height*heli1_height/heli1_width))).convert()
playerRect = playerImage.get_rect()
playerMask = pygame.mask.from_surface(playerImage)

baddieImage = pygame.image.load('plane_image.png').convert() #TODO regarder la taille pour garder les proportions
ArbreImage = pygame.image.load("Arbre.png").convert()
ArbreImage_height =  ArbreImage.get_height()


# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0

#importation du sol qui défile
ground = pygame.image.load("Sol.png").convert()
_width, ground_height = ground.get_width(),ground.get_height()
ARBREMINSIZE_height = 60
ARBREMAXSIZE_height = WINDOWHEIGHT/2 - ground_height

"""
class Ground(pygame.sprite.Sprite):
    def __init__(self,position):
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


ground = pygame.sprite.Group()
all_sprites.add(Ground(0))
all_sprites.add(Ground(1))
all_sprites.add(Ground(2))        ##Tout ça, les ckground(012,group) c'est pour faire défiler le sol #TODO peut-être changer façon de faire
"""

while True:
    # Set up the start of the game.
    baddies = []
    arbres = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT/2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    arbreAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
            arbreAddCounter += 1

        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(WINDOWWIDTH+baddieSize,random.randint(0,WINDOWHEIGHT/2-baddieSize), baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        #Add new arbres, if needed :
        if arbreAddCounter == ADDNEWARBRERATE:
            arbreAddCounter = 0
            arbreSize_height = random.randint(ARBREMINSIZE_height,ARBREMAXSIZE_height)
            arbreSize_width = arbreSize_height*93/122           #*93/122 car dimension de l'image de base
            newArbre = {'rect': pygame.Rect(WINDOWWIDTH+round(arbreSize_width),WINDOWHEIGHT-ground_height-arbreSize_height,round(arbreSize_width),round(arbreSize_height)),
                        'speed': -1,
                        'surface': pygame.transform.scale(ArbreImage,(round(arbreSize_width),round(arbreSize_height))),
                        'mask': pygame.mask.from_surface(pygame.transform.scale(ArbreImage,(round(arbreSize_width),round(arbreSize_height)))),
                        }

            arbres.append(newArbre)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies down + arbres left.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(-b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(-5, 0)
            elif slowCheat:
                b['rect'].move_ip(1, 0)
        for a in arbres :
            if not reverseCheat:
                a['rect'].move_ip(a['speed'], 0)
            elif reverseCheat:
                a['rect'].move_ip(-a['speed'], 0)

        # Delete baddies + arbres that have fallen past the left bordure.
        for b in baddies[:]:
            if b['rect'].left < 0:
                baddies.remove(b)
        for a in arbres[:]:
            if a['rect'].left < 0:
                arbres.remove(a)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        #group.update()
        #group.draw(windowSurface)
        #windowSurface.blit(ArbreImage,(450,WINDOWHEIGHT-Arbre_height -ground_height))
        #pygame.display.flip()
        ### image du sol

       # windowSurface.blit(ground, (0,WINDOWHEIGHT-ground_height))
        #windowSurface.blit(ground, (ground_width, WINDOWHEIGHT - ground_height))
        #pygame.display.flip()

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        for a in arbres :
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies) or playerRect.bottom > WINDOWHEIGHT - ground_height or playerHasHitArbre(playerRect, arbres):
            if Player_Health ==0:
                if score > topScore:
                    topScore = score # set new top score
                break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
