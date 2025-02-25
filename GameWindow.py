import tkinter as tk
from SceneManager import SceneManager
from ButtonPanel import ButtonPanel
from Inventory import Inventory
from ForageAnimation import ForageAnimation
from skills.ForageSkill import ForageSkill
from tkinter import ttk
from events.EventManager import EventManager
from state.GameState import GameState
from ui.UIManager import UIManager

class GameWindow:
    def __init__(self, root):
        # Core systems initialization
        self.event_manager = EventManager()
        self.game_state = GameState(self.event_manager)
        self.ui_manager = UIManager(root, self.event_manager)
        
        # Game components initialization
        self._initialize_components(root)
        
        # Event subscriptions
        self._setup_event_handlers()
        
        # Initial game state
        self._load_initial_state()

    def _initialize_components(self, root):
        """Initialize all game components"""
        self.root = root
        self.forage_skill = ForageSkill()
        self.scene_manager = SceneManager(
            self.ui_manager.get_scene_canvas(),
            self.ui_manager.get_description_label()
        )
        self.button_panel = ButtonPanel(self.ui_manager.get_main_container())
        self.inventory = Inventory(self.ui_manager.get_inventory_container())
        self.forage_animation = ForageAnimation(
            self.ui_manager.get_animation_canvas(),
            self.inventory,
            self.ui_manager.get_scene_canvas(),
            self.ui_manager.get_main_container()
        )

    def _setup_skills_display(self):
        """Setup the skills display UI"""
        self.forage_skill.ui_elements = self.ui_manager.create_skill_display(self.forage_skill)

    def _handle_item_gathered(self, item):
        self.event_manager.emit('switch_to_inventory')
        self.event_manager.emit('start_foraging_animation', {'item': item, 'button_panel': self.button_panel})

    def _handle_scene_changed(self, scene):
        self.load_buttons()

    def _handle_skill_updated(self, skill):
        self._update_skill_display(skill)

    def activity_handler(self, activity):
        if activity == "forage":
            self._handle_forage_activity()
        else:
            print(f"{activity} button clicked!")

    def _handle_forage_activity(self):
        current_scene = self.scene_manager.get_current_scene()
        if not current_scene or not current_scene.forage_loot_table:
            return

        # Disable buttons first
        self.event_manager.emit('buttons_disabled')
        
        # Then start gathering
        self.forage_skill.start_gathering(
            self.ui_manager.main_container,
            None,
            lambda: self._complete_forage(current_scene)
        )

    def _complete_forage(self, scene):
        item = scene.forage_loot_table.roll()
        if item:
            self.event_manager.emit('switch_to_inventory')
            self.event_manager.emit('start_foraging_animation', {'item': item, 'button_panel': self.button_panel})
            self.event_manager.emit('skill_experience_gained', {'skill': self.forage_skill, 'amount': 10})

    def _update_skill_display(self, skill):
        if hasattr(skill, 'ui_elements'):
            ui = skill.ui_elements
            ui['level_label'].config(text=f"{skill.name} - Level {skill.level}")
            exp_required = skill.get_exp_required()
            ui['exp_bar']['value'] = (skill.experience / exp_required) * 100
            ui['exp_label'].config(text=f"XP: {skill.experience}/{exp_required}")

    def move_to_scene(self):
        current_scene = self.scene_manager.get_current_scene()
        if current_scene and current_scene.contiguous_scenes:
            # Clear existing buttons
            self.button_panel.clear_buttons()
            
            # Add a button for each available scene
            for scene_name in current_scene.contiguous_scenes:
                self.button_panel.add_button(
                    f"Go to {scene_name}", 
                    lambda s=scene_name: self._perform_move(s)
                )
            
            # Add a cancel button
            self.button_panel.add_button("Cancel", self.load_buttons)

    def _perform_move(self, scene_name):
        self.scene_manager.load_scene(scene_name)
        self.load_buttons()

    def load_buttons(self):
        self.button_panel.clear_buttons()
        # Add Move button first
        self.button_panel.add_button("Move", self.move_to_scene)
        # Then add activity buttons
        current_scene = self.scene_manager.get_current_scene()
        for activity, enabled in current_scene.activities.items():
            if enabled:
                self.button_panel.add_button(activity.capitalize(), 
                    lambda a=activity: self.activity_handler(a))

    def _setup_event_handlers(self):
        """Setup all event subscriptions"""
        self.event_manager.subscribe('item_gathered', self._handle_item_gathered)
        self.event_manager.subscribe('scene_changed', self._handle_scene_changed)
        self.event_manager.subscribe('skill_updated', self._handle_skill_updated)
        # Add new event handlers
        self.event_manager.subscribe('switch_to_inventory', lambda: self.ui_manager.switch_to_inventory())
        self.event_manager.subscribe('start_foraging_animation', 
            lambda data: self.forage_animation.start_foraging(data['item'], data['button_panel']))
        self.event_manager.subscribe('skill_experience_gained', 
            lambda data: data['skill'].add_experience(data['amount']))
        # Fix: Add data parameter to lambda even though we don't use it
        self.event_manager.subscribe('buttons_disabled', lambda _: self.button_panel.disable_buttons())

    def _load_initial_state(self):
        """Load initial game state"""
        self.scene_manager.load_scene("Forest")
        self.load_buttons()
        self._setup_skills_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = GameWindow(root)
    root.mainloop()