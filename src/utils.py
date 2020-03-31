from pygame import Vector2, Surface, Rect, Color
from pygame.font import Font


class Camera:
    def __init__(self, x: int, y: int, screen: Surface):
        self.centre = Vector2(x, y)
        self.size = Vector2(screen.get_size())
        self.top_left = self.centre - self.size / 2
        self.rect = Rect(self.top_left, self.size)

    def move_to(self, centre: Vector2):
        self.centre = centre
        self.top_left = self.centre - self.size / 2
        self.rect = Rect(self.top_left, self.size)

    def clamp(self, area: Rect):
        self.rect = self.rect.clamp(area)
        self.centre = Vector2(self.rect.center)
        self.top_left = Vector2(self.rect.topleft)

    def from_world(self, world_coords: Vector2) -> Vector2:
        return world_coords - self.top_left


class TextUI:
    def __init__(self, x: int, y: int, text: str = None):
        self.position = Vector2(x, y)
        self.text = text if text is not None else ""
        self.surface = None
        self.font = Font(None, 36)

    def set_text(self, text: str = None):
        self.text = text if text is not None else ""

    def render(self, screen: Surface):
        rendered = self.font.render(self.text, True, Color(0, 0, 0))
        rect = rendered.get_rect().move(self.position)
        screen.blit(rendered, rect)
