from pygame import Vector2, Surface, Rect, Color
from pygame.font import Font


class Camera:
    def __init__(self, x: int, y: int, screen: Surface):
        """
        Creates a camera object
        @bug scaling not considered
        @param x: initial x position of the camera in *world coordinate*
        @param y: initial y position of the camera in *world coordinate*
        @param screen: screen object used to determine width and height of the camera view
        """
        self.centre = Vector2(x, y)
        self.size = Vector2(screen.get_size())
        self.top_left = self.centre - self.size / 2
        self.rect = Rect(self.top_left, self.size)

    def move_to(self, centre: Vector2):
        """
        Moves the camera to a position in the world. Sets camera's rect and position attributes
        @param centre: camera's new central position in *world coordinate*
        @return: None
        """
        self.centre = centre
        self.top_left = self.centre - self.size / 2
        self.rect = Rect(self.top_left, self.size)

    def clamp(self, area: Rect):
        """
        Bounds the camera view inside a rectangular area
        @param area: the area where the camera is restricted in
        @return: None
        """
        self.rect = self.rect.clamp(area)
        self.centre = Vector2(self.rect.center)
        self.top_left = Vector2(self.rect.topleft)

    def from_world(self, world_coords: Vector2) -> Vector2:
        """
        Converts world coordinates to view coordinates based on the camera's position
        @param world_coords: world coordinates to convert
        @return: the point in camera coordinate. Can be used to draw on the screen
        """
        return world_coords - self.top_left


class TextUI:
    def __init__(self, x: int, y: int, text: str = None):
        """
        Creates a UI element for displaying text
        @note This UI element uses *screen coordinate*. It should be used as a message at a fixed position on the
        screen rather than a piece of text following an object.
        @param x: x position on the screen
        @param y: y position on the screen
        @param text: text content in the UI element
        """
        self.position = Vector2(x, y)
        self.text = text if text is not None else ""
        self.surface = None
        self.font = Font(None, 36)

    def set_text(self, text: str = None):
        """
        Sets the text content of this UI element
        @param text: text content to display
        @return: None
        """
        self.text = text if text is not None else ""

    def render(self, screen: Surface):
        """
        Draws the element onto the screen
        @param screen: the screen object to draw on
        @return: None
        """
        rendered = self.font.render(self.text, True, Color(0, 0, 0))
        rect = rendered.get_rect().move(self.position)
        screen.blit(rendered, rect)
