import tkinter as tk

class Inventory:

    def __init__(self, parent):

        self.frame = tk.Frame(parent, bg="gray")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.grid_propagate(False)  # Prevent resizing issues

        # Inventory Label
        self.label = tk.Label(self.frame, text="Inventory", font=("Arial", 14, "bold"), bg="gray", fg="black")
        self.label.pack(pady=5)  # Add space to make label readable

        # Inventory Grid (3x3)
        self.slot_frame = tk.Frame(self.frame, bg="gray")
        self.slot_frame.pack(pady=10)

        self.slots = []
        for row in range(7):
            for col in range(4):
                slot = tk.Label(self.slot_frame, text="", width=6, height=3, bg="white", borderwidth=2, relief="ridge")
                slot.grid(row=row, column=col, padx=5, pady=5)  # Add padding for spacing
                self.slots.append(slot)
