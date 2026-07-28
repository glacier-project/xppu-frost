from typing_extensions import Self
import pygame
from pygame.camera import Camera
import threading
from shape import Shape

ZOOM_FACTOR = 1000.0  # Adjust as needed for scaling shapes to screen coordinates

class PyGameManager:
    _instance: "PyGameManager | None" = None

    def __new__(cls, *args, **kwargs) -> "PyGameManager":
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self, width: int, height: int, fps: int) -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self.screen: pygame.Surface | None = None
        self.background: pygame.Surface | None = None
        self.dynamic_elements: list[tuple[Shape, str | None]] = []

    def start(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        background = pygame.Surface((self.width, self.height))
        background.fill((255, 255, 255))
        self.background = background

    def stop(self) -> None:
        self.screen = None
        self.background = None
        self.dynamic_elements: list[tuple[Shape, str | None]] = []
        pygame.quit()

    def add_static_element(self, shape: Shape, text: str | None = None) -> None:
        if self.background is None:
            raise RuntimeError("PyGameManager not started. Call start() before adding elements.")
        self._draw_shape_on_surface(self.background, shape, text)

    def add_dynamic_element(self, shape: Shape, text: str | None = None) -> None:
        self.dynamic_elements.append((shape, text))

    def _draw_shape_on_surface(self, surface: pygame.Surface, shape: Shape, text: str | None) -> None:
        shape.draw(surface, ZOOM_FACTOR)
        # Optionally, add text rendering here if needed
        if not text:
            return

        center = shape.centroid_pos
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(center.x*ZOOM_FACTOR, center.y*ZOOM_FACTOR))
        surface.blit(text_surface, text_rect)

    def render(self) -> None:
        if self.screen is None or self.background is None:
            raise RuntimeError("PyGameManager not started. Call start() before rendering.")

        self.screen.blit(self.background, (0, 0))
        for element, text in self.dynamic_elements:
            self._draw_shape_on_surface(self.screen, element, text)

        pygame.display.flip()

def initialize_pygame_manager(width: int = 800, height: int = 600, fps: int = 60) -> None:
    if PyGameManager._instance is None:
        PyGameManager(width, height, fps)

def start_pygame_manager() -> PyGameManager:
    pygame_manager = get_pygame_manager()
    pygame_manager.start()
    return pygame_manager

def get_pygame_manager() -> PyGameManager:
    if PyGameManager._instance is None:
        raise RuntimeError("PyGameManager not initialized. Call initialize_pygame_manager() first.")
    return PyGameManager._instance

def stop_pygame_manager() -> None:
    pygame_manager = get_pygame_manager()
    pygame_manager.stop()

def run_pygame_event_loop() -> None:
    pygame_manager = start_pygame_manager()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame_manager.render()
        clock.tick(pygame_manager.fps)
    pygame_manager.stop()


pygame_thread: threading.Thread | None = None
def run_pygame_event_loop_in_thread() -> None:
    import time
    global pygame_thread
    thread = threading.Thread(target=run_pygame_event_loop)
    thread.start()
    pygame_thread = thread

    # Wait for PyGame window to start
    for _ in range(100):  # up to 1 second
        try:
            manager = get_pygame_manager()
            if manager.screen is not None:
                break
        except Exception:
            pass
        time.sleep(0.01)

def stop_pygame_event_loop() -> None:
    global pygame_thread
    # Only post QUIT event if pygame is initialized
    if pygame.get_init():
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    if pygame_thread is not None:
        pygame_thread.join()
        pygame_thread = None
