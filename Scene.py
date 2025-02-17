from PIL import Image, ImageTk

class Scene:

    def __init__(self, name, description, image_path, contiguous_scenes):

        self.name = name
        self.description = description
        self.image_path = image_path
        self.contiguous_scenes = contiguous_scenes

        # Store resized image separately to prevent UI shifting
        self.resized_image = None

    def load_scene_image(self, target_width=500, target_height=400):

        try:
            img = Image.open(self.image_path)
            img = img.resize((target_width, target_height), Image.LANCZOS)
            self.resized_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading scene image: {e}")
            self.resized_image = None
    
    def get_image(self):

        if not self.resized_image:
            self.load_scene_image()
        return self.resized_image