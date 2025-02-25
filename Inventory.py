import tkinter as tk

class InventorySlot:

    def __init__(self, frame, row, col):
        # Create a canvas for the slot
        self.canvas = tk.Canvas(
            frame, 
            width=55, 
            height=55, 
            highlightthickness=1,
            highlightbackground="gray",
            bg="#f0f0f0"
        )
        self.canvas.grid(row=row, column=col, padx=2, pady=2)

        # Draw the border
        self.canvas.create_rectangle(
            1, 1, 54, 54,
            outline="gray",
            width=1
        )

        self.item = None
        self.quantity = 0
        self.image_id = None
        self.quantity_id = None

    def has_item(self):
        return self.item is not None
    def update_display(self):
        if self.item and self.item.stack_size > 1:
            if not hasattr(self, 'stack_label'):
                self.stack_label = tk.Label(
                    self.canvas, 
                    text=str(self.item.stack_size),
                    font=('Arial', 12, 'bold'),
                    bg='#f0f0f0',
                    fg='black'
                )
                # Moved up slightly more
                self.stack_label.place(relx=0.65, rely=0.60)
            else:
                self.stack_label.config(text=str(self.item.stack_size))
            self.stack_label.lift()  # Ensure it's on top
            # Adjusted position more to the left and up
            self.stack_label.place(relx=0.65, rely=0.65)
        else:
            self.stack_label.config(text=str(self.item.stack_size))
        self.stack_label.lift()  # Ensure it's on top
    def add_item(self, item, quantity=1):
        if self.item and self.item.name == item.name:
            self.quantity += quantity
        else:
            self.item = item
            self.quantity = quantity

        # Update item image
        if self.image_id:
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(
            28, 28,  # Center of canvas
            image=item.icon
        )

        # Update quantity text
        if self.quantity_id:
            self.canvas.delete(self.quantity_id)
        if self.quantity > 1:
            self.quantity_id = self.canvas.create_text(
                48, 48,  # Bottom right
                text=str(self.quantity),
                font=("Arial", 10, "bold"),
                anchor="se"
            )

class Inventory:

    def __init__(self, parent):

        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.slots = []
        for row in range(8):
            for col in range(4):
                slot = InventorySlot(self.frame, row, col)
                self.slots.append(slot)
    def get_empty_slot(self):
        """Returns the first empty inventory slot, or None if inventory is full"""
        for slot in self.slots:
            if not slot.has_item():
                return slot
        return None
    def get_next_empty_slot(self, item):

        # First check for existing stacks of the same item
        for slot in self.slots:
            if slot.item and slot.item.name == item.name and slot.quantity < slot.item.max_stack:
                return slot
        
        # Then look for empty slots
        for slot in self.slots:
            if not slot.item:
                return slot
        
        return None
    
    def add_item(self, item):

        slot = self.get_next_empty_slot(item)
        if slot:
            slot.add_item(item)