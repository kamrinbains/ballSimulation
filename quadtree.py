# quadtree.py
import pygame
from pygame.math import Vector2

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Boundary is a pygame.Rect
        self.capacity = capacity  # Maximum number of objects before subdivision
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        nw = pygame.Rect(x, y, w / 2, h / 2)
        ne = pygame.Rect(x + w / 2, y, w / 2, h / 2)
        sw = pygame.Rect(x, y + h / 2, w / 2, h / 2)
        se = pygame.Rect(x + w / 2, y + h / 2, w / 2, h / 2)
        self.northwest = Quadtree(nw, self.capacity)
        self.northeast = Quadtree(ne, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.collidepoint(point.position):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northwest.insert(point):
                return True
            elif self.northeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True

        return False

    def query(self, range, found):
        if not self.boundary.colliderect(range):
            return found

        for p in self.points:
            if range.collidepoint(p.position):
                found.append(p)

        if self.divided:
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)

        return found