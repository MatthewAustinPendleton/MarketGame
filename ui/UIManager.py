import tkinter as tk
from tkinter import ttk

class UIManager:
    def __init__(self, root, event_manager):
        self.root = root
        self.event_manager = event_manager
        
        # Initialize window properties
        self._setup_window()
        
        # Initialize UI containers
        self._setup_containers()
        
        # Initialize UI components
        self._setup_components()
    def _setup_window(self):
        self.root.title("Economia")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Grid Layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=1)

    def _setup_containers(self):
        # Main container
        self.main_container = tk.Frame(self.root, width=750, height=600)
        self.main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right container
        self.right_container = tk.Frame(self.root, width=270, height=600)
        self.right_container.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        self.right_container.pack_propagate(False)

    def _setup_components(self):
        # Scene canvas
        self.canvas = tk.Canvas(self.main_container, width=600, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Description label
        self.description_label = tk.Label(self.main_container, text="", 
                                        font=("Arial", 12), wraplength=600)
        self.description_label.pack(pady=10)
        
        # Setup animation window
        self._setup_animation_window()
        
        # Notebook setup continues...
        
    def _setup_animation_window(self):
        """Setup the transparent animation overlay window"""
        self.animation_window = tk.Toplevel(self.root)
        self.animation_window.overrideredirect(True)
        self.animation_window.attributes('-alpha', 0)
        self.animation_window.attributes('-topmost', True)
        self.animation_window.attributes('-transparentcolor', self.root.cget('bg'))
        def update_animation_window_position(event=None):
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.animation_window.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{x}+{y}")
        self.root.bind('<Configure>', update_animation_window_position)
        update_animation_window_position()
        self.animation_canvas = tk.Canvas(
            self.animation_window,
            width=1000,
            height=700,
            highlightthickness=0,
            bg=self.root.cget('bg')
        )
        self.animation_canvas.pack(fill=tk.BOTH, expand=True)
        self.animation_window.attributes('-transparentcolor', self.root.cget('bg'))
        # Notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.right_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Inventory container
        self.inventory_container = tk.Frame(self.notebook, bg="gray")
        self.notebook.add(self.inventory_container, text="Inventory")

        # Skills container
        self.skills_container = tk.Frame(self.notebook, bg="gray")
        self.notebook.add(self.skills_container, text="Skills")

    def create_skill_display(self, skill):
        """Create and return the UI elements for a skill display"""
        # Skills header
        header = tk.Label(self.skills_container, text="Gathering Skills", 
                         font=("Arial", 14, "bold"), bg="gray", fg="white")
        header.pack(pady=10)
        
        # Skill frame
        skill_frame = tk.Frame(self.skills_container, bg="gray")
        skill_frame.pack(fill=tk.X, padx=10, pady=5)
        
        skill_label = tk.Label(skill_frame, 
            text=f"{skill.name} - Level {skill.level}", 
            font=("Arial", 12), bg="gray", fg="white")
        skill_label.pack(anchor="w")
        
        exp_progress = ttk.Progressbar(skill_frame, length=200, mode='determinate')
        exp_progress.pack(pady=5)
        
        exp_text = tk.Label(skill_frame, 
            text=f"XP: {skill.experience}/{skill.get_exp_required()}", 
            font=("Arial", 10), bg="gray", fg="white")
        exp_text.pack()
        
        return {
            'level_label': skill_label,
            'exp_bar': exp_progress,
            'exp_label': exp_text
        }
    def switch_to_inventory(self):
        """Switch to the inventory tab"""
        self.notebook.select(0)
    def get_scene_canvas(self):
        """Get the canvas for scene rendering"""
        return self.canvas

    def get_description_label(self):
        """Get the label for scene descriptions"""
        return self.description_label

    def get_main_container(self):
        """Get the main container for UI elements"""
        return self.main_container

    def get_inventory_container(self):
        """Get the container for inventory"""
        return self.inventory_container

    def get_skills_container(self):
        """Get the container for skills"""
        return self.skills_container

    def get_animation_canvas(self):
        """Get the canvas for animations"""
        return self.animation_canvas