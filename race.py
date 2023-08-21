import numpy
import pygame
from numpy import array
import math

# define constants
WINDOW_WIDTH = 896
WINDOW_HEIGHT = 640
TILE_SIZE = 50  # Tile width and height in pixel, image will be resized
FPS = 50  # Game refresh rate (frame per second)
SURFACE = {'a': {'name': 'asphalt', 'speed': 10},
           'd': {'name': 'dirt', 'speed': 5},
           'l': {'name': 'wheel launcher', 'speed': 7},
           'g': {'name': 'grass', 'speed': 2}}

COLOR_SURFACE = {'(166, 201, 203, 255)': 'a',
                 '(156, 192, 194, 255)': 'a',
                 '(238, 238, 238, 255)': 'l',
                 '(250, 250, 250, 255)': 'l',
                 '(39, 174, 96, 255)': 'g',
                 '(219, 98, 18, 255)': 'l',
                 '(163, 198, 200, 255)': 'a',
                 '(232, 106, 23, 255)': 'l',
                 '(39, 176, 97, 255)': 'g',
                 '(40, 178, 99, 255)': 'g',
                 '(43, 183, 102, 255)': 'g',
                 '(42, 181, 100, 255)': 'g',
                 '(41, 179, 99, 255)': 'g',
                 '(40, 177, 98, 255)': 'g',
                 '(39, 175, 97, 255)': 'g',
                 '(41, 178, 99, 255)': 'g'
                 }

TILE_NAMES = {'f-o': 4,
              'bfi': 6,
              'jfi': 7,
              'fff': 11,
              'b-o': 21,
              'j-o': 23,
              'bli': 24,
              'jli': 25,
              'jls': 27,
              'bls': 28,
              'l-o': 40,
              'jfs': 45,
              'bfs': 46, }


class Race:
    def __init__(self):
        # initialize and create screen
        pygame.init()
        self.load_track()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.show_background()
        self.clock = pygame.time.Clock()
        self.all_sprites_list = pygame.sprite.Group()

    def load_track(self):
        # Create the track
        # todo: read from file
        # todo: create a code table
        self.track = [['bfi', 'f-o', 'f-o', 'f-o', 'f-o', 'f-o', 'jfi'],
                      ['b-o', 'jls', 'l-o', 'l-o', 'l-o', 'bls', 'j-o'],
                      ['b-o', 'j-o', 'fff', 'fff', 'fff', 'b-o', 'j-o'],
                      ['b-o', 'jfs', 'f-o', 'f-o', 'f-o', 'bfs', 'j-o'],
                      ['bli', 'l-o', 'l-o', 'l-o', 'l-o', 'l-o', 'jli']]

        self.track_width = len(self.track[0])
        self.track_height = len(self.track)

    def show_background(self):
        # todo: load and parse xml file
        # todo: cut images from sheet as track needs
        for y in range(self.track_height):
            for x in range(self.track_width):
                road = pygame.image.load(f'track/road_asphalt{TILE_NAMES[self.track[y][x]]:02d}.png')
                self.background.blit(road, (x * 128, y * 128))

    def get_surface(self, pos):
        # todo: check the track surface az specific position
        # returns the surface enumaration
        color = self.background.get_at((int(pos[0]), int(pos[1])))
        if color[0]+color[1]+color[2] > 600:
            return "l"
        elif color[0]/color[1] > 1.1:
            return "l"
        elif color[1]/color[2] > 1.1:
            return 'g'
        else:
            return 'a'


    def start(self):
        self.running = True

        # game loop
        while self.running:
            self.clock.tick(FPS)

            # process event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update screen
            self.all_sprites_list.update()
            self.screen.blit(self.background, (0, 0))
            self.all_sprites_list.draw(self.screen)
            pygame.display.update()


class Car (pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.skin = "car_black_small_1.png"
        self.pos = numpy.array([100.0, 100.0])
        self.speed = 10
        self.direction = 10
        self.image = pygame.image.load(f'PNG\Cars\car_black_small_1.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=self.pos)
        self.orig_image = self.image
        self.game = game
        self.apex = 0
        self.apex_close = False


    def speed_vector(self):
        return numpy.array([self.speed * math.cos(math.radians(self.direction)),
                            self.speed * math.sin(math.radians(self.direction))])

    def update(self):
        self.control()
        self.pos += self.speed_vector()
        #self.direction += 1
        self.image = pygame.transform.rotate(self.orig_image, -self.direction)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=self.pos)
        self.game.get_surface(self.pos)
        max_speed = SURFACE[self.game.get_surface(self.pos)]["speed"]
        if self.speed > max_speed:

            self.speed = max_speed
        print(self.pos)

    def control(self):
        MAX_BREAK = 2
        MAX_ACCELARATION = 0.5
        apexes = [{"name": 't1', "pos": (600, 100), "dist": 50, "target_speed": 5, "angle": 2, "target_direction": 90},
                  {"name": 't2', "pos": (600, 500), "dist": 50, "target_speed": 5, "angle": 2, "target_direction": 180},
                  {"name": 't3', "pos": (100, 500), "dist": 50, "target_speed": 5, "angle": 2, "target_direction": 270},
                  {"name": 't4', "pos": (100, 100), "dist": 50, "target_speed": 5, "angle": 2, "target_direction": 0}]
        apex = apexes[self.apex]

        # set car direction
        distance = ((apex["pos"][1]-self.pos[1])**2 + (apex["pos"][0]-self.pos[0])**2)**0.5
        if distance > apex["dist"] and not self.apex_close:
            alpha = math.degrees(math.acos(
                (apex["pos"][0] - self.pos[0]) / distance))
            if apex["pos"][1] > self.pos[1]:
                target_dir = alpha
            else:
                target_dir = -alpha
        elif distance > apex["dist"] and self.apex_close:
            self.apex_close = False
            self.apex = (self.apex + 1) % len(apexes)
            target_dir = apex["target_direction"]
        else:
            target_dir = apex["target_direction"]
            self.apex_close = True

        if abs(self.direction-apex["target_direction"]) < apex["angle"]:
            self.direction = target_dir
        elif self.direction != target_dir:
            self.direction += (target_dir - self.direction) / (abs(target_dir - self.direction)) * apex["angle"]
        else:
            pass

        if self.direction == apex["target_direction"] and distance < apex["dist"]:
            self.apex = (self.apex + 1) % len(apexes)

        # set car speed
        if self.speed > apex["target_speed"]:
            self.speed -= MAX_BREAK
        elif self.speed > apex["target_speed"]:
            self.speed += MAX_ACCELARATION
            # TODO: NE ENGEDD TÚLFUTNI
# TODO: gumikopás, tapadás, eső, leszorítóerő, aszfalthőm, gumihőm, gumi felületének minősége, motor maximum hőmérséklet, üzemanyag szint, üzemanyag minőség,súly










