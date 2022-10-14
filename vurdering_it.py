import pygame
from pygame import gfxdraw
import random, sys, time

def print_slow(str): # skriver ut en og en bokstav i en string
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)
    print('')

print_slow('Velkommen til flappy bird!')
print_slow('Trykk space for å hoppe og pil til høyre for å skyte.')
print_slow('Lykke til...')

pygame.init()
surface = pygame.display.set_mode((700,500))

ORANGE = (255, 125, 25)
GREEN = (50, 255, 25)
BLUE = (50, 140, 255)
RED = (255, 25, 25)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 25)
PURPLE = (105, 0, 105)
GRAY = 	(25,25,25)

running = True
obstacle_width = 100
gravity_speed = 0.13
speed = 1
high_score = 0

def init_variables(): # initialisering av globale variabler
    global death, gravity, counter, score
    death = False
    gravity = 0
    counter = 0
    score = 0

init_variables()

class Obstacle:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move(self, speed):
        self.x_pos -= speed

    def display(self):
        pygame.draw.rect(surface, YELLOW, (self.x_pos, self.y_pos, obstacle_width, 500))
        pygame.draw.rect(surface, YELLOW, (self.x_pos, self.y_pos + 650, obstacle_width, 500))

class Wall(Obstacle):
    def __init__(self, x_pos, y_pos, hp):
        super().__init__(x_pos, y_pos)
        self.hp = hp
        self.x_pos = x_pos + 25
        self.y_pos = y_pos + 500
    
    def lose_hp(self):
        self.hp -= 1

    def show(self):
        pygame.draw.rect(surface, GRAY, (self.x_pos, self.y_pos, obstacle_width/2, 150))

class Character:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius

    def jump(self):
        global gravity 
        gravity = -4

    def fall(self, g):
        self.y_pos += g

    def display(self): # bruker gfxdraw for å tegne sirkel med antialiasing 
        pygame.gfxdraw.aacircle(surface, int(self.x_pos), int(self.y_pos), self.radius, RED)
        pygame.gfxdraw.filled_circle(surface, int(self.x_pos), int(self.y_pos), self.radius, RED)

class Bullet:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius

    def move(self, speed):
        self.x_pos += speed

    def display(self):
        pygame.gfxdraw.aacircle(surface, int(self.x_pos), int(self.y_pos), self.radius, PURPLE)
        pygame.gfxdraw.filled_circle(surface, int(self.x_pos), int(self.y_pos), self.radius, PURPLE)

def init_obj(): # initialisering av objekter
    global obstacles, walls, character, bullets
    random_pos = random.randint(-475, -175)
    obstacles = [Obstacle(700, random_pos)]
    walls = [Wall(700, random_pos, 3)]
    character = Character(100, 100, 30)
    bullets = []

init_obj()

def collision(c, r, y, m, w, h): # c; character, r; rektangel, y; ekstra y_pos for den nedre firkanten, m; margin, w: vidde/2, h; høyde/2
    # x- og y-distanse mellom sirkel og firkant:
    dist_x = abs(c.x_pos - r.x_pos - w)
    dist_y = abs(c.y_pos - r.y_pos - y - h) 

    # om distansen er større enn halve sirkelen og halve rektngelen vil de ikke kollidere:
    if dist_x > w + c.radius - m: 
        return False
    if dist_y > h + c.radius - m:
        return False

    # om distansen er mindre enn halve sirkelen og halve rektngelen vil de kollidere:
    if dist_x <= w:
        return True 
    if dist_y <= h:
        return True

    # bruker pytagoras for å sjekke om sirkelen kolliderer med rektangelhjørnet: 
    dx = dist_x - w
    dy = dist_y - h
    return dx*dx + dy*dy <= (c.radius - m)*(c.radius - m)

while running:
    pygame.time.delay(8)
    font = pygame.font.Font('freesansbold.ttf', 32)

    if not death:
        surface.fill(BLUE)
        counter += 1
        gravity += gravity_speed

        if counter % 256 == 0:
            random_pos = random.randint(-475, -175)
            obstacles.append(Obstacle(700, random_pos))

            if (random.randint(0, 2) == 1):
                walls.append(Wall(700, random_pos, 3))

            if (len(obstacles) > 4): # trenger ikke vise mer enn fire hindringer av gangen
                obstacles.pop(0) 
        
        for i in range(len(bullets)):
            bullets[i].move(speed*2)
            bullets[i].display()

        for i in range(len(obstacles)):
            obstacles[i].display()
            obstacles[i].move(speed)
            if (obstacles[i].x_pos + obstacle_width == character.x_pos): # får poeng ved passering av en hindring 
                score += 1
        
        for i in range(len(walls)):
            walls[i].show()
            walls[i].move(speed)

        character.fall(gravity)
        character.display() 

        def bullet_collision(): # sjekker om skuddet blir truffet
            for i in range(len(bullets)):
                if len(walls) > 0:
                    if collision(bullets[i], walls[0], 0, 3, 25, 75):
                        walls[0].lose_hp()
                        bullets.pop(i)
                        break
            for i in range(len(bullets)):
                for j in range(len(obstacles)):
                    if collision(bullets[i], obstacles[j], 0, 3, 50, 250) or collision(bullets[i], obstacles[j], 650, 3, 50, 250):
                        bullets.pop(i)
                        return
        
        bullet_collision()

        def character_collision(): # sjekker om karakteren blir truffet slik at du dør
            global death
            if len(walls) > 0:
                if collision(character, walls[0], 0, 5, 25, 75):
                    death = True
                    return
            for i in range(len(obstacles)):
                if collision(character, obstacles[i], 0, 5, 50, 250) or collision(character, obstacles[i], 650, 5, 50, 250):
                    death = True
                    return
        
        character_collision()

        if len(walls) > 0:
            if (walls[0].hp == 0):
                walls.pop(0)

        if character.y_pos > 500 - character.radius + 5:
            death = True

        score_text = font.render('Score: ' + str(score), True, BLACK)
        surface.blit(score_text, (10, 10))

    else:
        surface.fill(GREEN)
        text0 = font.render('GAME OVER', True, BLACK)
        if score > high_score:
            text1 = font.render('New highscore: ' + str(score), True, ORANGE)
        else:
            text1 = font.render('Score: ' + str(score) + '    Highscore: ' + str(high_score), True, ORANGE)

        text2 = font.render('Press enter to try again!', True, BLACK)
        surface.blit(text0, (100, 170))
        surface.blit(text1, (100, 210))
        surface.blit(text2, (100, 250))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and character.y_pos > character.radius:
                character.jump()
            if e.key == pygame.K_RIGHT:
                bullets.append(Bullet(character.x_pos, character.y_pos, 8))
            if e.key == pygame.K_RETURN and death:
                death = False
                high_score = score if score > high_score else high_score
                init_variables()
                init_obj()

        if e.type == pygame.QUIT:
            running = False
