# The Boid class file
# Resources:
#   Draw lines:   https://stackoverflow.com/questions/10354638/pygame-draw-single-pixel

import pygame
import numpy as np
from math import sin, cos
from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale
import math

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
        self.prev_coords = [[self.x, self.y]]
        self.trail_limit = 4
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location
        self.vel = 10            # How fast the player moves - hypotenuse
        self.vis_dist = 75      # How far can boid see
        self.vis_angle = 150    # Vision of +150 or -150 degrees
        self.rotate_degree = 1  # Can rotate 5 degrees per move
        self.true_angle = 0     # Facing directly up at first
        self.orginal_angle = 0
        self.fut_x, self.fut_y = self.get_coords(self.vel, 0)         # Future direction coordinates
        self.personal_space = int(self.vis_dist*.40)    # Personal boid bubble
        self.sprites = self.make_my_sprites(['images/fish1.png', 'images/fish2.png', 'images/fish3.png', 'images/fish2.png'], '#00FF31')

    def make_my_sprites(self, sprite_images, color_tint):

        my_sprites = []
        for image in sprite_images:
            my_png = self.image_tint(image, color_tint)
            png_mode = my_png.mode
            png_size = my_png.size
            png_data = my_png.tobytes()
            my_sprites.append(pygame.image.fromstring(png_data, png_size,
                                                      png_mode).convert_alpha())  # Convert alpha makes it run faster?
        return my_sprites

        # Borrowed from stack - may make this a more general function...

    def image_tint(self, src, tint='#ffffff'):
        src = Image.open(src)

        tr, tg, tb = getrgb(tint)
        tl = getcolor(tint, "L")  # tint color's overall luminosity
        if not tl: tl = 1  # avoid division by zero
        tl = float(tl)  # compute luminosity preserving tint factors
        sr, sg, sb = map(lambda tv: tv / tl, (tr, tg, tb))  # per component adjustments

        # create look-up tables to map luminosity to adjusted tint
        # (using floating-point math only to compute table)
        luts = (list(map(lambda lr: int(lr * sr + 0.5), range(256))) +
                list(map(lambda lg: int(lg * sg + 0.5), range(256))) +
                list(map(lambda lb: int(lb * sb + 0.5), range(256))))
        l = grayscale(src)  # 8-bit luminosity version of whole image
        if Image.getmodebands(src.mode) < 4:
            merge_args = (src.mode, (l, l, l))  # for RGB verion of grayscale
        else:  # include copy of src image's alpha layer
            a = Image.new("L", src.size)
            a.putdata(src.getdata(3))
            merge_args = (src.mode, (l, l, l, a))  # for RGBA verion of grayscale
            luts += range(256)  # for 1:1 mapping of copied alpha values

        return Image.merge(*merge_args).point(luts)

    def get_coords(self, radius, theta):
        '''
        Remeber that the top left corner is 0,0 and the bottom right corner is screen_w, screen_h.
        :param radius:
        :param theta:
        :return:
        '''
        self.true_angle = (self.true_angle + theta) % 360                # Keep track of true angle
        y = radius * sin(self.true_angle)       # Get y coordinate
        x = radius * cos(self.true_angle)       # Get x coordinate
        return -x, -y                            # Give back flipped x, regular y and return that

    def do_move(self, game, move):
        '''
        Allow the boid to move in certain ways. ie - rotate left or right
        :param game:
        :param move:
        :return:
        '''
        #self.vel = np.random.choice((5,10))
        self.prev_coords.append([self.x, self.y])   # Add to trail

        if move == 0:       # Continue straight
            x, y = self.get_coords(self.vel, 0)

        elif move == 1:       # Rotate left
            x, y = self.get_coords(self.vel, self.rotate_degree)

        elif move == 2:     # Rotate right
            x, y = self.get_coords(self.vel, -self.rotate_degree)

        self.x += int(x)  # New x location
        self.y += int(y)  # New y location

        self.fut_x = self.x + int(x)*4  # Potential future x location
        self.fut_y = self.y + int(y)*4  # Potential future y location

        # Hit a wall, then undo the move - Angle will still remain modified
        if not game.screen_w - (self.w + self.vel) > self.x > self.vel or not self.vel < self.y < game.screen_h - (self.h + self.vel):
            #print("undo move")
            self.x -= int(x)  # Undo x location
            self.y -= int(y)  # Undo y location

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.w, self.h)

    def separation(self, other_boids):
        # Get the average distance of each of the boids from one another and try to keep them from colliding
        neighbor_count = 0
        avg_dist = 0
        neighbor_ids = []
        neighbor_dists = []

        for othr_b in other_boids:
            distance = math.sqrt(((self.x - othr_b.x) ** 2) + ((self.y - othr_b.y) ** 2))
            if 0 < distance < self.vis_dist:        # In range, get their true angle
                avg_dist += distance
                neighbor_count += 1
                neighbor_ids.append(othr_b.id)      # Get the id
                neighbor_dists.append(distance)     # Get their distance from this boid

        if neighbor_count > 0:              # At least one boid near me
            #avg_dist = int(avg_dist/neighbor_count)   # Get the average distance of the boids
            avg_dist = self.personal_space

            for i, id in enumerate(neighbor_ids):
                if neighbor_dists[i] > avg_dist:    # If greater than average distance, move towards them
                    if other_boids[id].true_angle > self.true_angle:
                        self.true_angle += self.rotate_degree       # Move towards them
                    else:
                        self.true_angle -= self.rotate_degree       # Move towards them

                else:       # Less than average distance, move away from them
                    if other_boids[id].true_angle > self.true_angle:
                        self.true_angle -= self.rotate_degree       # Move away from them
                    else:
                        self.true_angle += self.rotate_degree       # Move away from them

    def alignment(self, other_boids):
        neighbor_count = 0
        avg = 0
        # Boid will try to move in the same direction as the other boids in it's vision
        for othr_b in other_boids:
            distance = math.sqrt(((self.x - othr_b.x) ** 2) + ((self.y - othr_b.y) ** 2))
            if 0 < distance < self.vis_dist:        # In range, get their true angle
                avg += othr_b.true_angle
                neighbor_count += 1

        if neighbor_count > 0:  # At least one boid near me
            avg = int(avg/neighbor_count)                   # Get the average of the boids true angle

            if avg > self.true_angle:                       # Adjust my true angle to line up with my neighbors
                self.true_angle += self.rotate_degree
            else:
                self.true_angle -= self.rotate_degree

    def cohesion(self, other_boids):
        # Boids move towards central location of group in vision range
        positions = []
        for othr_b in other_boids:
            distance = math.sqrt(((self.x - othr_b.x) ** 2) + ((self.y - othr_b.y) ** 2))
            if 0 < distance < self.vis_dist:        # In range, get their true angle
                positions.append([othr_b.x, othr_b.y])      # Append their x and y coordinate

        if len(positions) != 0:     # Only if there are boids near me
            temp_coords = np.array(positions)
            avg_coords = np.mean(temp_coords, axis=0)   # Get average of both of these coordinates for central point

            if self.x > avg_coords[0]:     # Remember, we're flipped
                self.true_angle += self.rotate_degree       # Check this later - make sure it's rotating towards central
            else:
                self.true_angle -= self.rotate_degree

            if self.y > avg_coords[1]:
                self.true_angle += self.rotate_degree  # Check this later - make sure it's rotating towards central
            else:
                self.true_angle -= self.rotate_degree

    def draw(self, window, frames, other_boids):

        # Color
        #rand_color = (np.random.choice(255),0,np.random.choice(255))

        if len(self.prev_coords) > self.trail_limit:
            self.prev_coords.pop(0)     # Pop the oldest coord, FIFO

        for i, coords in enumerate(self.prev_coords):
            if i != len(self.prev_coords) - 1:  # Not on last index
                pygame.draw.line(window, (0, 240, 0), (coords[0], coords[1]),
                                 (self.prev_coords[i+1][0], self.prev_coords[i+1][1]), i+1)
            else:   # Last Index
                pygame.draw.line(window, (0, 255, 0), (self.x, self.y), (self.prev_coords[i][0], self.prev_coords[i][1]), i+2)

        # Where I may go next -> direction
        pygame.draw.line(window, (0, 255, 255), (self.x, self.y), (self.fut_x, self.fut_y), 1)

        # Show Range of Vision
        pygame.draw.circle(window, (0,0,255), (self.x, self.y), self.vis_dist, 1)

        # Show Personal bubble range
        pygame.draw.circle(window, (0, 0, 200), (self.x, self.y), self.personal_space, 1)

        # Show connection if in range
        for othr_b in other_boids:
            distance = math.sqrt(((self.x - othr_b.x) ** 2) + ((self.y - othr_b.y) ** 2))
            if 0 < distance < self.vis_dist:
                pygame.draw.line(window, (255, 0, 0), (self.x, self.y), (othr_b.x, othr_b.y), 1)


        # Draw a randomly collored box as a boid place holder
        #pygame.draw.rect(window, (np.random.choice(255),0,np.random.choice(255)), self.hitbox, 3)

        '''
        scaled_img = pygame.transform.scale(self.sprites[frames % len(self.sprites)], (self.w, self.h))
        rotated_img = pygame.transform.rotate(scaled_img, (self.true_angle - self.orginal_angle)/5 * 12)
        window.blit(rotated_img, (self.x, self.y))
        '''

    def active_player(self):
        keys = pygame.key.get_pressed()     # Collect the key presses from user
        move = 0                            # Initialize a move to go straight

        # Go left
        if keys[pygame.K_LEFT]:
            move = 1

        # Go Right
        elif keys[pygame.K_RIGHT]:
            move = 2

        return move     # Move from player