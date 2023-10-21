from enum import Enum

import pygame
import pymunk
import pymunk.util
import pymunk.pygame_util
from pymunk import Vec2d
import pygame_gui

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

WIDTH = 1400
HEIGHT = 700

pygame.init()
pygame.display.set_caption('Pysicks')
pygame_icon = pygame.image.load('data/logo.png')
pygame.display.set_icon(pygame_icon)
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'themes/button_theming_test_theme.json')
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

        # Walls
        self.walls = []
        self.create_wall_segments([(0, 100), (1400, 100)])

        # Balls
        # balls = [createBall(space, (100,300))]
        # self.balls = []

        # Polys
        # self.polys = []

        self.run_physics = True

        # Wall under construction
        self.wall_points = []
        # Poly under construction
        self.poly_points = []

        self.shape_to_remove = None
        self.mouse_contact = None

        # self.balls.append(self.create_ball((500, 500)))
        scene_objects.append(self.create_ball((500, 500)))

    def flipyv(self, v):
        return int(v.x), int(-v.y + HEIGHT)

    def create_ball(self, point, v=(0, 0), mass=1.0, radius=15.0):
        moment = pymunk.moment_for_circle(mass, 0.0, radius)
        ball_body = pymunk.Body(mass, moment)
        ball_body.position = Vec2d(*point)
        ball_body.velocity = v

        ball_shape = pymunk.Circle(ball_body, radius)
        ball_shape.friction = 1.5
        ball_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(ball_body, ball_shape)

        object = Object(Object.Type.BALL, ball_body, ball_shape)

        scene_objects.append(object)

        return object

    def create_box(self, pos, v, size=10, mass=5.0):
        box_points = [(-size, -size), (-size, size), (size, size), (size, -size)]

        return self.create_poly(box_points, v, mass=mass, pos=pos)

    def create_poly(self, points, v=(0, 0), mass=5.0, pos=(0, 0)):
        moment = pymunk.moment_for_poly(mass, points)
        # moment = 1000
        body = pymunk.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pymunk.Poly(body, points)
        shape.friction = 0.5
        shape.collision_type = COLLTYPE_DEFAULT
        body.velocity = v
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

            # scene_objects.append(Object(Object.Type.WALL, wall_body, wall_shape))
            self.walls.append(Object(Object.Type.WALL, wall_body, wall_shape))

    def draw_ball(self, ball):
        body = ball.body
        v = body.position + ball.offset.cpvrotate(body.rotation_vector)
        p = self.flipyv(v)
        r = ball.radius
        pygame.draw.circle(background, pygame.Color("blue"), p, int(r), 5)

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

        for wall in self.walls:
            self.draw_wall(wall.poly)

        if len(self.wall_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.wall_points]
            pygame.draw.lines(background, pygame.Color("gray"), False, ps, 2)

        if len(self.poly_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.poly_points]
            pygame.draw.lines(background, pygame.Color("red"), False, ps, 2)

        if self.mouse_contact is not None:
            p = self.flipyv(self.mouse_contact)
            pygame.draw.circle(background, pygame.Color("red"), p, 3)

        pygame.display.flip()

    def simulate(self):
        self.space.step(0.01)

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

    control_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(588, 630, 235, 50), manager=manager)
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 7.5, 120, 30)),
                                                text='Play/Pause',
                                                manager=manager,
                                                container=control_panel)
    reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 7.5, 80, 30)),
                                                text='Reset',
                                                manager=manager,
                                                container=control_panel)

    properties_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(1135, 30, 235, 510),
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

    properties_panel_mass = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(10, 260, 210, 55),
                                                            manager=manager,
                                                            container=properties_panel)
    mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10, 120, 30)),
                                             text='Mass:         ',
                                             manager=manager,
                                             container=properties_panel_mass)
    mass_textentry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((60, 10, 80, 30)),
                                                        manager=manager,
                                                        container=properties_panel_mass)
    mass_unit_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((95, 10, 120, 30)),
                                                  text='kg',
                                                  manager=manager,
                                                  container=properties_panel_mass)

    properties_panel_size = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(10, 325, 210, 55),
                                                        manager=manager,
                                                        container=properties_panel)
    size_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10, 120, 30)),
                                             text='Size:         ',
                                             manager=manager,
                                             container=properties_panel_size)
    size_textentry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((60, 10, 80, 30)),
                                                        manager=manager,
                                                        container=properties_panel_size)
    size_unit_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((95, 10, 120, 30)),
                                                  text='m',
                                                  manager=manager,
                                                  container=properties_panel_size)

    x_position_textentry.set_text('300')
    y_position_textentry.set_text('105')
    x_velocity_textentry.set_text('0')
    y_velocity_textentry.set_text('0')
    mass_textentry.set_text('5')
    size_textentry.set_text('5')

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
                    if not viewport.running:
                        print('Start')
                        viewport.start()
                    else:
                        print('Pause button pressed')
                        viewport.pause()
                if event.ui_element == reset_button:
                    print('Reset button pressed')
                    scene_objects.clear()
                    viewport.space = pymunk.Space()  # Create a Space which contain the simulation
                    viewport.space.gravity = 0, -981
                    viewport.create_wall_segments([(0, 100), (1400, 100)])

                if event.ui_element == add_box_button:
                    x = float(x_position_textentry.get_text())
                    y = float(y_position_textentry.get_text())
                    vx = float(x_velocity_textentry.get_text())
                    vy = float(y_velocity_textentry.get_text())

                    viewport.create_box((x, y), (vx, vy))
                if event.ui_element == add_ball_button:
                    x = float(x_position_textentry.get_text())
                    y = float(y_position_textentry.get_text())
                    vx = float(x_velocity_textentry.get_text())
                    vy = float(y_velocity_textentry.get_text())

                    viewport.create_ball((x, y), (vx, vy))

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
