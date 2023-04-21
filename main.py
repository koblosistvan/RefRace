""" Set up the track and the cars, and start the race """
import race



game = race.Race()
game.all_sprites_list.add(race.Car())
game.start()
