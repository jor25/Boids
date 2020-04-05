# Main File where program where execution happens.

import numpy as np
import pygame
import boids as bd

# Game class to manage game set up and settings
class Game:
    def __init__(self, screen_w, screen_h, num_boids):
        pygame.display.set_caption('Boids')     # Caption
        self.screen_w = screen_w                # Screen width
        self.screen_h = screen_h                # Screen height
        self.window = pygame.display.set_mode((screen_w, screen_h))  # Game window
        self.crash = False                      # When to shut down the game
        self.spawn_point = [int(screen_w/2), int(screen_h/2), 20, 20]   # [x,y,w,h]

        # Initialize Boids
        self.boids = [bd.Boid(i, self.spawn_point) for i in range(num_boids)]  # Make boids

    def run(self):
        '''
        Run the game.
        :return:
        '''
        clock = pygame.time.Clock()
        while not self.crash:                   # Keep going while the game hasn't ended.
            #clock.tick(5)                      # Frames per second
            for event in pygame.event.get():    # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    self.crash = True           # Crash will get us out of the game loop

            # Allow all boids to make a move once per frame
            for boid in self.boids:
                boid.do_move(self, np.random.choice(2))

            # Draw everything on screen once per frame
            self.draw_window()

    def draw_window(self):
        self.window.fill((0, 0, 0))  # Screen Color fill
        # Draw stuff here
        for boid in self.boids:
            boid.draw(self.window)

        pygame.display.update()


# Main Function
if __name__ == "__main__":
    print("Hello world, We're making some BOIDS")
    game = Game(800, 600, 20)
    game.run()
