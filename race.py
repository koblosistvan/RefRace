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
    def __init__(self):
        # initialize and create screen
        pygame.init()
        self.load_track()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
                self.screen.blit(road, (x * 128, y * 128))

    def get_surface(self, x, y):
        # todo: check the track surface az specific position
        # returns the surface enumaration
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
            self.all_sprites_list.draw(self.screen)
            pygame.display.update()


class Car (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.skin = "car_black_small_1.png"
        self.pos = (100, 100)
        self.speed = 0
        self.direction = 0
        self.image = pygame.image.load(f'PNG\Cars\car_black_small_1.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=self.pos)



