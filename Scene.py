from PIL import Image, ImageTk
from Item import Item, LootTable

class Scene:

    def __init__(self, name, description, image_path, contiguous_scenes, activities=None):

        self.name = name
        self.description = description
        self.image_path = image_path
        self.contiguous_scenes = contiguous_scenes
        self.activities = activities if activities else {}

        # Store resized image separately to prevent UI shifting
        self.resized_image = None

        self.forage_loot_table = LootTable()

        # Initialize default loot tables if this is Forest or Cavern Entrance
        if name == "Forest":
            apple = Item("Apple", "items/apple.png")
            acorn = Item("Acorn", "items/acorn.png")
            self.forage_loot_table.add_item(apple, 60)
            self.forage_loot_table.add_item(acorn, 40)
        elif name == "Cavern Entrance":
            apple = Item("Apple", "items/apple.png")
            rock = Item("Rock", "items/rock.png")
            flint = Item("Flint", "items/flint.png")
            twig = Item("Twig", "items/twig.png")
            self.forage_loot_table.add_item(apple, 25)
            self.forage_loot_table.add_item(rock, 30)
            self.forage_loot_table.add_item(flint, 20)
            self.forage_loot_table.add_item(twig, 25)

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