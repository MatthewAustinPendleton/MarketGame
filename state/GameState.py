class GameState:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.current_scene = None
        self.inventory = None
        self.skills = {}
        
    def update_scene(self, scene):
        self.current_scene = scene
        self.event_manager.emit('scene_changed', scene)