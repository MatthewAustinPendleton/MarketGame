class ForageAnimation:
    def __init__(self, canvas, inventory, scene_canvas, main_container):
        self.canvas = canvas
        self.inventory = inventory
        self.scene_canvas = scene_canvas
        self.main_container = main_container
        self.is_animating = False
        self._current_item = None
        self._photo_image = None

    def start_foraging(self, item, button_panel):
        if self.is_animating:
            return
            
        self.canvas.delete("all")
        self.is_animating = True
        self.button_panel = button_panel
        self._current_item = item
        
        # Find target slot
        self.target_slot = None
        for slot in self.inventory.slots:
            if slot.item and slot.item.name == item.name:
                self.target_slot = slot
                break
        
        if not self.target_slot:
            self.target_slot = self.inventory.get_empty_slot()
        
        # Make window visible and position it
        window = self.canvas.master
        window.attributes('-alpha', 1)
        
        # Calculate center position
        initial_size = 20
        image = item.get_display_image(initial_size)
        self._photo_image = image  # Store reference
        
        # Position in center of scene canvas
        scene_x = self.scene_canvas.winfo_width() // 2
        scene_y = self.scene_canvas.winfo_height() // 2
        
        image_id = self.canvas.create_image(scene_x, scene_y, image=self._photo_image)
        self._animate_growth(image_id, initial_size, 85)

    def _animate_growth(self, image_id, current_size, target_size):
        if not self.is_animating:
            return
            
        growth_rate = 2
        new_size = current_size + growth_rate
        
        if new_size >= target_size:
            new_size = target_size
            if self.target_slot:
                self._animate_flying(image_id, self.target_slot)
            else:
                self._end_animation()
            return
        
        # Update image size
        new_image = self._current_item.get_display_image(new_size)
        self._photo_image = new_image  # Update reference
        self.canvas.itemconfig(image_id, image=self._photo_image)
        
        self.canvas.after(16, lambda: self._animate_growth(image_id, new_size, target_size))

    def _animate_flying(self, image_id, target_slot):
        current_pos = self.canvas.coords(image_id)
        if not current_pos:
            return
            
        # Get target position (center of inventory slot)
        slot_x = target_slot.canvas.winfo_rootx() - self.canvas.master.winfo_rootx()
        slot_y = target_slot.canvas.winfo_rooty() - self.canvas.master.winfo_rooty()
        
        # Add offset to target the center of the slot (slots are 55x55)
        target_x = slot_x + (target_slot.canvas.winfo_width() // 2)
        target_y = slot_y + (target_slot.canvas.winfo_height() // 2)
        
        dx = (target_x - current_pos[0]) * 0.1
        dy = (target_y - current_pos[1]) * 0.1
        
        if abs(dx) < 1 and abs(dy) < 1:
            # Add item to inventory
            if target_slot.has_item():
                target_slot.item._stack_size += 1
                target_slot.update_display()
            else:
                target_slot.add_item(self._current_item)
            self._end_animation()
        else:
            self.canvas.move(image_id, dx, dy)
            self.canvas.after(16, lambda: self._animate_flying(image_id, target_slot))

    def _end_animation(self):
        self.canvas.delete("all")
        self.is_animating = False
        self.canvas.master.attributes('-alpha', 0)
        if self.button_panel:
            self.button_panel.enable_buttons()
        self._current_item = None
        self._photo_image = None
        self.target_slot = None