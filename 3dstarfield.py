"""
 Original Starfield from 
 3D Starfield Simulation
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com
 http://twitter.com/codentronix

 Modification and Buttons from Chris Munnelly

"""
import pygame, math, Buttons
from random import randrange
from pygame.locals import *

class Simulation:
    def __init__(self, num_stars, max_depth):
        pygame.init()
        
#       self.screen = pygame.display.set_mode((640, 480), pygame.NOFRAME)    - original settings
        self.screen = pygame.display.set_mode((1200, 800), pygame.NOFRAME)
        pygame.display.set_caption("X-Wing Console")

        self.clock = pygame.time.Clock()
        self.num_stars = num_stars
        self.max_depth = max_depth
        self.mode = 1
        self.count = 0
        self.duration = 5
        self.shoot_x = [50, 100, 150, 300, 600]
        self.shoot_y = [0, 50, 100, 200, 400]
        self.init_stars()
        self.planet = [0, 0, 0]
        

    def init_stars(self):
        """ Create the starfield """
        self.stars = []
        for i in range(self.num_stars):
            # A star is represented as a list with this format: [X,Y,Z]
            star = [randrange(-25,25), randrange(-25,25), randrange(1, self.max_depth)]
            self.stars.append(star)

    def move_and_draw_stars(self):
        """ Move and draw the stars """
        origin_x = self.screen.get_width() / 2
        origin_y = self.screen.get_height() / 2
        
        for star in self.stars:
            # The Z component is decreased on each frame.
            star[2] -= 0.19

            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star[2] <= 0:
                star[0] = randrange(-25,25)
                star[1] = randrange(-25,25)
                star[2] = self.max_depth

            # Convert the 3D coordinates to 2D using perspective projection.
            k = 128.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)

            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < self.screen.get_width() and 0 <= y < self.screen.get_height():
                size = (1 - float(star[2]) / self.max_depth) * 5
                shade = (1 - float(star[2]) / self.max_depth) * 255
                self.screen.fill((shade,shade,shade),(x,y,size,size))

    def show_target_grid(self):
        """" Add targetting grid to starfield display """
        origin_x = self.screen.get_width() / 2
        origin_y = self.screen.get_height() / 2
        # Draw the center mark
        pygame.draw.lines(self.screen, (107,142,35), False, [((origin_x - 20),origin_y),((origin_x + 20),origin_y)], 2)
        pygame.draw.lines(self.screen, (107,142,35), False, [(origin_x,(origin_y - 20)),(origin_x,(origin_y + 20))], 2)
        # Draw the corner grids
        pygame.draw.lines(self.screen, (107,142,35), False, [((origin_x - 50),(origin_y + 40)),((origin_x - 50),(origin_y + 50)),((origin_x - 40),(origin_y + 50))], 2)
        pygame.draw.lines(self.screen, (107,142,35), False, [((origin_x - 50),(origin_y - 40)),((origin_x - 50),(origin_y - 50)),((origin_x - 40),(origin_y - 50))], 2)
        pygame.draw.lines(self.screen, (107,142,35), False, [((origin_x + 50),(origin_y + 40)),((origin_x + 50),(origin_y + 50)),((origin_x + 40),(origin_y + 50))], 2)
        pygame.draw.lines(self.screen, (107,142,35), False, [((origin_x + 50),(origin_y - 40)),((origin_x + 50),(origin_y - 50)),((origin_x + 40),(origin_y - 50))], 2)

    def fire_lasers(self):
        origin_x = self.screen.get_width() / 2
        origin_y = self.screen.get_height() / 2
        if self.count > 0:
             pygame.draw.lines(self.screen, (55,255,243), False, [((origin_x - self.shoot_x[self.count]),(origin_y + self.shoot_y[self.count])),((origin_x - self.shoot_x[(self.count - 1)]),(origin_y + self.shoot_y[(self.count - 1)]))], (self.count * 2))
             pygame.draw.lines(self.screen, (55,255,243), False, [((origin_x + self.shoot_x[self.count]),(origin_y + self.shoot_y[self.count])),((origin_x + self.shoot_x[(self.count - 1)]),(origin_y + self.shoot_y[(self.count - 1)]))], (self.count * 2))
             self.Button3.create_button(self.screen, (55,255,243), 10, 150, 100,    50,    0,        "FIRED", (255,255,255))
             self.duration = self.duration - 1
             if self.duration == 0:
                  self.count = self.count - 1
                  self.duration = 5
        else:
             self.Button3.create_button(self.screen, (107,142,35), 10, 150, 100,    50,    0,        "Fire Laser", (255,255,255))   
          
    def show_planet (self):
            # The Z component is decreased on each frame.
            self.planet[2] -= 0.19
            origin_x = self.screen.get_width() / 2
            origin_y = self.screen.get_height() / 2

            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if self.planet[2] <= 0:
                self.planet[0] = randrange(-25,25)
                self.planet[1] = randrange(-25,25)
                self.planet[2] = self.max_depth
 
            if self.planet[0] <= 0:
                self.planet[0] -= 10
            else:
                self.planet[0] += 10
            x = self.planet[0]
            if self.planet[1] <= 0:
                self.planet[1] -= 10
            else:
                self.planet[1] += 10
            y = self.planet[1]
          
            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < self.screen.get_width() and 0 <= y < self.screen.get_height():
                size = 300
                shade = 200
#                print ("x ", x, " y ",y," rad ",size)
                pygame.draw.circle(self.screen,(shade,shade,shade),(x,y),size,0)



    def run(self):
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        """ Main Loop """
        while 1:
            # Lock the framerate at 50 FPS.
            self.clock.tick(50)

            # Handle events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        self.mode = 1
                        print ("Show starfield!")
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        self.mode = self.mode + 1
                        if self.mode >= 3:
                             self.Button2.create_button(self.screen, (107,142,35), 10, 80, 100,    50,    0,        "Target Grid OFF", (255,255,255))
                             self.mode = 1
                        print ("Targetting systems!")
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        self.mode = 3
                        self.count = 4
                        self.duration = 5
                        print ("Fire!")

            
            self.screen.fill((0,0,0))
            if self.mode == 1:
                self.move_and_draw_stars()
                self.Button2.create_button(self.screen, (107,142,35), 10, 80, 100,    50,    0,        "Target OFF", (255,255,255))
                self.Button3.create_button(self.screen, (107,142,35), 10, 150, 100,    50,    0,        "Fire Laser", (255,255,255))
            if self.mode == 2:
                self.move_and_draw_stars()
                self.show_target_grid()
                self.Button2.create_button(self.screen, (255,0,0), 10, 80, 100,    50,    0,        "Target ON", (255,255,255))
                self.Button3.create_button(self.screen, (107,142,35), 10, 150, 100,    50,    0,        "Fire Laser", (255,255,255))
            if self.mode == 3:
                self.move_and_draw_stars()
                self.show_target_grid()
                self.Button2.create_button(self.screen, (255,0,0), 10, 80, 100,    50,    0,        "Target ON", (255,255,255))
                self.fire_lasers()
            self.show_planet()
            #Parameters:               surface,      color,       x,   y,   length, height, width,    text,     text_color    
            self.Button1.create_button(self.screen, (107,142,35), 10, 10, 100,    50,    0,        "Starview", (255,255,255))
#            self.Button2.create_button(self.screen, (107,142,35), 10, 80, 100,    50,    0,        "Target OFF", (255,255,255))
#            self.Button3.create_button(self.screen, (107,142,35), 10, 150, 100,    50,    0,        "Fire Laser", (255,255,255))
            pygame.display.flip()

if __name__ == "__main__":
    Simulation(512, 32).run()
