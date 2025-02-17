import tkinter as tk
from PIL import Image, ImageTk
from Scene import Scene

class SceneManager:

    def __init__(self, canvas, description_label):

        self.canvas = canvas
        self.description_label = description_label
        self.scenes = self.load_scenes()
        self.current_scene = None
    
    def load_scenes(self):

        # Define scenes
        scenes = {
            "Forest": Scene(
                name="Forest",
                description="A dense forest with tall trees and a sense of mystery.",
                image_path="forest.jpg",
                contiguous_scenes=["Forest Pond"]
            ),
            "Forest Pond": Scene(
                name="Forest Pond",
                description="A serene pond surrounded by trees, with the sound of birds in the distance.",
                image_path="forest-pond.jpg",
                contiguous_scenes=["Forest"]
            )
        }

        return scenes
    
    def load_scene(self, scene_name):

        # Update the current scene
        self.current_scene = self.scenes[scene_name]

        # Load the background image
        image = Image.open(self.current_scene.image_path)
        image = image.resize((800, 500), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        # Update the scene description
        self.description_label.config(text=self.current_scene.description)
    
    def get_current_scene(self):

        return self.current_scene