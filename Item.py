from PIL import Image, ImageTk

class Item:
    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path
        self._stack_size = 1
        self._load_image()  # Call this first to set up all image attributes

    def _load_image(self):
        # Load base image
        self.image = Image.open(self.image_path)
        
        # Create inventory icon (55x55)
        inventory_size = 55
        width, height = self.image.size
        ratio = min(inventory_size / width, inventory_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        inventory_square = Image.new('RGBA', (inventory_size, inventory_size), (0, 0, 0, 0))
        inventory_resized = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        x = (inventory_size - new_width) // 2
        y = (inventory_size - new_height) // 2
        inventory_square.paste(inventory_resized, (x, y), inventory_resized)
        self.icon = ImageTk.PhotoImage(inventory_square)
        
        # Create base display image (85x85)
        base_size = 85
        ratio = min(base_size / width, base_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        square = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
        resized = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        x = (base_size - new_width) // 2
        y = (base_size - new_height) // 2
        square.paste(resized, (x, y), resized)
        self.image = square
        
        # Initialize cache
        self._photo_images = {}

    def get_display_image(self, size):
        if size in self._photo_images:
            return self._photo_images[size]
            
        square = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        width, height = self.image.size
        ratio = min(size / width, size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        resized = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        square.paste(resized, (x, y), resized)
        
        photo = ImageTk.PhotoImage(square)
        self._photo_images[size] = photo
        return photo

    @property
    def stack_size(self):
        return self._stack_size

    @stack_size.setter
    def stack_size(self, value):
        self._stack_size = value

class LootTable:

    def __init__(self):

        self.items = []
        self.weights = []

    def add_item(self, item, weight):

        self.items.append(item)
        self.weights.append(weight)

    def roll(self):
        import random
        if not self.items:
            return None
        return random.choices(self.items, weights=self.weights, k=1)[0]
