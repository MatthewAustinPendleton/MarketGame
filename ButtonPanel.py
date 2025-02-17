import tkinter as tk

class ButtonPanel:

    def __init__(self, root):

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.BOTTOM, pady=10)
    
    def add_button(self, text, command):

        button = tk.Button(self.frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=10)

