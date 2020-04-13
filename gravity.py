import pygame
import math

W_WIDTH, W_HEIGHT = 1500, 900
win = pygame.display.set_mode(
    (W_WIDTH, W_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Gravity Simulation')


class Planet():
    def __init__(self, w, x, y, dx, dy, m, move=True):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.mass = m
        self.radius = m / R_FRAC
        self.color = [255, 255, 255]
        self.win = w
        self.is_moveable = move

    def draw(self):
        pygame.draw.circle(self.win, self.color, (int(
            self.x), int(self.y)), int(self.radius))
        self.update_color()

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.draw()

    def calc_dist(self, p2):
        dist = math.dist((self.x, self.y), (p2.x, p2.y))
        return dist

    def calc_angle(self, p2):
        angle = math.atan2(p2.y-self.y, p2.x-self.x)
        return angle

    def update_vel(self, p2):
        b = 0
        if math.hypot(p2.y-self.y, p2.x-self.x) == 0:
            b = .0001
        acc = G * p2.mass / (math.hypot(p2.y-self.y, p2.x-self.x)**2+b)
        angle = self.calc_angle(p2)
        self.dx += math.cos(angle) * acc
        self.dy += math.sin(angle) * acc

    def check_colision(self, p2):
        dist = math.hypot(p2.y-self.y, p2.x-self.x)
        if dist <= self.radius+p2.radius:
            if self.mass >= p2.mass:
                self.update_mass(p2.mass)
                planets.remove(p2)
                del(p2)

            else:
                p2.update_mass(self.mass)
                planets.remove(self)
                del(self)

    def update_mass(self, dm):
        self.mass += dm
        self.radius = self.mass/R_FRAC

    def update_color(self):
        self.color = [255, 255, 255]
        to_substr = self.mass / 1000
        if to_substr >= 255:
            self.color[2] = 0
            to_substr -= 255
            if to_substr >= 255:
                self.color[1] = 0
                to_substr -= 255
                if to_substr >= 255:
                    self.color[0] = 0
                else:
                    self.color[0] -= to_substr
            else:
                self.color[1] -= to_substr
        else:
            self.color[2] -= to_substr
        if self.color[0] < 100:
            self.color = [100, 0, 0]

    def check_remove(self, position):
        dist = math.hypot(position[1]-self.y, position[0]-self.x)
        if dist <= self.radius:
            planets.remove(self)
            del(self)

    def check_lock(self, position):
        dist = math.hypot(position[1]-self.y, position[0]-self.x)
        if dist <= self.radius:
            if self.is_moveable:
                self.is_moveable = False
            else:
                self.is_moveable = True


R_FRAC = 10000  # how much radius is smaller than mass
G = .01  # Gravitational constant
sun = Planet(win, 750, 450, 0, 0, 330000, False)
planet1 = Planet(win, 700, 300, 4.5, -1.3, 10)
planet2 = Planet(win, 500, 200, 2.5, -2, 100)
planets = [sun, planet1, planet2]

run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Exit fullscreen
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            win = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

        # Removing planet
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            for pl in planets:
                pl.check_remove(pos)

        # Clear screen
        if pygame.key.get_pressed()[pygame.K_c]:
            planets.clear()

        # lock and unlock planet
        if pygame.mouse.get_pressed()[1]:
            pos = pygame.mouse.get_pos()
            for pl in planets:
                pl.check_lock(pos)

        # Adding new planet
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pl = Planet(win, pos[0], pos[1], 0, 0, 1, False)

            i = True
            while i:  # Taking size of the planet
                for e in pygame.event.get():
                    if pygame.mouse.get_pressed()[0] == 0 or pygame.mouse.get_pos() != pos:
                        i = False
                pl.update_mass(100)
                pl.draw()
                pygame.time.delay(1)
                pygame.display.update()

            j = True
            prev_pos = pygame.mouse.get_pos()
            while j:  # Taking acceleration of the planet
                for e in pygame.event.get():
                    if pygame.mouse.get_pressed()[0] == 0:
                        j = False
                pygame.draw.line(win, (0, 0, 0), pos, prev_pos)
                prev_pos = pygame.mouse.get_pos()
                pygame.draw.line(win, (255, 0, 0), pos, prev_pos)
                pygame.time.delay(1)
                pygame.display.update()

            pl.dx = (pos[0] - prev_pos[0]) / 50
            pl.dy = (pos[1] - prev_pos[1]) / 50
            pl.is_moveable = True
            planets.append(pl)

    win.fill((0, 0, 0))
    for planet in planets:
        for p in planets:
            if p == planet:
                continue
            if planet.is_moveable:
                planet.update_vel(p)
            else:
                planet.dx, planet.dy = 0, 0
            planet.check_colision(p)

        planet.move()

    pygame.display.update()

pygame.quit()
