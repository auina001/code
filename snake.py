import pygame 
import random
from colors import *

pygame.init()
surface = pygame.display.set_mode((600, 360))

running = True
high_score = 0

def init_variables():
    global counter, score, direction, x_vel, y_vel, death
    counter = 0
    score = 0
    direction = 1
    x_vel = 30
    y_vel = 0
    death = False

init_variables()

class Rectangle:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = 24

    def display(self):
        m = (30 - self.size)/2 # margin
        pygame.draw.rect(surface, ORANGE, (self.x_pos + m, self.y_pos + m, self.size, self.size))

class Target:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = 18
    
    def display(self):
        m = (30 - self.size)/2 # margin
        pygame.draw.rect(surface, BLUE, (self.x_pos + m, self.y_pos + m, self.size, self.size))

def target_x_pos():
    x = random.randint(0, 19) * 30
    while any(e.x_pos == x for e in rectangles):
        x = random.randint(0, 19) * 30
    return x

def target_y_pos():
    y = random.randint(0, 11) * 30
    while any(e.y_pos == y for e in rectangles):
        y = random.randint(0, 11) * 30
    return y

def init_obj(): # initialisering av objekter
    global rectangles, target
    rectangles = [Rectangle(120, 60), Rectangle(90, 60), Rectangle(60, 60)]
    target = Target(target_x_pos(), target_y_pos())

init_obj()

while running:
    pygame.time.delay(8)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    if not death:
        surface.fill(RED)
        counter += 1
        if counter % 24 == 0:
            if direction == 1:
                x_vel = 30; y_vel = 0
            elif direction == 2:
                x_vel = -30; y_vel = 0
            elif direction == 3:
                y_vel = 30; x_vel = 0
            elif direction == 4:
                y_vel = -30; x_vel = 0

            for i in range(len(rectangles) - 1, 0, -1):
                append_x = rectangles[len(rectangles) - 1].x_pos
                append_y = rectangles[len(rectangles) - 1].y_pos
                rectangles[i].x_pos = rectangles[i-1].x_pos
                rectangles[i].y_pos = rectangles[i-1].y_pos
            
            rectangles[0].x_pos += x_vel
            rectangles[0].y_pos += y_vel

            if rectangles[0].x_pos == 600:
                rectangles[0].x_pos = 0
            elif rectangles[0].x_pos == -30:
                rectangles[0].x_pos = 570
            elif rectangles[0].y_pos == 360:
                rectangles[0].y_pos = 0
            elif rectangles[0].y_pos == -30:
                rectangles[0].y_pos = 330

            if rectangles[0].x_pos == target.x_pos and rectangles[0].y_pos == target.y_pos:
                score += 1
                rectangles.append(Rectangle(append_x, append_y))
                target = Target(target_x_pos(), target_y_pos())
            
            for i in range(len(rectangles) - 1, 0, -1):
                if rectangles[0].x_pos == rectangles[i].x_pos and rectangles[0].y_pos == rectangles[i].y_pos:
                    death = True
        
        target.display()

        for i in range(len(rectangles)):
            rectangles[i].display()

    else:
        surface.fill(PURPLE)
        text0 = font.render('GAME OVER', True, BLACK)
        if score > high_score:
            text1 = font.render('New highscore: ' + str(score), True, ORANGE)
        else:
            text1 = font.render('Score: ' + str(score) + '    Highscore: ' + str(high_score), True, ORANGE)

        text2 = font.render('Press enter to try again!', True, BLACK)
        surface.blit(text0, (80, 120))
        surface.blit(text1, (80, 160))
        surface.blit(text2, (80, 200))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN and death:
                death = False
                init_variables()
                init_obj()
            if e.key == pygame.K_RIGHT and x_vel != -30:
                direction = 1
            elif e.key == pygame.K_LEFT and x_vel != 30:
                direction = 2
            elif e.key == pygame.K_DOWN and y_vel != -30:
                direction = 3
            elif e.key == pygame.K_UP and y_vel != 30:
                direction = 4

        if e.type == pygame.QUIT:
            running = False
