# Import and initialize pygame
import pygame
pygame.init()

# Import mixer for audio functions
from pygame import mixer

# Import misc
import random
import math

# Create the screen
screenX = 800
screenY = int(3*(screenX/4))
screenSize = (screenX,screenY)
screen = pygame.display.set_mode(screenSize)

# Global Variables
playerSize = 64
baseOffset = 20
white = (255,255,255)
origin = (0,0)
safeZone = screenY - baseOffset - playerSize - 50
path = '/home/abhay/Desktop/Python/Games/SpaceInvaders/'

# Background Image
background = pygame.image.load(path + 'Images/space.png')

# Background Music, -1 for loop
mixer.music.load(path + 'Sound/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(path + 'Images/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(path + 'Images/ship.png')
playerX = (screenX - playerSize)/2
playerY = screenY - playerSize - baseOffset
playerSpeed = 4
playerXChange = 0

def player(x,y):
    playerLoc = (x,y)
    screen.blit(playerImg, playerLoc)

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def showScore(x,y):
    score = font.render("Score : " + str(scoreValue), True, white)
    scoreLoc = (x,y)
    screen.blit(score, scoreLoc)

# Enemy
numberOfEnemies = 5
enemyImg = []
enemyX = []
enemyY = []
enemySpeed = []
enemyFall = 40
enemyAcceleration = []
jerk = 0.8

# Initialize enemy values
for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load(path + 'Images/enemy.png'))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(30, 150))
    enemySpeed.append(10)
    enemyAcceleration.append(1)

def enemy(x,y,i):
    enemyLoc = (x,y)
    screen.blit(enemyImg[i], enemyLoc)

# Laser
laserImg = pygame.image.load(path + 'Images/bullet.png')
laserX = 0
laserY = 480
laserSpeed = 10
laserFired = False

def laser(x,y):
    laserLoc = (x + 16,y + 10)
    global laserFired
    laserFired = True
    screen.blit(laserImg, laserLoc)

# Collision
def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt(math.pow(enemyX - laserX,2) + math.pow(enemyY - laserY,2))
    return (distance < 27)

# Game Over
over = pygame.font.Font('freesansbold.ttf', 64)

def gameOver():
    for j in range(numberOfEnemies):
        enemyY[j] = 2000

    middleScreen = (200,250)
    overText = over.render("Game Over", True, white)
    screen.blit(overText, middleScreen)

# Game Loop ----------------------------------------------------------------------------------------
running = True
while running:
    # Sample Colors
    midnightBlue = (0,0,36)
    indigo = (75,0,130)
    sea = (32,178,170)

    # Screen Color
    # screen.fill(midnightBlue)

    # Background
    screen.blit(background, origin)

    # Events
    for event in pygame.event.get():
        # Close window
        if event.type == pygame.QUIT:
            running = False

        # Keyboard buttons
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -playerSpeed
            elif event.key == pygame.K_RIGHT:
                playerXChange = playerSpeed
            # Shoot
            elif event.key == pygame.K_SPACE:
                if not laserFired:
                    # Laser sound
                    laserSound = mixer.Sound(path + 'Sound/laser.wav')
                    laserSound.play()

                    laserX = playerX
                    laser(laserX, laserY)

            if(event.key != pygame.K_SPACE):
                prevKey = event.key

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                if event.key == prevKey:
                    playerXChange = 0

    # Move Player
    playerX += playerXChange
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(numberOfEnemies):
        # Game Over
        if enemyY[i] > safeZone:
            gameOver()
            break

        # Move Enemy
        enemyX[i] += enemySpeed[i]
        if enemyX[i] >= 736 or enemyX[i] <= 0:
            enemySpeed[i] *= -1
            enemyY[i] += enemyFall

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:

            # Collision Sound
            explosionSound = mixer.Sound(path + 'Sound/explosion.wav')
            explosionSound.play()

            # Reset laser
            laserY = 480
            laserFired = False

            scoreValue += 1
            # print(score)

            # Respawn enemy
            if( enemySpeed[i] > 0 ):
                enemySpeed[i] += enemyAcceleration[i]
            else:
                enemySpeed[i] -= enemyAcceleration[i]

            enemyAcceleration[i] *= jerk
            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(30, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Laser
    if laserY <= 0:
        laserY = 480
        laserFired = False

    if laserFired == True:
        laser(laserX, laserY)
        laserY -= laserSpeed

    # Player and Score
    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
# -----------------------------------------------------------------------------------------------------------

# Credits
# <div>Icons made by <a href="https://www.flaticon.com/authors/pixel-buddha" title="Pixel Buddha">Pixel Buddha</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <a href='https://www.freepik.com/vectors/background'>Background vector created by freepik - www.freepik.com</a>