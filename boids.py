# The Boid class file
import pygame
import numpy as np

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
        self.vel = 5           # How fast the player moves

    def do_move(self, game, move=0):
        '''
        Allow the boid to move in certain ways.
        :param game:
        :param move:
        :return:
        '''
        move = np.random.choice(4)
        if move == 0:       # Move right
            if self.x < game.screen_w - (self.w + self.vel):    # Within right wall
                self.x += self.vel

        elif move == 1:     # Move left
            if self.x > self.vel:   # Within the left bound
                self.x -= self.vel

        elif move == 2:     # Move Up
            if self.y > self.vel:   # Within the upper bound
                self.y -= self.vel

        elif move == 3:     # Move Down
            if self.y < game.screen_h - (self.h + self.vel):    # Within right wall
                self.y += self.vel

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.w, self.h)


        pass

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
