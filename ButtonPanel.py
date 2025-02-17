import tkinter as tk

class ButtonPanel:

    def __init__(self, root):

        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.buttons = []
    
    def add_button(self, text, command):

        button = tk.Button(self.frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=10)
        self.buttons.append(button)
    
    def clear_buttons(self):

        for button in self.buttons:
            button.destroy()
        self.buttons = []