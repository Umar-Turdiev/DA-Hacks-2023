# Psysicks - DAHacks Project

from time import sleep

import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import pygame_gui
import threading

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

pygame.init()
pygame.display.set_caption('Pysicks')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/button_theming_test_theme.json')
clock = pygame.time.Clock()

background = pygame.Surface((800, 600))
background.fill(manager.get_theme().get_colour('dark_bg'))

scene_objects = {}


class Object:
    def __init__(self, body, poly):
        self.body = body
        self.poly = poly


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

        # self.add_box(200, 1100, 100, 3)

        ### Init pygame and create screen
        pygame.init()
        self.w, self.h = 600, 600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        ### Walls
        self.walls = []
        self.create_wall_segments([(100, 50), (500, 50)])

        ## Balls
        # balls = [createBall(space, (100,300))]
        self.balls = []

        ### Polys
        self.polys = []
        h = 10
        for y in range(1, h):
            # for x in range(1, y):
            x = 0
            s = 10
            p = Vec2d(300, 40) + Vec2d(0, y * s * 2)
            self.polys.append(self.create_box(p, size=s, mass=1))

        self.run_physics = True

        ### Wall under construction
        self.wall_points = []
        ### Poly under construction
        self.poly_points = []

        self.shape_to_remove = None
        self.mouse_contact = None

        self.create_ball((500, 500))

    def detect_click(self, x, y):
        for circle, circle_info in self.balls:
            if circle.point_query((x, 600 - y)):
                print("Circle clicked!")

    def add_box(self, x, y, width, height, mass=10):
        body = pymunk.Body()
        body.position = x, y
        poly = pymunk.Poly.create_box(body, (width, height))
        poly.mass = mass
        self.space.add(body, poly)

    def create_ball(self, point, mass=1.0, radius=15.0):
        moment = pymunk.moment_for_circle(mass, 0.0, radius)
        ball_body = pymunk.Body(mass, moment)
        ball_body.position = Vec2d(*point)

        ball_shape = pymunk.Circle(ball_body, radius)
        ball_shape.friction = 1.5
        ball_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(ball_body, ball_shape)

        return ball_shape

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

        return shape

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
            self.walls.append(wall_shape)

    def draw_ball(self, ball):
        body = ball.body
        v = body.position + ball.offset.cpvrotate(body.rotation_vector)
        p = self.flipyv(v)
        r = ball.radius
        pygame.draw.circle(self.screen, pygame.Color("blue"), p, int(r), 2)

    def draw_wall(self, wall):
        body = wall.body
        pv1 = self.flipyv(body.position + wall.a.cpvrotate(body.rotation_vector))
        pv2 = self.flipyv(body.position + wall.b.cpvrotate(body.rotation_vector))
        pygame.draw.lines(self.screen, pygame.Color("lightgray"), False, [pv1, pv2])

    def draw_poly(self, poly):
        body = poly.body
        ps = [p.rotated(body.angle) + body.position for p in poly.get_vertices()]
        ps.append(ps[0])
        ps = list(map(self.flipyv, ps))
        if u.is_clockwise(ps):
            color = pygame.Color("green")
        else:
            color = pygame.Color("red")
        pygame.draw.lines(self.screen, color, False, ps)

    def draw(self):
        ### Clear the screen
        self.screen.fill(pygame.Color("white"))

        ### Display some text
        self.draw_helptext()

        ### Draw balls
        for ball in self.balls:
            self.draw_ball(ball)

        ### Draw walls
        for wall in self.walls:
            self.draw_wall(wall)

        ### Draw polys
        for poly in self.polys:
            self.draw_poly(poly)

        ### Draw Uncompleted walls
        if len(self.wall_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.wall_points]
            pygame.draw.lines(self.screen, pygame.Color("gray"), False, ps, 2)

        ### Uncompleted poly
        if len(self.poly_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.poly_points]
            pygame.draw.lines(self.screen, pygame.Color("red"), False, ps, 2)

        ### Mouse Contact
        if self.mouse_contact is not None:
            p = self.flipyv(self.mouse_contact)
            pygame.draw.circle(self.screen, pygame.Color("red"), p, 3)

        ### All done, lets flip the display
        pygame.display.flip()

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    x, y = pygame.mouse.get_pos()
                    viewport.detect_click(x, y)

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


if __name__ == '__main__':
    main()

pygame.quit()
