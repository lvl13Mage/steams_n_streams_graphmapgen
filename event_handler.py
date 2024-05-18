import pygame
import pygame_gui

class EventHandler:
    def __init__(self, graph_manager, ui_drawing, manager, node_count_entry):
        self.graph_manager = graph_manager
        self.ui_drawing = ui_drawing
        self.dragging = False
        self.selected_node = None
        self.panning = False
        self.last_mouse_pos = (0, 0)

        self.manager = manager
        self.node_count_entry = node_count_entry

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                print('Text entry finished')
                if event.ui_element == self.node_count_entry:
                    print('Node count:', self.node_count_entry.get_text())
                    self.graph_manager.num_nodes = int(self.node_count_entry.get_text())
                    self.graph_manager.points, self.graph_manager.edges = self.graph_manager.generate_graph()
                #elif event.ui_element == self.max_distance_entry:
                #    print('Max distance:', self.max_distance_entry.get_text())
                #    max_distance = int(self.max_distance_entry.get_text())
                #    #self.graph_manager.add_edges_based_on_distance(max_distance)
                #    #self.graph_manager.create

        self.manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.last_mouse_pos = event.pos
                self.selected_node = self.get_node_at_pos(event.pos)
                if not self.selected_node:
                    self.panning = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.dragging = False
                self.panning = False
                self.selected_node = None

        elif event.type == pygame.MOUSEMOTION:
            if self.panning:
                dx, dy = event.pos[0] - self.last_mouse_pos[0], event.pos[1] - self.last_mouse_pos[1]
                self.ui_drawing.offset_x += dx
                self.ui_drawing.offset_y += dy
                self.last_mouse_pos = event.pos
            elif self.selected_node is not None and self.dragging:
                new_pos = ((event.pos[0] - self.ui_drawing.offset_x) / self.ui_drawing.zoom_level, (event.pos[1] - self.ui_drawing.offset_y) / self.ui_drawing.zoom_level)
                self.graph_manager.points[self.selected_node] = new_pos

        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            self.ui_drawing.handle_zoom(event.y, mouse_pos)

    def get_node_at_pos(self, pos):
        for key, point in enumerate(self.graph_manager.points):
            node_screen_pos = (point[0] * self.ui_drawing.zoom_level + self.ui_drawing.offset_x, point[1] * self.ui_drawing.zoom_level + self.ui_drawing.offset_y)
            if (pos[0] - node_screen_pos[0])**2 + (pos[1] - node_screen_pos[1])**2 < (10 * self.ui_drawing.zoom_level)**2:
                self.dragging = True
                return key
        return None
