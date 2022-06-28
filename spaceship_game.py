import os
import keyboard
import random
from threading import Thread
from time import sleep

# PARAMETERS #
score = 3  # initial lives
lenght = 10  # this for the arena
width = 10

# VARIABLE DECLARATION #
runner = True
ast_x_coord = []
ast_y_coord = []


# CLASSES DECLARATION #
# it's the starship that the user moves to kill asteroids
class Spaceship:
    def __init__(self):
        self.x_coord = 0

    def move_right(self):  # moves the ship to the right
        if self.x_coord <= (width - 2):
            self.x_coord += 1

    def move_left(self):  # moves the ship to the left
        if self.x_coord >= 1:
            self.x_coord -= 1


# it's the projectile emitted by the ship. it kills asterodids
class Projectile:
    def __init__(self):
        global lenght
        self.x_coord = 0
        self.y_coord = lenght
        self.stop = False  # am i moving? and do i like pizza?

    def fire(self):  # this dictates the movement of the projectile once fired
        global lenght, spaceship, runner
        self.x_coord = spaceship.x_coord
        self.y_coord = 0  # initial position
        for _i in range(lenght + 1):  # move!
            if runner and not self.stop:  # helps for "fast" shut off
                self.y_coord += 1
                sleep(0.05)
        self.stop = False  # ah you hit it!
        self.y_coord = lenght
        # so that it is back in its neutral position once fired


# i like to be killed by spaceships
class Asteroid(object):
    def __init__(self, name):
        self.name = name  # so there can be many of mee!
        self.x_coord = width
        self.y_coord = lenght - 1
        self.life = True  # am i alive? and do i like pizza?

    def go(self):  # this dictates how the asteroid moves
        global ast_x_coord, ast_y_coord, score, projectile, runner
        self.x_coord = random.randint(0, width - 1)
        self.y_coord = lenght
        for i in range(lenght + 1):
            if runner:  # so the programm shuts off rapidly
                if (self.life):
                    # so that we do not get errors once the asteroid is killed
                    self.y_coord -= 1
                    if self.y_coord == 0:
                        score -= 1  # if at the end, we lose on score
                    try:  # its coordinates may not be in the lists
                        ast_x_coord.pop(self.name)
                        ast_y_coord.pop(self.name)
                    except:
                        pass
                    finally:
                        ast_y_coord.insert(self.name, self.y_coord)
                        ast_x_coord.insert(self.name, self.x_coord)
                        # add or add back the coordinates
                    for i in range(29):
                        # 30 small delays to check often because of thread
                        if (self.y_coord == projectile.y_coord and
                            self.x_coord == projectile.x_coord
                        ):  # checks for collisions projectile - asteroid
                            ast_x_coord.pop(self.name)
                            ast_y_coord.pop(self.name)
                            # asteroid have saved them already at least once
                            ast_y_coord.insert(self.name, lenght)
                            ast_x_coord.insert(self.name, width)
                            # getting rid of the shadow remaining on screen
                            projectile.stop = (True)
                            # signaling to the projectile to stop
                            self.life = False  # you die!
                            break  # exit the loop for no delay
                        sleep(0.01)
                elif not self.life:
                    del self  # we do not want a ton of objects laying around
                    break


spaceship = Spaceship()  # the ship is being built
projectile = Projectile()  # the projectile is alive


# FUNCTIONS #
def manager():  # this manages base functions
    global score, ast_y_coord, runner
    while runner:  # so we can shut it off
        sleep(0.005)  # refresh rate
        refresh_display()
        if score <= 0:  # in case we lost
            stop()


def refresh_display():  # refreshes the frame
    global projectile, spaceship, score, lenght, width, runner
    if runner:  # so we can shut it off rapidly
        os.system('cls')  # blank paper sheet
        print('you have to kill all the asteroids')  # instructions
        print('if you fail 3 times, your game is over\n')
        print('to allign the ship with the asteroid use right/left arrow')
        print('fire with "f". if you want to quit use "q"\n')
        print('you can only fire when the past projectile has disappeared')
        print(f'>>> ONLY {int(score)} HITS LEFT <<<')  # score line
        frame = ''  # temporary variable
        for y in range(lenght):
            # we build the screen by coordinates, assigning the right item
            for x in range(width):
                try:
                    if x == ast_x_coord[ast_y_coord.index(y)]:
                        frame += ' ●'
                    elif (y, x) == (0, spaceship.x_coord):
                        frame += ' Ħ'
                    elif (y, x) == (projectile.y_coord, projectile.x_coord):
                        frame += ' ⁞'
                    elif (y-1, x) == (projectile.y_coord, projectile.x_coord):
                        frame += ' ˘'
                    else:
                        frame += '  '
                except:
                    if (y, x) == (0, spaceship.x_coord):
                        frame += ' Ħ'
                    elif (y, x) == (projectile.y_coord, projectile.x_coord):
                        frame += ' ⁞'
                    elif (y-1, x) == (projectile.y_coord, projectile.x_coord):
                        frame += ' ˘'
                    else:
                        frame += '  '
            frame += '|\n'  # so we can move to the next row
        print(frame)


def asteroid_generator():  # generates asteroid at random intervals
    id_name = 0
    global runner
    while runner:  # so everything shuts when we want
        asteroid = Asteroid(id_name)
        # new pizza-eater i.e. astroid with name 'id_name'
        ast_go = Thread(target=asteroid.go)  # its own thread of movement
        ast_go.start()
        sleep(random.uniform(1, 2.5))  # time before the next spawns
        id_name += 1  # change the name of the next


def fire():  # fires the projectile if possible
    global lenght, life
    if projectile.y_coord == lenght:
        # which means 'neutral state'. i.e not fired
        proj_fire = Thread(target=projectile.fire)  # fires the projectile
        proj_fire.start()  # in its own thread


def stop():  # ends the programm
    global runner  # shut it off
    runner = False
    os.system('cls')
    print('goodbye')


# SPACESHIP CONTROL #
keyboard.add_hotkey('right', spaceship.move_right)
keyboard.add_hotkey('left', spaceship.move_left)
keyboard.add_hotkey('f', fire)

# GAME CONTROLS #
keyboard.add_hotkey('q', stop)


# MANAGER #
# starts manager and asteroid generator
manager = Thread(target=manager)
manager.start()
sleep(5)  # you have to read instructions at the start
ast_generator = Thread(target=asteroid_generator)
ast_generator.start()
