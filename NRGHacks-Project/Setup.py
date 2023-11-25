import pygame 
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600), pygame.RESIZABLE) 

icon2 = pygame.image.load("C:/Users/MajorSanad/Downloads/number-2.png")
#icon3 = pygame.image.load()
#icon4 = pygame.image.load()
#icon5 = pygame.image.load()
#icon6 = pygame.image.load()
#icon7 = pygame.image.load()

pygame.display.set_caption("Math Shooter")

# player code
player = pygame.image.load("C:/Users/MajorSanad/Downloads/spaceship.png")
playerX = 370
playerX_change = 0
playerY = 480
score = 0

 #score font
font = pygame.font.Font(None, 32)
over_font = pygame.font.Font(None, 64)
# game over font
#over_font = pygame.font.Font("C:/Users/MajorSanad/Downloads/analogist.zip", 64)

textX = 10
textY = 10

def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))
def game_over_text():
    text = over_font.render("GAME OVER" , True, (255,255,255))
    screen.blit(text, (200, 250))

# enemy code
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 9
for i in range(num_of_enemies):
    tmp = pygame.image.load("C:/Users/MajorSanad/Downloads/number-2.png")
    tmp = pygame.transform.scale(tmp, (64,64))
    enemyImg.append(tmp)
    enemyX.append(random.randint(64,736))
    enemyY.append(random.randint(64, 128))
    enemyX_change.append(0.8)
    enemyY_change.append(50)

playerX_change = 0
    
enemy1 = pygame.image.load("C:/Users/MajorSanad/Downloads/number-one.png")
enemy1X = random.randint(64, 746)
enemy1Y = random.randint(64,128)
enemy1X_change = .3
enemy1Y_change = 40

# numbered bullets
bullet1 = pygame.image.load("C:/Users/MajorSanad/Downloads/number-1.png")
bullet1X = 0
bullet1Y = playerY
bullet1Y_change = .3
fire_state = "ready"


def show_player(x,y):
    screen.blit(player, (x,y))
def show_enemy1(x, y):
    screen.blit(enemyImg[i], (x, y))

def show_bullet1(x,y):
    global fire_state
    fire_state = "fire"
    screen.blit(bullet1, (x + 16, y + 10))

def isCollision(enemy1X, enemy1Y, bullet1X, bullet1Y):
    distance = math.sqrt((math.pow(enemy1X - bullet1X, 2)) + (math.pow(enemy1Y - bullet1Y,2)))
    if distance < 27:
        return True
    else:
        return False


running = True 
while running:
    screen.fill("black")

    for event in pygame.event.get(): # condition to quit the game
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # move character to the left
                
                playerX_change = -.5
            if event.key == pygame.K_RIGHT:
                # move character to the right
                
                playerX_change = .5
            if event.key == pygame.K_SPACE:
                if fire_state == "ready":
                    bullet1X = playerX
                    show_bullet1(bullet1X, 480)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if(playerX < 0):
        playerX = 0
    elif(playerX > 736):
        playerX = 736

    # moving the enemy
    enemy1X_change += enemy1X_change
    if enemy1X < 64:
        enemy1X = 64
        enemy1X_change = .25
        enemy1Y += enemy1Y_change
    elif enemy1X > 736:
        enemy1X_change = -.25
        enemy1X = 736
        enemy1Y += enemy1Y_change

    # move the bullets
    if fire_state == "fire":
        show_bullet1(bullet1X, bullet1Y)
        bullet1Y -= bullet1Y_change

    # bullet off screen
    if bullet1Y < 0:
        fire_state = "ready"
        bullet1Y = playerY
    
    # collision logic
    collision = isCollision(enemy1X, enemy1Y, bullet1X, bullet1Y)
    if collision:
        bullet1Y = playerY
        fire_state = "ready"

        enemy1X = random.randint(64,746)
        enemy1Y = random.randint(64,128)

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if (enemyX[i] < 0):
            enemyX_change[i] = 0.15
            enemyY[i] += enemyY_change[i]
        elif (enemyX[i] > 736):
            enemyX_change[i] = -.15
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bullet1X, bullet1Y)
        if collision:
            bullet1Y = 480
            fire_state = "ready"
            score += 1
            print(score)

        # respawn enemy
        enemyX[i] = random.randint(64, 735)
        enemyY[i] = random.randint(64, 128)
    if enemyY[i] > 440:
        for j in range(num_of_enemies):
            enemyY[j] = 2000
            game_over_text()
            break
    show_enemy1(enemyX[i], enemyY[i])

   
# render your game here
    show_player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update() # make sure screen refreshes every time
