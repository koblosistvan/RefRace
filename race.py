"""
Base classes for Car Race game
"""
import pygame

# define constants
WINDOW_WIDTH = 896
WINDOW_HEIGHT = 640
TILE_SIZE = 50  # Tile width and height in pixel, image will be resized
FPS = 50  # Game refresh rate (frame per second)
SURFACE = {'a': {'name': 'asphalt', 'speed': 100},
           'd': {'name': 'dirt', 'speed': 20},
           'l': {'name': 'wheel launcher', 'speed': 70}}
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
              'bfs': 46,}


class Race:
    """ class for play a race between several cars created by different players """
    def __init__(self):
        # initialize and create screen
        pygame.init()
        self.load_track()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.show_background()
        self.clock = pygame.time.Clock()
        self.running = False

    def load_track(self):
        """
        loads the specified track data from a file
        the text file contains tile codes separated by space character
        the rows of text file will be rendered under each other
        """
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
        """ generate the background from tile png files, depending on the track description file """
        # todo: load and parse xml file
        # todo: cut images from sheet as track needs
        for y in range(self.track_height):
            for x in range(self.track_width):
                road = pygame.image.load(f'track/road_asphalt{TILE_NAMES[self.track[y][x]]:02d}.png')
                self.screen.blit(road, (x * 128, y * 128))

    def get_surface(self, x, y):
        """
        examine the surface material on a specified position
        this is used by the car control functions
        """
        # todo: check the track surface az specific position
        # returns the surface enumaration
        return 'a'

    def start(self):
        """ main game loop, start the race, and control the cars """
        self.running = True

        # game loop
        while self.running:
            self.clock.tick(FPS)

            # process event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update screen
            pygame.display.update()
