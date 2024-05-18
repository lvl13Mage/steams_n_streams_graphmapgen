import pygame
import pygame_gui
from event_handler import EventHandler
from graph_manager import GraphManager
from ui_drawing import UIDrawing

# Initialize pygame
pygame.init()
pygame.display.set_caption('Interactive Graph Map with UI')

# Get screen resolution and set window size to 70%
info_object = pygame.display.Info()
print(info_object.current_w, info_object.current_h)
WIDTH, HEIGHT = int(info_object.current_w * 0.7), int(info_object.current_h * 0.7)
window_surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)

# Load the background image and adjust it to window size
background_image_path = 'background.jpg'
background = pygame.image.load(background_image_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale background to window size
background_rect = background.get_rect()

manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

graph_manager = GraphManager(WIDTH, HEIGHT)

# GUI elements
node_count_entry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 10), (100, 25)),
    text='Node Count:',
    manager=manager
)
node_count_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((110, 10), (50, 30)),
    manager=manager
)
node_count_entry.set_text(str(graph_manager.num_nodes))  # Default node count
#max_distance_entry_label = pygame_gui.elements.UILabel(
#    relative_rect=pygame.Rect((10, 50), (100, 25)),
#    text='Max Distance:',
#    manager=manager
#)
#max_distance_entry = pygame_gui.elements.UITextEntryLine(
#    relative_rect=pygame.Rect((110, 50), (50, 30)),
#    manager=manager
#)
#max_distance_entry.set_text(str(graph_manager.max_distance))  # Default max distance

# Initialize modules
ui_drawing = UIDrawing(window_surface, graph_manager, background)
event_handler = EventHandler(graph_manager, ui_drawing, manager, node_count_entry)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            event_handler.handle_event(event)

    ui_drawing.draw_graph()
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()

# Save graph to JSON before closing
graph_manager.to_json()

pygame.quit()
