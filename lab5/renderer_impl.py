from tkinter import *
from point import Point
from idle_state import IdleState


class RendererImpl(Canvas):

    def __init__(self, parent, gui_callback_right, gui_callback_left, **kw):
        super().__init__(parent, **kw)
        self.configure(bg="white")

        self.current_class = 0
        self.current_class_counter = 0
        self.train_X, self.train_y = [], []
        self.current_state = IdleState()

        self.bind("<ButtonPress-1>", self.left_mouse_pressed)
        self.bind("<ButtonRelease-1>", self.left_mouse_released)
        self.bind("<B1-Motion>", self.left_mouse_dragged)

        self.gui_callback_right = gui_callback_right
        self.gui_callback_left = gui_callback_left

        self.bind("<Button-3>", self.right_mouse_pressed)

    def draw_line(self, s: Point, e: Point, color: str):
        self.create_line(self.canvasx(s.x), self.canvasy(s.y),
                         self.canvasx(e.x), self.canvasy(e.y),
                         fill=color)

    def clear_canvas(self):
        self.delete("all")

    def right_mouse_pressed(self, event):
        self.current_class += 1
        self.current_class_counter = 0
        self.gui_callback_right()

    def left_mouse_pressed(self, event):
        self.current_state.mouse_down(Point(event.x, event.y))

    def left_mouse_released(self, event):
        self.current_class_counter += 1
        self.current_state.mouse_up(Point(event.x, event.y))
        self.gui_callback_left()

    def left_mouse_dragged(self, event):
        self.current_state.mouse_dragged(Point(event.x, event.y))
