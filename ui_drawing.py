import pygame

class UIDrawing:
    def __init__(self, screen, graph_manager, background):
        self.screen = screen
        self.background = background
        self.graph_manager = graph_manager
        self.zoom_level = 1.0
        self.offset_x, self.offset_y = 0, 0
        self.background_rect = self.background.get_rect()

    def draw_graph(self):
        # Fill screen with a black background to handle any space around the image during zoom-out
        self.screen.fill((0, 0, 0))

        # Calculate the current dimensions of the zoomed background
        current_bg_width = int(self.background_rect.width * self.zoom_level)
        current_bg_height = int(self.background_rect.height * self.zoom_level)

        scaled_background = pygame.transform.scale(self.background, (current_bg_width, current_bg_height))
        background_position = (self.offset_x, self.offset_y)

        self.screen.blit(scaled_background, background_position)

        for position in self.graph_manager.points:
            node_screen_x = int(position[0] * self.zoom_level + self.offset_x)
            node_screen_y = int(position[1] * self.zoom_level + self.offset_y)

            # show dot only when in view
            #if 0 <= node_screen_x <= self.screen.get_width() and 0 <= node_screen_y <= self.screen.get_height():
            #    pygame.draw.circle(self.screen, (102, 0, 102), (node_screen_x, node_screen_y), 10)

            # Draw nodes
            pygame.draw.circle(self.screen, (102, 0, 102), (node_screen_x, node_screen_y), 10)

        for edge in self.graph_manager.edges:
            start_pos = (int(self.graph_manager.points[edge[0]][0] * self.zoom_level + self.offset_x),
                         int(self.graph_manager.points[edge[0]][1] * self.zoom_level + self.offset_y))
            end_pos = (int(self.graph_manager.points[edge[1]][0] * self.zoom_level + self.offset_x),
                       int(self.graph_manager.points[edge[1]][1] * self.zoom_level + self.offset_y))

            # Draw the edge if both nodes are within the visible area
            #if (0 <= start_pos[0] <= self.screen.get_width() and 0 <= start_pos[1] <= self.screen.get_height() and
            #    0 <= end_pos[0] <= self.screen.get_width() and 0 <= end_pos[1] <= self.screen.get_height()):
            #    pygame.draw.line(self.screen, (102, 102, 255), start_pos, end_pos, 2)

            # Draw edges
            pygame.draw.line(self.screen, (102, 102, 255), start_pos, end_pos, 2)

        #pygame.display.flip()

    def handle_zoom(self, scroll_direction, mouse_pos):
        old_zoom_level = self.zoom_level
        zoom_factor = 1.1 if scroll_direction > 0 else 0.9  # Adjust zoom factor here to control zoom sensitivity

        new_zoom_level = self.zoom_level * zoom_factor
        new_zoom_level = max(1.0, min(new_zoom_level, 3.0))  # Constrain zoom level between 1 and 3

        # Calculate the new offsets
        self.offset_x = (self.offset_x - mouse_pos[0]) * (new_zoom_level / self.zoom_level) + mouse_pos[0]
        self.offset_y = (self.offset_y - mouse_pos[1]) * (new_zoom_level / self.zoom_level) + mouse_pos[1]

        # Apply the new zoom level and offsets
        self.zoom_level = new_zoom_level
        self.update_offset_limits()  # This method should ensure offsets do not let the image go out of visible bounds

    def update_offset_limits(self):
        """Adjust offsets to prevent the image from moving out of view."""
        self.offset_x = min(0, max(self.offset_x, self.screen.get_width() - self.background_rect.width * self.zoom_level))
        self.offset_y = min(0, max(self.offset_y, self.screen.get_height() - self.background_rect.height * self.zoom_level))