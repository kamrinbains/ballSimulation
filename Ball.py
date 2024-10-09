# Ball.py
import pygame
from pygame import Vector2, Color

class Ball:
    def __init__(self, x, y, radius, color):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)  # Initialize velocity
        self.radius = radius
        self.color = color
        self.life = 15

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def draw_ring(self, screen, thickness):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius, thickness)