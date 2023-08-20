import pyxel
from enum import Enum
from typing import Self
from vector import Vector2D

class CollisionType(Enum):
    OUTSIDE = 0
    INSIDE = 1
    INTERSECT = 2

class Circle:
    center : Vector2D
    radius : float
    color = pyxel.COLOR_LIME

    def __init__(self, pos : Vector2D, radius : float) -> None:
        self.center = pos
        self.radius = radius

    def draw_circle(self):
        pyxel.circb(self.center.x, self.center.y, self.radius, self.color)

    def set_pos(self, pos : Vector2D):
        self.center = pos

    def set_radius(self, radius : float):
        self.radius = radius

    def intersect(self, other : Self) -> CollisionType:
        dist : float = self.center.dist_between(other.center)
        
        collision = dist - self.radius - other.radius
        print(collision)
        if (collision + other.radius <= 0.0):
            return CollisionType.INSIDE
        elif (collision <= 0.0):
            return CollisionType.INTERSECT
        else:
            return CollisionType.OUTSIDE
        
    def update_status(self, other : Self):
        collision_result = CollisionType = self.intersect(other)
        print(collision_result)
        # colors = [pyxel.COLOR_GREEN, pyxel.COLOR_RED, pyxel]
        match collision_result:
            case CollisionType.INSIDE:
                self.color = pyxel.COLOR_GREEN
            case CollisionType.OUTSIDE:
                self.color = pyxel.COLOR_RED
            case CollisionType.INTERSECT:
                self.color = pyxel.COLOR_NAVY