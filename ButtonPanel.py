import tkinter as tk
import math

class ButtonPanel:

    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.buttons = []
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(expand=True)
    
    def add_button(self, text, command):

        button = tk.Button(self.button_frame, text=text, command=command)
        self.buttons.append(button)
        self._arrange_buttons()
    
    def clear_buttons(self):

        for button in self.buttons:
            button.destroy()
        self.buttons = []
    
    def _arrange_buttons(self):

        for button in self.buttons:
            button.grid_forget()
        
        num_buttons = len(self.buttons)
        if num_buttons <= 4:
            for i, button in enumerate(self.buttons):
                button.grid(row=0, column=i, padx=5, pady=5)
        else:
            cols = min(4, math.ceil(math.sqrt(num_buttons)))
            rows = math.ceil(num_buttons / cols)

            for i, button in enumerate(self.buttons):
                row = i // cols
                col = i % cols
                button.grid(row=row, column=col, padx=5, pady=5)
    def disable_buttons(self):
        for button in self.buttons:
            button.configure(state='disabled')

    def enable_buttons(self):
        for button in self.buttons:
            button.configure(state='normal')
    def setup_movement_buttons(self, scene_names, move_callback, cancel_callback):
        """Setup movement buttons for scene navigation"""
        self.clear_buttons()
        for scene_name in scene_names:
            self.add_button(
                f"Go to {scene_name}", 
                lambda s=scene_name: move_callback(s)
            )
        self.add_button("Cancel", cancel_callback)

    def setup_scene_buttons(self, scene, move_callback, activity_callback):
        """Setup buttons for the current scene"""
        self.clear_buttons()
        self.add_button("Move", move_callback)
        for activity, enabled in scene.activities.items():
            if enabled:
                self.add_button(activity.capitalize(), 
                    lambda a=activity: activity_callback(a))