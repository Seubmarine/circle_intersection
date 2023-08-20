import pyxel
from circle import Circle
from vector import Vector2D

class App:
    circles : list[Circle] = [Circle(Vector2D(28, 60), 21)]
    new_zone : Circle = Circle(Vector2D.ZERO, 10)
    
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        # self.circles[0] = Circle(Vector2D(28, 60), 21)
        pyxel.run(self.update, self.draw)

    def update(self):
        mouse_pos : Vector2D = Vector2D(pyxel.mouse_x, pyxel.mouse_y)

        self.new_zone.set_pos(mouse_pos)
        # self.new_zone.intersect(self.circles[0])
        self.new_zone.update_status(self.circles[0])
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        for circle in self.circles:
            circle.draw_circle()
        self.new_zone.draw_circle()


App()