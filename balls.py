import pygame

W_WIDTH, W_HEIGHT = 800, 800
win = pygame.display.set_mode((W_WIDTH, W_HEIGHT))


class Planet():
    def __init__(self, w, x, y, dx, dy, m, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.mass = m
        self.radius = m / 100
        self.color = color
        self.win = w

    def draw(self):
        pygame.draw.circle(self.win, self.color, (int(
            self.x), int(self.y)), int(self.radius))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()


planet1 = Planet(win, 400, 400, 1, 5, 2000)
planet2 = Planet(win, 400, 400, -2, 1, 2000)
planet3 = Planet(win, 400, 400, 0, -5, 2000)
planets = [planet1, planet2, planet3]

GRAVITY = .2

run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((0, 0, 0))
    for planet in planets:
        planet.dy += GRAVITY

        if planet.x >= W_WIDTH or planet.x <= 0:
            planet.dx *= -.9
        if planet.y + 20 >= W_HEIGHT or planet.y - 20 <= 0:
            planet.dy *= -.9

        planet.move(planet.dx, planet.dy)

    pygame.display.update()

pygame.quit()
