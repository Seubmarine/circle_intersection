import pyxel
import copy
from circle import Circle, CollisionType, CollisionInfo
from vector import Vector2D

def collide_with(circles_a : tuple[Circle], circles_b: tuple[Circle]) -> list[CollisionInfo]:
    collisions : list[CollisionInfo] = []    
    for a in circles_a:
        for b in circles_b:
            col_type : CollisionType = a.intersect(b)
            collisions.append(CollisionInfo(col_type, b))
    return collisions

def collision_is_not_outside(collision : CollisionInfo) -> bool:
    return collision.col_type != CollisionType.OUTSIDE

class App:
    circles : list[Circle] = []
    new_zone : Circle = Circle(Vector2D.ZERO, 10)
    new_zone_collision : CollisionType = CollisionType.OUTSIDE
    intersections_points : list[Circle] = []
    intersections_circles : list[Circle] = []
    
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        # self.circles[0] = Circle(Vector2D(28, 60), 21)
        pyxel.run(self.update, self.draw)

    def update(self):
        print("Update")
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.new_zone.radius *= 1.5
        elif pyxel.btnp(pyxel.KEY_SHIFT):
            self.new_zone.radius /= 2
        elif pyxel.btnp(pyxel.KEY_R): #reset all sphere
            self.circles.clear()
        mouse_pos : Vector2D = Vector2D(pyxel.mouse_x, pyxel.mouse_y)
        self.new_zone.set_pos(mouse_pos)
        # self.new_zone.intersect(self.circles[0])
        self.new_zone_collision = CollisionType.OUTSIDE
        
        circles_collisions : list[CollisionInfo] = collide_with([self.new_zone], self.circles)
        for circle in self.circles:
            circle.color = pyxel.COLOR_PEACH

        circles_collisions = list(filter(collision_is_not_outside, circles_collisions))
        for collision in circles_collisions:
            collision.collider.color = pyxel.COLOR_WHITE
                
        for collision in circles_collisions:
            tmp : CollisionInfo = collision
            if tmp.col_type == CollisionType.INSIDE:
                self.new_zone_collision = CollisionType.INSIDE
                break
            elif tmp.col_type == CollisionType.INTERSECT:
                self.new_zone_collision = CollisionType.INTERSECT
        
        circles_touched = [x.collider for x in circles_collisions if x.col_type != CollisionType.OUTSIDE]

        self.intersections_points.clear()
        self.intersections_circles.clear()
        for circle_1 in circles_touched:
            for circle_2 in circles_touched:
                if (circle_1 != circle_2 and circle_1.intersect(circle_2) == CollisionType.INTERSECT):
                    lol = circle_1.center.dist_between(circle_2.center)
                    if lol > max(circle_1.radius, circle_2.radius): #Generate circle only if the middle of one circle is not contained in the other
                        (p1, p2, inter_circle) = circle_1.get_intersections_point(circle_2)
                        for point in (p1, p2):
                            tmp_circle = Circle(point, 1)
                            tmp_circle.color = pyxel.COLOR_ORANGE
                            self.intersections_points.append(tmp_circle)
                        inter_circle.color = pyxel.COLOR_ORANGE
                        # if (self.new_zone.radius < inter_circle.radius):
                        self.intersections_circles.append(inter_circle)

        #remove intersection point that touch more than two circle (keep only outer points) 
        inner_intersections_point : list[Circle] = []
        for point in self.intersections_points[:]:
            number_of_collision : int = 0
            for circle in circles_touched:
                collision : CollisionType = point.intersect(circle)
                if collision == CollisionType.INTERSECT:
                    number_of_collision += 1
                if collision == CollisionType.INSIDE or number_of_collision > 2:
                    self.intersections_points.remove(point)
                    inner_intersections_point.append(point)
                    break

        outer_points_touched = [x for x in self.intersections_points if self.new_zone.intersect(x) != CollisionType.OUTSIDE]
        for p in self.intersections_circles:
            p.color = pyxel.COLOR_RED
        
        for p in outer_points_touched:
            p.color = pyxel.COLOR_LIGHT_BLUE
        inter_circle_touched = [c for c in self.intersections_circles if self.new_zone.intersect(c) != CollisionType.OUTSIDE]
        # print(inter_circle_touched)
        for c in inter_circle_touched:
            c.color = pyxel.COLOR_ORANGE
        inner_intersections_point = [x for x in inner_intersections_point if self.new_zone.intersect(x) != CollisionType.OUTSIDE]            
        print(inner_intersections_point)

        
        # if len(self.intersections_points) > 0 and len(self.intersections_points) != len(outer_points_touched): #Only one circle
        #     self.new_zone_collision = CollisionType.INTERSECT
        #     if len(self.intersections_circles) == 1 and self.new_zone.intersect(self.intersections_circles) == CollisionType.INSIDE:
        #         self.new_zone_collision = CollisionType.INSIDE
        
        print("intercirle")
        print(self.intersections_circles)
        # if 

        if self.intersections_points:# and inner_intersections_point:
            if outer_points_touched:
                print("touch outer")
                self.new_zone_collision = CollisionType.INTERSECT
            elif len(circles_touched) == 2: #TODO: two should be one but every collision are reported twice currently
                c1, c2 = circles_touched
                # c1.color = pyxel.COLOR_DARK_BLUE
                # print(c1.center.dist_between(self.new_zone.center) < c1.radius)
                if c1.center.dist_between(self.new_zone.center) < c1.radius and c2.center.dist_between(self.new_zone.center) < c2.radius:
                    print("Yeepi")
                    self.new_zone_collision = CollisionType.INSIDE
            elif len(inner_intersections_point) >= 4:
                print("touch inner")
                self.new_zone_collision = CollisionType.INSIDE
            # elif inter_circle_touched:
            #     print("inside intersection circle")
            #     self.new_zone_collision = CollisionType.INSIDE
        # if len(points_touched) == 0 and len(self.intersections_points) != 0 and len(inter_circle_touched) >= 1:
        #     if len(inter_circle_touched) == 1 and self.new_zone.intersect(inter_circle_touched[0]) != CollisionType.INSIDE:
        #         self.new_zone_collision = CollisionType.INTERSECT
        #     elif len(inter_circle_touched) == len(self.intersections_circles):
        #         self.new_zone_collision = CollisionType.INSIDE
        #     elif len(inner_intersections_point) >= (2 * 2):
        #         self.new_zone_collision = CollisionType.INSIDE

        self.new_zone.update_status(self.new_zone_collision)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for circle in self.circles[:]: #Do a shallow copy to remove while iterating
                if self.new_zone.intersect(circle) == CollisionType.INSIDE:
                    if self.new_zone.radius < circle.radius:
                        return #Your circle is inside of another circle
                    else:
                        self.circles.remove(circle) #Your circle is bigger than the previous circles known so you can remove them
            self.circles.append(copy.deepcopy(self.new_zone))
            
        #     #At this point we recalculate every intersection point and keep only those that are "outside" (only touch two circles)
        #     self.intersections_points.clear()
        #     for circle_1 in self.circles:
        #         for circle_2 in self.circles:
        #             if (circle_1 != circle_2 and circle_1.intersect(circle_2) == CollisionType.INTERSECT):
        #                 for point in circle_1.get_intersections_point(circle_2):
        #                     tmp_circle = Circle(point, 2)
        #                     tmp_circle.color = pyxel.COLOR_ORANGE
        #                     self.intersections_points.append(tmp_circle)
        #                     print("Append points")


    def draw(self):
        pyxel.cls(0)
        for circle in self.circles:
            circle.draw_circle()
        for intersection_circle in self.intersections_circles:
            intersection_circle.draw_circle()
        for points in self.intersections_points:
            points.draw_circle()
        self.new_zone.draw_circle()


App()