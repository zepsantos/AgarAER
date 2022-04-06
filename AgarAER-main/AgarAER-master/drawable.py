class Drawable:
    """Used as an abstract base-class for every drawable element.
    """

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass
    
    