# Testing commit

import tkinter as tk
from SceneManager import SceneManager
from ButtonPanel import ButtonPanel
from Inventory import Inventory

class GameWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Economia")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Grid Layout (Fix Inventory Overflow)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=4)  # 75% for scene
        self.root.grid_columnconfigure(1, weight=1)  # 25% for inventory

        # Main game container (for scene)
        self.main_container = tk.Frame(self.root, width=600, height=600)  # Limit width
        self.main_container.grid(row=0, column=0, sticky="nsew")

        # Canvas for scene background
        self.canvas = tk.Canvas(self.main_container, width=600, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Scene description label
        self.description_label = tk.Label(self.main_container, text="", font=("Arial", 12), wraplength=600)
        self.description_label.pack(pady=10)

        # Initialize SceneManager
        self.scene_manager = SceneManager(self.canvas, self.description_label)

        # Button Panel for actions
        self.button_panel = ButtonPanel(self.root)
        self.scene_manager.load_scene("Forest")
        self.load_buttons()

        # Inventory UI (Constrain its Width)
        self.inventory_container = tk.Frame(self.root, width=200, height=600, bg="gray")  
        self.inventory_container.grid(row=0, column=1, sticky="nsew")
        self.inventory_container.grid_propagate(False)  # Prevent resizing past set width

        # Inventory Object (Inside Constrained Container)
        self.inventory = Inventory(self.inventory_container)

    def move_to_scene(self):
        current_scene = self.scene_manager.get_current_scene()
        if current_scene and current_scene.contiguous_scenes:
            new_scene = current_scene.contiguous_scenes[0]
            self.scene_manager.load_scene(new_scene)
            self.load_buttons()  # Load the buttons for the new scene

    def load_buttons(self):

        self.button_panel.clear_buttons()
        self.button_panel.add_button("Move", self.move_to_scene)
        current_scene = self.scene_manager.get_current_scene()
        for activity, enabled in current_scene.activities.items():
            if enabled:
                self.button_panel.add_button(activity.capitalize(), lambda a=activity: self.activity_handler(a))
    def activity_handler(self, activity):

        print(f"{activity} button clicked!")
if __name__ == "__main__":
    root = tk.Tk()
    game = GameWindow(root)
    root.mainloop()
