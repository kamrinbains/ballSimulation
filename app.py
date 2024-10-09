# Red, blue, green, white balls bounce inside circular boundary, each has a certain amount of lives described in Ball Class
# When balls collide, they lose a life; when a ball loses all its lives, it is removed from the game
# Leaderboard functionality is added to the game


import pygame
from pygame.time import Clock
from Ball import Ball
from pygame.math import Vector2
from quadtree import Quadtree
import random
import math

pygame.init()

width, height = 1000, 800
gravity = Vector2(0, 0.1)
init_vel = 7.5
init_bound_radius = 300
outer_x, outer_y = width // 2, height // 2

clock = Clock()
screen = pygame.display.set_mode((width, height))

outer_ball = Ball(outer_x, outer_y, init_bound_radius, (255, 255, 255))
circumference = 2 * 3.14159 * init_bound_radius

counter = 0
pos_x, pos_y = 250, 20

boundary = pygame.Rect(0, 0, width, height)
quadtree = Quadtree(boundary, 4)

def handle_collision(ball1, ball2):
    distance = ball1.position.distance_to(ball2.position)
    if distance < ball1.radius + ball2.radius:
        ball1.life, ball2.life = ball1.life - 1, ball2.life - 1
        direction = (ball2.position - ball1.position).normalize()
        overlap = ball1.radius + ball2.radius - distance
        ball1.position -= direction * (overlap / 2)
        ball2.position += direction * (overlap / 2)
        ball1.velocity, ball2.velocity = ball2.velocity, ball1.velocity

def check_lives():
    for i, ball1 in enumerate(inner_balls):
        if ball1.life <= 0:
            dead_balls.append(dead(ball1))
            inner_balls.remove(ball1)

def add_ball(color):
    angle = random.uniform(0, 2 * math.pi)
    radius = init_bound_radius * math.sqrt(random.uniform(0, 1))
    x = outer_x + radius * math.cos(angle)
    y = outer_y + radius * math.sin(angle)
    new_ball = Ball(x, y, 10, color)
    new_ball.velocity = Vector2(random.uniform(-init_vel, init_vel), random.uniform(-init_vel, init_vel))
    return new_ball

def dead(ball):
    new_ball = Ball(120, 160 + len(dead_balls) * 30, 10, ball.color)
    new_ball.velocity = Vector2(0, 0)
    return new_ball


def draw_lives():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Hits: {red.life}", True, (255, 0, 0))
    screen.blit(text, (250, 50))
    text = font.render(f"Hits: {green.life}", True, (0, 0, 255))
    screen.blit(text, (375, 50))
    text = font.render(f"Hits: {blue.life}", True, (0, 255, 0))
    screen.blit(text, (525, 50))
    text = font.render(f"Hits: {white.life}", True, (255, 255, 255))
    screen.blit(text, (650, 50))
    text = font.render(f"Leaderboard: ", True, (255, 255, 255))
    screen.blit(text, (20, 100))
    for i, ball in enumerate(dead_balls):
        text = font.render(f"{4 - i}", True, ball.color)
        screen.blit(text, (80, 150 + i * 30))

def end():
    dead_balls.append(dead(inner_balls[0]))
    outer_ball.color = inner_balls[0].color
    inner_balls.remove(inner_balls[0])
    outer_ball.draw(screen)


red = add_ball((255, 0, 0))
green = add_ball((0, 0, 255))
blue = add_ball((0, 255, 0))
white = add_ball((255, 255, 255))

red.velocity = Vector2(init_vel, -0.05)
blue.velocity = Vector2(-init_vel, 0.05)  # Initial velocity for the second ball
green.velocity = Vector2(0, -init_vel)  # Initial velocity for the third ball
white.velocity = Vector2(0, init_vel)

inner_balls = [red, blue, green, white]
dead_balls = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for inner_ball in inner_balls:
        inner_ball.velocity += gravity
        inner_ball.position += inner_ball.velocity
        quadtree.insert(inner_ball)

    range = pygame.Rect(outer_ball.position.x - outer_ball.radius, outer_ball.position.y - outer_ball.radius, outer_ball.radius * 2, outer_ball.radius * 2)
    found = quadtree.query(range, [])

    for ball in found:
        distance = outer_ball.position.distance_to(ball.position)
        if distance + ball.radius >= outer_ball.radius:
            direction = (ball.position - outer_ball.position).normalize()
            ball.position = outer_ball.position + direction * (outer_ball.radius - ball.radius)
            ball.velocity = ball.velocity.reflect(direction)  # Reflect the velocity upon collision


    for i, ball1 in enumerate(inner_balls):
        for ball2 in inner_balls[i + 1:]:
            handle_collision(ball1, ball2)
    screen.fill((0, 0, 0))
    for inner_ball in inner_balls:
        inner_ball.draw(screen)
    for dead_ball in dead_balls:
        dead_ball.draw(screen)
    check_lives()
    draw_lives()
    if len(inner_balls) == 1:
        end()
    else:
        outer_ball.draw_ring(screen, 2)
    pygame.display.flip()
    clock.tick(90)

    quadtree = Quadtree(boundary, 4)  # Reset quadtree for the next frame
    print(clock.get_fps())

pygame.quit()