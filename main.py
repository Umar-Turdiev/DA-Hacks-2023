# Psysicks - DAHacks Project
from enum import Enum
from time import sleep

import pygame
import pymunk
import pymunk.util
import pymunk.pygame_util
from pymunk import Vec2d
import pygame_gui
import threading

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

WIDTH = 1400
HEIGHT = 700

pygame.init()
pygame.display.set_caption('Pysicks')
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/themes/button_theming_test_theme.json')
clock = pygame.time.Clock()

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(manager.get_theme().get_colour('dark_bg'))

scene_objects = []


class Object:
    def __init__(self, type, body, poly):
        self.type = type
        self.body = body
        self.poly = poly

    class Type(Enum):
        BALL = 1
        POLY = 2
        WALL = 3


class Viewport:
    def __init__(self):
        self.running = False
        self.thread = None

        self.space = pymunk.Space()  # Create a Space which contain the simulation
        self.space.gravity = 0, -981

        self.clock = pygame.time.Clock()

        ### Walls
        self.walls = []
        self.create_wall_segments([(100, 50), (500, 50)])

        ## Balls
        # balls = [createBall(space, (100,300))]
        self.balls = []

        ### Polys
        self.polys = []

        self.run_physics = True

        ### Wall under construction
        self.wall_points = []
        ### Poly under construction
        self.poly_points = []

        self.shape_to_remove = None
        self.mouse_contact = None

        # self.balls.append(self.create_ball((500, 500)))
        scene_objects.append(self.create_ball((500, 500)))

    def flipyv(self, v):
        return int(v.x), int(-v.y + HEIGHT)

    def create_ball(self, point, mass=1.0, radius=15.0):
        moment = pymunk.moment_for_circle(mass, 0.0, radius)
        ball_body = pymunk.Body(mass, moment)
        ball_body.position = Vec2d(*point)
        ball_body.velocity = -100, 500

        ball_shape = pymunk.Circle(ball_body, radius)
        ball_shape.friction = 1.5
        ball_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(ball_body, ball_shape)

        object = Object(Object.Type.BALL, ball_body, ball_shape)

        scene_objects.append(object)

        return object

    def create_box(self, pos, size=10, mass=5.0):
        box_points = [(-size, -size), (-size, size), (size, size), (size, -size)]

        return self.create_poly(box_points, mass=mass, pos=pos)

    def create_poly(self, points, mass=5.0, pos=(0, 0)):
        moment = pymunk.moment_for_poly(mass, points)
        # moment = 1000
        body = pymunk.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pymunk.Poly(body, points)
        shape.friction = 0.5
        shape.collision_type = COLLTYPE_DEFAULT
        body.velocity = 10, 2
        self.space.add(body, shape)

        object = Object(Object.Type.POLY, body, shape)

        scene_objects.append(object)

        return object

    def create_wall_segments(self, points):
        """Create a number of wall segments connecting the points"""
        if len(points) < 2:
            return []
        points = [Vec2d(*p) for p in points]
        for i in range(len(points) - 1):
            v1 = Vec2d(points[i].x, points[i].y)
            v2 = Vec2d(points[i + 1].x, points[i + 1].y)
            wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            wall_shape = pymunk.Segment(wall_body, v1, v2, 0.0)
            wall_shape.friction = 1.0
            wall_shape.collision_type = COLLTYPE_DEFAULT
            self.space.add(wall_body, wall_shape)

            scene_objects.append(Object(Object.Type.WALL, wall_body, wall_shape))

    def draw_ball(self, ball):
        body = ball.body
        v = body.position + ball.offset.cpvrotate(body.rotation_vector)
        p = self.flipyv(v)
        r = ball.radius
        pygame.draw.circle(background, pygame.Color("blue"), p, int(r), 2)

    def draw_wall(self, wall):
        body = wall.body
        pv1 = self.flipyv(body.position + wall.a.cpvrotate(body.rotation_vector))
        pv2 = self.flipyv(body.position + wall.b.cpvrotate(body.rotation_vector))
        pygame.draw.lines(background, pygame.Color("lightgray"), False, [pv1, pv2])

    def draw_poly(self, poly):
        body = poly.body
        ps = [p.rotated(body.angle) + body.position for p in poly.get_vertices()]
        ps.append(ps[0])
        ps = list(map(self.flipyv, ps))
        if pymunk.util.is_clockwise(ps):
            color = pygame.Color("green")
        else:
            color = pygame.Color("red")
        pygame.draw.lines(background, color, False, ps)

    def draw(self):
        # Clear the screen
        background.fill(manager.get_theme().get_colour('dark_bg'))

        for object in scene_objects:
            if object.type == Object.Type.BALL:
                self.draw_ball(object.poly)

            if object.type == Object.Type.POLY:
                self.draw_poly(object.poly)

            if object.type == Object.Type.WALL:
                self.draw_wall(object.poly)

        ### Draw Uncompleted walls
        if len(self.wall_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.wall_points]
            pygame.draw.lines(background, pygame.Color("gray"), False, ps, 2)

        ### Uncompleted poly
        if len(self.poly_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.poly_points]
            pygame.draw.lines(background, pygame.Color("red"), False, ps, 2)

        ### Mouse Contact
        if self.mouse_contact is not None:
            p = self.flipyv(self.mouse_contact)
            pygame.draw.circle(background, pygame.Color("red"), p, 3)

        ### All done, lets flip the display
        pygame.display.flip()

    def simulate(self):
        draw_options = pymunk.pygame_util.DrawOptions(background)
        # draw_options = pymunk.SpaceDebugDrawOptions()  # For easy printing

        self.space.step(0.02)

        # self.space.debug_draw(draw_options)  # Print the state of the simulation
        # self.draw()

        # while self.running:
        #     self.space.step(0.02)
        #
        #     # self.space.debug_draw(draw_options)  # Print the state of the simulation
        #     self.draw()
        #     clock.tick(50)

    def start(self):
        if not self.running:
            self.running = True
            # self.thread = threading.Thread(target=self.simulate)
            # self.thread.start()

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

    add_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(30, 30, 235, 50), manager=manager)
    add_box_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 7.5, 100, 30)),
                                                  text='Add Box',
                                                  manager=manager,
                                                  container=add_panel)
    add_ball_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 7.5, 100, 30)),
                                                   text='Add Ball',
                                                   manager=manager,
                                                   container=add_panel)

    control_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(588, 620, 235, 50), manager=manager)
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 7.5, 100, 30)),
                                                text='Start',
                                                manager=manager,
                                                container=control_panel)
    pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 7.5, 100, 30)),
                                                text='Pause',
                                                manager=manager,
                                                container=control_panel)

    restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 10), (100, 30)),
                                                  text='Restart',
                                                  manager=manager,
                                                  object_id='Restart')

    properties_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(1135, 30, 235, 310),
                                                   manager=manager)
    properties_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((70, 0, 80, 30)),
                                                   text='Properties',
                                                   manager=manager,
                                                   container=properties_panel)
    properties_panel_position = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(10, 30, 210, 105),
                                                            manager=manager,
                                                            container=properties_panel)
    position_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0, 120, 30)),
                                                 text='Position    ',
                                                 manager=manager,
                                                 container=properties_panel_position)
    x_position_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 25, 70, 30)),
                                                   text='X:',
                                                   manager=manager,
                                                   container=properties_panel_position)
    y_position_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 55, 70, 30)),
                                                   text='Y:',
                                                   manager=manager,
                                                   container=properties_panel_position)
    x_position_textentry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((50, 25, 130, 30)),
                                                              manager=manager,
                                                              container=properties_panel_position)
    y_position_textentry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((50, 55, 130, 30)),
                                                              manager=manager,
                                                              container=properties_panel_position)

    properties_panel_velocity = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(10, 145, 210, 105),
                                                            manager=manager,
                                                            container=properties_panel)
    velocity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 0, 120, 30)),
                                                 text='Velocity (m/s)',
                                                 manager=manager,
                                                 container=properties_panel_velocity)
    x_velocity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 25, 70, 30)),
                                                   text='X:',
                                                   manager=manager,
                                                   container=properties_panel_velocity)
    y_velocity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 55, 70, 30)),
                                                   text='Y:',
                                                   manager=manager,
                                                   container=properties_panel_velocity)
    x_velocity_textentry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((50, 25, 130, 30)),
                                                              manager=manager,
                                                              container=properties_panel_velocity)
    y_velocity_textentry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((50, 55, 130, 30)),
                                                              manager=manager,
                                                              container=properties_panel_velocity)

    update_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 260, 100, 30)),
                                                  text='Update',
                                                  manager=manager,
                                                  container=properties_panel)
    remove_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 260, 100, 30)),
                                                   text='Remove',
                                                   manager=manager,
                                                   container=properties_panel)
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                viewport.shutdown()
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    pass

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

                if event.ui_element == add_box_button:
                    viewport.create_box((500, 500))
                if event.ui_element == add_ball_button:
                    viewport.create_ball((500, 500))

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        if viewport.running:
            viewport.simulate()

        viewport.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()

pygame.quit()
