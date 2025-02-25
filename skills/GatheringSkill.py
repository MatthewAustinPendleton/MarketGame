from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk

class GatheringSkill(ABC):
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.is_gathering = False
        
    def get_exp_required(self):
        return 100 * self.level  # Basic formula, can be adjusted
        
    def add_experience(self, amount):
        self.experience += amount
        if self.experience >= self.get_exp_required():
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.experience -= self.get_exp_required()
        # TODO: Add level up notification
        
    @abstractmethod
    def can_gather(self, player, node):
        pass
        
    @abstractmethod
    def get_gather_time(self, player, node):
        pass
        
    def start_gathering(self, window, node, on_complete):
        if self.is_gathering:
            return False
            
        self.is_gathering = True
        
        # Create progress bar
        progress_frame = tk.Frame(window)
        progress_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        progress = ttk.Progressbar(
            progress_frame, 
            length=200,
            mode='determinate'
        )
        progress.pack()
        
        gather_time = self.get_gather_time(None, node)  # Will pass player later
        steps = 50  # Number of updates
        step_time = gather_time / steps
        
        def update_progress(current_step):
            if current_step >= steps:
                progress_frame.destroy()
                self.is_gathering = False
                on_complete()
                return
                
            progress['value'] = (current_step / steps) * 100
            window.after(int(step_time * 1000), 
                lambda: update_progress(current_step + 1))
                
        update_progress(0)
        return True