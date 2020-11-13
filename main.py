import pygame
import random
import math
from pygame import mixer

# it initialize pygame
pygame.init()
# screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('3969.jpg')
# backgroung music
# mixer.music.load(file name)
# mixer.music.play(-1)

# icon and title
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('spaceship1.png')
playerX = 370
playerY = 480
playerXchange = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
noofenemy = 6
for i in range(noofenemy):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(0.4)
    enemyYchange.append(30)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = 1
bulletstate = "ready"

# score
scoreval = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# gameover
overfont = pygame.font.Font('freesansbold.ttf', 64)
out = "notout"


def scoreshow(x, y):
    score = font.render("SCORE : " + str(scoreval), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameovertext():
    global out
    out = "out"
    overtext = overfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))  # means to draw image on screen


def Enemy(x, y, i):
    screen.blit(enemyimg[i], (x + 16, y + 10))  # means to draw image on screen


def fireBullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg, (x, y))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 25:
        return True
    else:
        return False


# for running game
run = True
while run:
    screen.fill((0, 0, 0))  # RGB
    screen.blit(background, (0, 0))  # background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -0.6

            if event.key == pygame.K_RIGHT:
                playerXchange = 0.6
            if event.key == pygame.K_SPACE:
                if bulletstate == "ready":
                    bulletsound = mixer.Sound('laser.wav')
                    bulletsound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0

    playerX += playerXchange
    if playerX <= 0:
        playerX = 0
    if playerX >= 738:
        playerX = 738
    # enemy move
    for i in range(noofenemy):
        # game over
        if enemyY[i] > 437 or enemyX[i] == playerX:
            for i in range(noofenemy):
                enemyY[i] = 2000
            gameovertext()
            break
        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 0.3
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 738:
            enemyXchange[i] = -0.3
            enemyY[i] += enemyYchange[i]
        # collision case
        col = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            explosionsound = mixer.Sound('explosion.wav')
            explosionsound.play()
            bulletY = 480
            bulletstate = "ready"
            scoreval += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        Enemy(enemyX[i], enemyY[i], i)
    # bullet move
    if bulletY <= 0:
        bulletY = 480
        bulletstate = "ready"
    if bulletstate == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYchange

    player(playerX, playerY)
    scoreshow(textX, textY)
    pygame.display.update()
