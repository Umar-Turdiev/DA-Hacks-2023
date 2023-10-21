# Psysicks - DAHacks Project

from time import sleep

import pygame
import pymunk
import pymunk.pygame_util
import pygame_gui
import threading

pygame.init()
pygame.display.set_caption('Button Theming Test')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/button_theming_test_theme.json')
clock = pygame.time.Clock()

background = pygame.Surface((800, 600))
background.fill(manager.get_theme().get_colour('dark_bg'))

scene_objects = {}


class Object:
    def __init__(self, shape_data):
        pass


class Viewport:
    def __init__(self):
        self.running = False
        self.thread = None

        self.space = pymunk.Space()  # Create a Space which contain the simulation
        self.space.gravity = 0, -981

        self.body = pymunk.Body()  # Create a Body
        self.body.position = 50, 100  # Set the position of the body

        self.poly = pymunk.Poly.create_box(self.body)  # Create a box shape and attach to body
        self.poly.mass = 10  # Set the mass on the shape
        self.space.add(self.body, self.poly)

    def simulate(self):
        draw_options = pymunk.pygame_util.DrawOptions(background)
        # draw_options = pymunk.SpaceDebugDrawOptions()  # For easy printing

        while self.running:
            self.space.step(0.02)

            background.fill(manager.get_theme().get_colour('dark_bg'))
            self.space.debug_draw(draw_options)  # Print the state of the simulation

            sleep((1000.0 / 60) / 1000)

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
    viewport = Viewport()

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
