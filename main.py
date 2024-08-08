import pygame
from pygame import mixer
import random
import math

# Initialize pygame
pygame.init()

# Creating the clock
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('Assets/background(1).png')

# background sound
mixer.music.load('Assets/background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Assets/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Assets/001-spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Assets/enemy1.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

# Bullet
bulletImg = pygame.image.load('Assets/001-missile.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = 'ready'

# Score

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 16)
over_font = pygame.font.Font('freesansbold.ttf', 64)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render(f'Score: {score_val}', True, 'green')
    screen.blit(score, (x, y))


def Player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fired(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over_text():
    over_text = over_font.render('GAME OVER', True, 'red')
    screen.blit(over_text, (235, 250))


text = font2.render('press S to stop the music', True, 'white')

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(text, (595, 585))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_sound = mixer.Sound('Assets/laser.wav')
                bullet_sound.play()
                bulletX = playerX
                bullet_fired(bulletX, bulletY)
            if event.key == pygame.K_s:
                mixer.music.stop()
            if event.key == pygame.K_z:
                mixer.music.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Check for boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('Assets/explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_val += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        Enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= -50:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fired':
        bullet_fired(bulletX, bulletY)
        bulletY -= bulletY_change

    Player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

    clock.tick(60)
