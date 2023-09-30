import pyxel
from enum import Enum
from typing import Self
from vector import Vector2D
from math import sqrt

class CollisionType(Enum):
    OUTSIDE = 0
    INSIDE = 1
    INTERSECT = 2

import math

def circle_collision(x1, y1, r1, x2, y2, r2):
    # Calculate the distance between the centers of the two circles.
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Check if the circles are completely separate or one is contained within the other.
    if distance > r1 + r2 or distance < abs(r1 - r2):
        return []

    # Calculate the angles from the center of the first circle to the points of intersection.
    angle1 = math.atan2(y2 - y1, x2 - x1)
    angle2 = math.acos((r1**2 + distance**2 - r2**2) / (2 * r1 * distance))

    # Calculate the coordinates of the two points of intersection.
    intersection1 = (x1 + r1 * math.cos(angle1 + angle2), y1 + r1 * math.sin(angle1 + angle2))
    intersection2 = (x1 + r1 * math.cos(angle1 - angle2), y1 + r1 * math.sin(angle1 - angle2))

    p1 = Vector2D(intersection1[0], intersection1[1])
    p2 = Vector2D(intersection2[0], intersection2[1])
    return [p1, p2]


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
        distance : float = self.center.dist_between(other.center)
        
        if (distance > self.radius + other.radius):
            return CollisionType.OUTSIDE
        elif (distance < abs(self.radius - other.radius)):
            return CollisionType.INSIDE
        else:
            return CollisionType.INTERSECT
        
    # def update_status(self, other : Self) -> CollisionType:
    #     collision_result : CollisionType = self.intersect(other)
    #     print(collision_result)
    #     # colors = [pyxel.COLOR_GREEN, pyxel.COLOR_RED, pyxel]
    #     match collision_result:
    #         case CollisionType.INSIDE:
    #             self.color = pyxel.COLOR_GREEN
    #         case CollisionType.OUTSIDE:
    #             self.color = pyxel.COLOR_RED
    #         case CollisionType.INTERSECT:
    #             self.color = pyxel.COLOR_NAVY
    #     return collision_result

    def update_status(self, collision : CollisionType):
        match collision:
            case CollisionType.INSIDE:
                self.color = pyxel.COLOR_GREEN
            case CollisionType.OUTSIDE:
                self.color = pyxel.COLOR_RED
            case CollisionType.INTERSECT:
                self.color = pyxel.COLOR_NAVY

    def get_intersections_point(self, other : Self) -> tuple[Vector2D, Vector2D, Self]:
        d= sqrt((other.center.x-self.center.x)**2 + (other.center.y-self.center.y)**2)
        a=(self.radius**2-other.radius**2+d**2)/(2*d)
        tmp = self.radius**2-a**2
        h=sqrt(tmp)
        x2 : float = self.center.x+a*(other.center.x-self.center.x)/d   
        y2 : float = self.center.y+a*(other.center.y-self.center.y)/d   
        # x3 : float = other.center.x+h*(other.center.y-self.center.y)/d       # also x3=x2-h*(y1-y0)/d
        # y3 : float = other.center.y-h*(other.center.x-self.center.x)/d       # also y3=y2+h*(x1-x0)/d

        v1, v2 = circle_collision(self.center.x, self.center.y, self.radius, other.center.x, other.center.y, other.radius)
        return [v1, v2, Circle(Vector2D(x2, y2), h)]
    
class CollisionInfo:
    col_type : CollisionType = CollisionType.OUTSIDE
    collider : Circle = Circle(Vector2D.ZERO, 0.0)
    def __init__(self, col_type : CollisionType, collider : Circle):
        self.col_type = col_type
        self.collider = collider