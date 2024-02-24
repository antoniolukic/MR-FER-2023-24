from __future__ import annotations
from typing import Dict
from tkinter import *
from tkinter import ttk
from renderer_impl import RendererImpl
from draw_state import DrawState
from data_cleaning import *
from neural_network import *
import threading


class Gui(Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.canvas1 = None
        self.network = None
        self.additional_labels_frame = None
        self.label_examples = None
        self.init_toolbar()

    def init_toolbar(self):
        notebook = ttk.Notebook()
        notebook.pack(fill=BOTH, expand=True)

        frame1 = Frame(notebook)  # create the frames
        frame2 = Frame(notebook)
        frame3 = Frame(notebook)

        self.create_frame1(frame1)  # configure the frames
        self.create_frame2(frame2)
        self.create_frame3(frame3)

        notebook.add(frame1, text="Defining examples")
        notebook.add(frame2, text="Network learning")
        notebook.add(frame3, text="Using the network")

        self.bind("<Configure>", self.on_resize)

    def create_frame1(self, frame1):
        self.canvas1 = RendererImpl(frame1, self.on_right_mouse_click, self.on_left_mouse_click)
        self.canvas1.current_state = DrawState(self.canvas1)
        self.canvas1.pack(side=LEFT, fill=BOTH, expand=1)

        label_frame = Frame(frame1, bd=1, relief=SOLID)
        label_frame.pack(side=TOP, anchor=NE, padx=1)
        label_class = Label(label_frame, text="  Class  ")
        label_class.pack(side=LEFT)
        separator_line = Canvas(label_frame, width=1, height=20, bg="black")
        separator_line.pack(side=LEFT)
        label_examples = Label(label_frame, text="No. of Examples")
        label_examples.pack(side=LEFT, padx=1)

        self.additional_labels_frame = Frame(frame1)  # Frame to hold additional labels
        self.additional_labels_frame.pack(side=TOP, anchor=NE, padx=1)

        self.on_right_mouse_click()

    def on_right_mouse_click(self):
        both = Frame(self.additional_labels_frame, bd=1, relief=SOLID)
        label_class = Label(both, text=str(self.canvas1.current_class), width=5)
        label_class.pack(side=LEFT)
        separator_line = Canvas(both, width=1, height=20, bg="black")
        separator_line.pack(side=LEFT)
        self.label_examples = Label(both, text=str(self.canvas1.current_class_counter), width=13)
        self.label_examples.pack(side=RIGHT)
        both.pack(side=TOP)

    def on_left_mouse_click(self):
        self.label_examples.config(text=str(self.canvas1.current_class_counter))

    def create_frame2(self, frame2):
        table_frame = Frame(frame2)
        table_frame.pack(side=TOP, anchor=NW, padx=1)

        entries = {}
        labels_col1 = ["Type of algorithm:", "M - number of inputs:", "Hidden layers (separated by comma):",
                       "Eta:", "Iteration limit:", "Maximal acceptable error:", "Data:"]

        for i, label_text in enumerate(labels_col1):
            text = Label(table_frame, text=label_text)
            text.grid(row=i, column=0, sticky=E)

            if label_text == "Data:":
                data_options = ["Drawn examples", "Load examples"]
                selected_data = StringVar()
                selected_data.set("Drawn examples")
                data_menu = OptionMenu(table_frame, selected_data, *data_options)
                data_menu.grid(row=i, column=1, padx=1, pady=5, sticky=W)
                entries[label_text] = selected_data
            elif label_text == "Type of algorithm:":
                algorithm_options = ["Stochastic backpropagation", "Mini-batch backpropagation, must be with load data",
                                     "Batch backpropagation"]
                selected_algorithm = StringVar()
                selected_algorithm.set(algorithm_options[0])
                dropdown_menu = OptionMenu(table_frame, selected_algorithm, *algorithm_options)
                dropdown_menu.grid(row=i, column=1, padx=1, sticky=W)
                entries[label_text] = selected_algorithm
            else:
                entry_widget = Entry(table_frame)
                entry_widget.grid(row=i, column=1, padx=1, sticky=W)
                entries[label_text] = entry_widget

        buttons = Frame(table_frame)
        train_button = Button(buttons, text="Train", command=lambda: threading.Thread(target=self.train_network, args=(entries,)).start())
        train_button.grid(row=len(labels_col1) + 1, column=0, pady=10)
        stop_button = Button(buttons, text="Stop", command=self.stop_network)
        stop_button.grid(row=len(labels_col1) + 1, column=1, pady=10)
        buttons.grid(row=len(labels_col1) + 1, column=0, sticky=E)

    def train_network(self, entries):
        self.given_arguments(entries, self.canvas1.train_X, self.canvas1.train_y)

    def stop_network(self):
        try:
            self.network.stop = True
        except AttributeError:
            print("Network is not created yet")

    def create_frame3(self, frame3):
        self.canvas2 = RendererImpl(frame3, None, self.draw_on_left_click)
        self.canvas2.current_state = DrawState(self.canvas2)
        self.canvas2.pack(side=BOTTOM, fill=BOTH, expand=1)

        self.histogram_canvas = Canvas(frame3, width=100, height=100)
        self.histogram_canvas.pack(side=TOP, fill='both', expand=True)

        self.create_histogram([])

    def create_histogram(self, data):
        if len(data) == 0:
            label = Label(self.histogram_canvas, text="No data to show")
            label.pack(side=TOP, fill='both', expand=True, pady=10)
            return

        print(data)

        for child in self.histogram_canvas.winfo_children():
            if isinstance(child, Label):
                child.destroy()
        self.histogram_canvas.delete("all")

        num_bins = len(data)

        for i in range(num_bins):
            rect_height = data[i] * 150

            self.histogram_canvas.create_rectangle(
                i * (590 / num_bins), 150 - rect_height,
                (i + 1) * (590 / num_bins), 150,
                fill='blue', outline='black'
            )
            bin_class = Label(self.histogram_canvas, text=f"Class {i}")
            bin_class.place(
                x=(i + 0.5) * (590 / num_bins),
                y=165,
                anchor="center"
            )

    def draw_on_left_click(self):
        test_x = [self.canvas2.current_state.all_mouse_points]
        test_x, test_y = transform_data(test_x, [0], self.network.layers[0] // 2)  # y is irellevant
        output = self.network.feed_forward(test_x[0])
        self.create_histogram(output)

    def on_resize(self, event):  # resize the on stretch
        width = event.width
        height = event.height

        self.canvas1.config(width=width, height=height)
        self.pack_propagate(False)
        self.pack(fill=BOTH, expand=True)

    def given_arguments(self, entries: Dict, train_x, train_y):
        alg_type, m, hidden, eta, iteration, error = "", 0, [], 0, 0, 0
        for name, element in entries.items():
            if name == "Type of algorithm:":
                alg_type = element.get()
            elif name == "M - number of inputs:":
                try:
                    m = int(element.get())
                except Exception as e:
                    print(f"Error converting 'M' value to integer:", e)
            elif name == "Hidden layers (separated by comma):":
                try:
                    hidden = [int(x.strip()) for x in element.get().split(",")]
                except Exception as e:
                    print(f"Error processing 'Hidden layers': {e}")
            elif name == "Eta:":
                try:
                    eta = float(element.get())
                except Exception as e:
                    print(f"Error converting 'Eta' value to float: {e}")
            elif name == "Iteration limit:":
                try:
                    iteration = int(element.get())
                except Exception as e:
                    print(f"Error converting 'Iteration limit' value to integer: {e}")
            elif name == "Maximal acceptable error:":
                try:
                    error = float(element.get())
                except Exception as e:
                    print(f"Error converting 'Maximal acceptable error' value to float: {e}")

        if entries["Data:"].get() == "Load examples":
            train_x, train_y = load_data_from_file('saved_data')
            output = 5
        else:
            train_x, train_y = transform_data(train_x, train_y, m)
            output = len(train_y[0])
        act_fun = Sigmoid(1)
        self.network = Nnetwork(2 * m, hidden, output, eta, act_fun.transformation, act_fun.derivation, iteration,
                                error, entries["Type of algorithm:"].get())
        self.network.train(train_x, train_y)
