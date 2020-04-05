# The Boid class file
import pygame
import numpy as np
from math import sin, cos

class Boid:
    def __init__(self, id, coords):
        '''
        Initialize the boid to an initial location with a specific size and id value.
        :param id: Boid identification integer.
        :param coords: list of integers in the format of [x,y,w,h]
        '''
        print("This is boid[{}]".format(id))
        self.id = id        # Player's ID number
        self.x, self.y, self.w, self.h = coords         # Initalize coords
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location
        self.vel = 5            # How fast the player moves - hypotenuse
        self.vis_dist = 10      # How far can boid see
        self.vis_angle = 150    # Vision of +150 or -150 degrees
        self.rotate_degree = 1  # Can rotate 5 degrees per move
        self.true_angle = 90    # Facing directly up at first

    def get_coords(self, radius, theta):
        '''
        Remeber that the top left corner is 0,0 and the bottom right corner is screen_w, screen_h.
        :param radius:
        :param theta:
        :return:
        '''
        self.true_angle += theta                # Keep track of true angle
        y = radius * sin(self.true_angle)       # Get y coordinate
        x = radius * cos(self.true_angle)       # Get x coordinate
        return -x, y                            # Give back flipped x, regular y and return that

    def do_move(self, game, move):
        '''
        Allow the boid to move in certain ways. ie - rotate left or right
        :param game:
        :param move:
        :return:
        '''

        if move == 0:       # Rotate left
            x, y = self.get_coords(self.vel, self.rotate_degree)

        elif move == 1:     # Rotate right
            x, y = self.get_coords(self.vel, -self.rotate_degree)

        self.x += int(x)  # New x location
        self.y += int(y)  # New y location

        # Hit a wall, then undo the move - Angle will still remain modified
        if not game.screen_w - (self.w + self.vel) > self.x > self.vel or not self.vel < self.y < game.screen_h - (self.h + self.vel):
            #print("undo move")
            self.x -= int(x)  # Undo x location
            self.y -= int(y)  # Undo y location

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.w, self.h)

    def separation(self):
        pass

    def alignment(self):
        pass

    def cohesion(self):
        pass

    def draw(self, window):
        # Draw a randomly collored box as a boid place holder
        pygame.draw.rect(window, (np.random.choice(255),0,np.random.choice(255)), self.hitbox, 3)
        pass
