import pygame
import random

pygame.init()
surface = pygame.display.set_mode((700,500))

def init_variables():
    global ORANGE, GREEN, BLUE, RED, BLACK, YELLOW
    ORANGE = (255, 120, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    global obstacle_width, gravity_speed, gravity, running, counter, speed
    obstacle_width = 75
    gravity_speed = 0.075
    gravity = 0
    running = True
    counter = 0
    speed = 1

init_variables()

class Obstacle:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move(self, speed):
        self.x_pos -= speed

    def display(self):
        pygame.draw.rect(surface, YELLOW, (self.x_pos, self.y_pos, obstacle_width, 500))
        pygame.draw.rect(surface, YELLOW, (self.x_pos, self.y_pos + 600, obstacle_width, 500))

class Character:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius

    def jump(self):
        global gravity
        gravity = -2.5
        self.y_pos -= 50

    def fall(self, g):
        self.y_pos += g

    def display(self):
        pygame.draw.circle(surface, RED, (self.x_pos, self.y_pos), self.radius)

def init_lists():
    global obstacles, character
    obstacles = [Obstacle(700, random.randint(-450, -150))]
    character = Character(100, 100, 30, 0)

init_lists()

while running:
    pygame.time.delay(10)

    if not death:
        surface.fill(BLUE)
        counter += 1
        gravity += gravity_speed

        if counter % 300 == 0:
                obstacles.append(Obstacle(700, random.randint(-450, -150)))
                if (len(obstacles) > 3):
                    obstacles.pop(0)
        
        for i in range(len(obstacles)):
            obstacles[i].display()
            obstacles[i].move(speed)

        character.fall(gravity)
        character.display()

        for i in range(len(obstacles)):
            hit_x = character.x_pos > obstacles[i].x_pos - character.radius and character.x_pos < obstacles[i].x_pos + character.radius
            hit_y = character.y_pos > obstacles[i].y_pos - character.radius + 650 or character.y_pos < obstacles[i].y_pos + character.radius + 500
            if hit_x and hit_y:
                death = True

        if character.y_pos > 500 - character.radius:
            death = True

    else:
        surface.fill(GREEN)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game over. Score: '+len(obstacles)+'\nPress enter to play again', True, BLACK)
        surface.blit(text, (100, 200))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                character.jump()
            if e.key == pygame.K_RETURN:
                death = False
                init_variables()
                init_lists()
        if e.type == pygame.QUIT:
            running = False
