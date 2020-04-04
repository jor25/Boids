# Main File where program where execution happens.

import numpy
import pygame
import boids as bd

# Main Function
if __name__ == "__main__":
    print("Hello world, We're making some BOIDS")
    boids = [bd.boid() for x in range(5)]       # Make 5 boids