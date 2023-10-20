from time import sleep

import pygame
import pymunk
import pygame_gui
import threading

scene_objects = {}


class Object:
    def __init__(self, shape_data):
        # Initialize object properties using shape data
        self.shape_data = shape_data


class Viewport:
    def __init__(self):
        self.running = False
        self.thread = None

    def simulate(self):
        while self.running:
            # replace this to simulate the objects from the list
            print('sim')
            sleep(0.5)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.simulate)
            self.thread.start()

    def pause(self):
        self.running = False

    def restart(self):
        self.shutdown()
        self.start()

    def shutdown(self):
        self.pause()
        self.thread.join()


def main():
    pygame.init()

    viewport = Viewport()

    pygame.display.set_caption('Button Theming Test')
    window_surface = pygame.display.set_mode((800, 600))
    manager = pygame_gui.UIManager((800, 600), 'data/themes/button_theming_test_theme.json')
    clock = pygame.time.Clock()

    background = pygame.Surface((800, 600))
    background.fill(manager.get_theme().get_colour('dark_bg'))

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                                text='Start',
                                                manager=manager,
                                                object_id='Start')
    pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 10), (100, 30)),
                                                text='Pause',
                                                manager=manager,
                                                object_id='Pause')
    restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 10), (100, 30)),
                                                  text='Restart',
                                                  manager=manager,
                                                  object_id='Restart')

    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                viewport.shutdown()
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    print('Start button pressed')
                    viewport.start()

                if event.ui_element == pause_button:
                    print('Pause button pressed')
                    viewport.pause()

                if event.ui_element == restart_button:
                    print('Restart button pressed')
                    viewport.restart()

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
