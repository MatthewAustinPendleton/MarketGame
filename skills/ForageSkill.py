from .GatheringSkill import GatheringSkill

class ForageSkill(GatheringSkill):
    def __init__(self):
        super().__init__("Foraging")
        
    def can_gather(self, player, node):
        return True  # Foraging has no requirements
        
    def get_gather_time(self, player, node):
        base_time = 20  # 60 seconds base time
        time_reduction = (self.level - 1) * 2  # 2 seconds per level
        return max(5, base_time - time_reduction)  # Minimum 5 seconds