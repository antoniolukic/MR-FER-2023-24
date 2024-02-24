from __future__ import annotations
from renderer_impl import RendererImpl
from point import Point


class DrawState:
    def __init__(self, canvas: RendererImpl):
        self.canvas = canvas
        self.all_mouse_points = []
        self.last_mouse_point = None

    def mouse_down(self, mouse_point: Point) -> None:
        self.canvas.clear_canvas()
        self.all_mouse_points = []
        self.all_mouse_points.append(mouse_point)
        self.last_mouse_point = mouse_point

    def mouse_up(self, mouse_point: Point) -> None:
        self.canvas.train_X.append(self.all_mouse_points)
        self.canvas.train_y.append(self.canvas.current_class)

    def mouse_dragged(self, mouse_point: Point) -> None:
        self.all_mouse_points.append(mouse_point)
        self.canvas.draw_line(self.last_mouse_point, mouse_point, 'black')
        self.last_mouse_point = mouse_point
