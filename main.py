""" Set up the track and the cars, and start the race """
import race



game = race.Race()
myferrari_car = race.Car(game)
myferrari_car.direction = 0
myferrari_car.speed = 10
game.all_sprites_list.add(myferrari_car)


game.start()
