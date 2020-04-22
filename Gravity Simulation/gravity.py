import math
import pickle
import pygame

pygame.init()
win = pygame.display.set_mode((1500, 900))
W_WIDTH, W_HEIGHT = win.get_size()
pygame.display.set_caption('Gravity Simulation')
pygame.display.set_icon(pygame.image.load('data/space_logo-sm.png'))
pygame.font.init()
FONT = pygame.font.SysFont("arial", 34)


class Planet():
    def __init__(self, x, y, dx, dy, m, move=True):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.mass = m
        self.radius = m / R_FRAC
        self.color = [255, 255, 255]
        self.is_moveable = move

    def draw(self):
        pygame.draw.circle(win, self.color, (int(
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
            self.is_moveable = not self.is_moveable


class Menu():
    def __init__(self, bg_color=(0, 0, 0)):
        self.width = W_WIDTH
        self.height = W_HEIGHT
        self.bg_color = bg_color
        self.widgets = []
        self.run = True

    def draw(self):
        self.width, self.height = W_WIDTH, W_HEIGHT
        pygame.draw.rect(win, self.bg_color, pygame.Rect(
            0, 0, self.width, self.height))
        for wg in self.widgets:
            wg.draw()

    def add(self, obj):
        self.widgets += obj

    def remove(self, obj):
        self.widgets.pop(obj)

    def clear(self):
        self.widgets = []

    def open_menu(self):
        self.run = True
        while self.run:
            pygame.time.delay(10)
            self.draw()
            pygame.display.update()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.close()
                    pygame.quit()
                    exit()

                if self.run and pygame.key.get_pressed()[pygame.K_m]:
                    self.close()

                if ev.type == pygame.MOUSEBUTTONUP:
                    pt = pygame.mouse.get_pos()
                    for wdg in self.widgets:
                        if not isinstance(wdg, Text):
                            wdg.on_click(pt, ev.button)

    def close(self):
        self.run = False

    def change_res(self, res):
        global W_WIDTH, W_HEIGHT, win
        if res == "full":
            W_WIDTH, W_HEIGHT = pygame.display.list_modes()[0]
            win = pygame.display.set_mode(
                (W_WIDTH, W_HEIGHT), pygame.FULLSCREEN)
        elif res == "1500x900":
            W_WIDTH, W_HEIGHT = 1500, 900
            win = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        elif res == "800x800":
            W_WIDTH, W_HEIGHT = 800, 800
            win = pygame.display.set_mode((W_WIDTH, W_HEIGHT))


class Button():
    def __init__(self, x, y, w, h, font_color, text, on_click, param):
        self.x = x
        self.temp_x = x
        self.center = 0
        self.y = y
        self.temp_y = y
        self.width = w
        self.height = h
        self.font_color = font_color
        self.text = text
        self.function = on_click
        self.param = param
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_active = False

    def draw(self):
        text_surf = FONT.render(self.text, True, self.font_color)
        t_width, t_height = FONT.size(self.text)

        if W_WIDTH == 800 and self.text == "800x800":
            self.temp_x, self.temp_y = 300, 200
            self.rect = pygame.Rect(
                self.temp_x, self.temp_y, self.width, self.height)
            win.blit(text_surf, (round(self.temp_x+self.width/2-t_width/2),
                                 round(self.temp_y+self.height/2-t_height/2)))
        else:
            if self.x == -1 or self.center == 1:  # center horizontaly
                self.center = 1
                self.x = round(W_WIDTH/2 - self.width/2)
            elif self.x == -2 or self.center == 2:  # center horizontaly on the left half
                self.center = 2
                self.x = round(W_WIDTH/4 - self.width/2)
            elif self.x == -3 or self.center == 3:  # center horizontaly on the right half
                self.center = 3
                self.x = round(W_WIDTH*3/4 - self.width/2)
            self.rect = pygame.Rect(
                self.x, self.y, self.width, self.height)
            win.blit(text_surf, (round(self.x+self.width/2-t_width/2),
                                 round(self.y+self.height/2-t_height/2)))

        pygame.draw.rect(win, self.font_color, self.rect, 3)

    def on_click(self, point, button):
        if self.rect.collidepoint(point) and button == 1:
            if self.text == "ADD":
                if text_inp_preset.text != "Click to add preset name" and text_inp_preset.text:
                    save_preset(text_inp_preset.text, planets)
                    add_preset_menu.close()

            elif self.param:
                self.function(self.param)
            else:
                self.function()


class Text():
    def __init__(self, x, y, text, font_size, font_color=(255, 255, 255), long=False):
        self.x = x
        self.center = 0
        self.y = y
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.SysFont("arial", font_size)
        self.text = text
        self.width, self.height = self.font.size(self.text)
        self.long = long

    def draw(self):
        if self.long:
            lines = self.text.split("|")
            y = self.y
            for line in lines:
                text_surf = self.font.render(line, True, self.font_color)
                win.blit(text_surf, (self.x, y))
                y += 40
        else:
            if self.x == -1 or self.center == 1:  # center horizontaly
                self.center = 1
                self.x = round(W_WIDTH/2 - self.width/2)
            elif self.x == -2 or self.center == 2:  # center horizontaly on the left half
                self.center = 2
                self.x = round(W_WIDTH/4 - self.width/2)
            elif self.x == -3 or self.center == 3:  # center horizontaly on the right half
                self.center = 3
                self.x = round(W_WIDTH*3/4 - self.width/2)

            text_surf = self.font.render(self.text, True, self.font_color)
            win.blit(text_surf, (self.x, self.y))

        # ------- Presets ---------


class Text_inp(Button):
    def on_click(self, point, button):
        if self.rect.collidepoint(point) and button == 1:
            self.text = ""
            self.is_active = not self.is_active

    def draw(self):
        text_surf = FONT.render(self.text, True, self.font_color)
        t_width, t_height = FONT.size(self.text)
        if self.x == -1 or self.center == 1:  # center horizontaly
            self.center = 1
            self.x = round(W_WIDTH/2 - self.width/2)

        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height)
        win.blit(text_surf, (round(self.x+self.width/2-t_width/2),
                             round(self.y+self.height/2-t_height/2)))

        if self.is_active:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_BACKSPACE and len(self.text) > 0:
                        self.text = self.text[:-1]
                    else:
                        self.text += ev.unicode

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.is_active = False

        pygame.draw.rect(win, self.font_color, self.rect, 3)


class Button_pre(Button):
    def on_click(self, point, button):
        global planets
        if button == 1 and self.rect.collidepoint(point):
            planets = load_preset(self.text)
            presets_menu.close()
            main_menu.close()
        elif button == 3 and self.rect.collidepoint(point):
            delete_preset(self.text)

    def draw(self):
        text_surf = FONT.render(self.text, True, self.font_color)
        t_width, t_height = FONT.size(self.text)
        if self.x == -1 or self.center == 1:  # center horizontaly
            self.center = 1
            self.x = round(W_WIDTH/2 - self.width/2)

        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height)
        win.blit(text_surf, (round(self.x+self.width/2-t_width/2),
                             round(self.y+self.height/2-t_height/2)))
        pygame.draw.rect(win, self.font_color, self.rect, 3)

# --------------- Pickle functions -----------------


def save_preset(name, arr):
    try:
        presets = pickle.load(open("data/presets.p", "rb"))
    except EOFError:
        presets = {}
    presets[name] = arr
    pickle.dump(presets, open("data/presets.p", "wb"))
    update_presets()


def load_preset(name):
    presets = pickle.load(open("data/presets.p", "rb"))
    update_presets()
    return presets[name]


def delete_preset(name):
    presets = pickle.load(open("data/presets.p", "rb"))
    del(presets[name])
    pickle.dump(presets, open("data/presets.p", "wb"))
    update_presets()


def update_presets():
    presets_menu.clear()
    presets = pickle.load(open("data/presets.p", "rb"))
    for k, n in zip(presets.keys(), range(len(presets.keys()))):
        y = n*150 + 50
        button_preset = Button_pre(-1, y, 600, 100, (0, 0, 200), k, None, None)
        presets_menu.add([button_preset])
    presets_menu.add([Button(-1, 650, 200, 100, (0, 200, 0),
                             "OK", presets_menu.close, None)])
# --------------------------------------------------


R_FRAC = 10000  # how much radius is smaller than mass
G = .01  # Gravitational constant
sun = Planet(750, 450, 0, 0, 330000, False)
planet1 = Planet(700, 300, 4.5, -1.3, 10)
planet2 = Planet(500, 200, 2.5, -2, 100)
planets1 = [sun, planet1, planet2]
#save_preset("preset_1", planets1)
# --------------------------------

# ------ MENU ---------------------
main_menu = Menu()
settings_menu = Menu()
presets_menu = Menu()
add_preset_menu = Menu()
tutorial_menu = Menu()

# main menu
button_quit = Button(-2, 650, 200, 100, (150, 0, 0), "QUIT", pygame.quit, None)
button_ok = Button(-3, 650, 200, 100, (0, 200, 0),
                   "OK", main_menu.close, None)
button_presets = Button(-1, 100, 400, 100, (0, 0, 200),
                        "PRESETS", presets_menu.open_menu, None)
button_options = Button(-1, 250, 400, 100, (0, 0, 200),
                        "OPTIONS", settings_menu.open_menu, None)
button_tutorial = Button(-1, 400, 400, 100, (0, 0, 200),
                         "TUTORIAL", tutorial_menu.open_menu, None)
main_menu.add([button_quit, button_ok, button_presets,
               button_options, button_tutorial])

# settings menu
button_ok_sett = Button(-1, 650, 200, 100, (0, 200, 0),
                        "OK", settings_menu.close, None)
text_res = Text(100, 100, "Resolution: ", 42)
button_fullscreen = Button(
    300, 80, 200, 100, (0, 0, 200), "FULLSCREEN", settings_menu.change_res, "full")
button_1500x900 = Button(
    550, 80, 150, 100, (0, 0, 200), "1500x900", settings_menu.change_res, "1500x900")
button_800x800 = Button(
    750, 80, 150, 100, (0, 0, 200), "800x800", settings_menu.change_res, "800x800")

settings_menu.add([button_ok_sett, text_res, button_fullscreen,
                   button_1500x900, button_800x800])

# tutorial menu
text_title_tut = Text(-1, 30, "Tutorial", 64, (0, 0, 220))
text_desc_tut = Text(60, 130, "To add a new planet to the system simply click and hold LMB. |The longer you hold the more mass it will gain. |One you happy with the resoult move your cursor(without releasing LMB). |Now you can give it some initial velocity. |A red line connecting the planet and your cursor will appear. |Longer line means more velocity. |That's it. Enjoy. ||Usefull keyboard shortcuts:", 28, (255, 255, 255), True)
text_shts_tut = Text(
    60, 500, "LMB - new planet. RMB - lock/unlock a planet. MMB - delete a planet. |c - clear screen. z - delete most recent planet. m - open menu. |s - save to presets. RMB - delete preset(presets menu)", 28, (100, 255, 100), True)
button_ok_tut = Button(-1, 650, 200, 100, (0, 200, 0),
                       "OK", tutorial_menu.close, None)

tutorial_menu.add([text_title_tut, text_desc_tut,
                   text_shts_tut, button_ok_tut])

# presets menu


# add preset menu
text_inp_preset = Text_inp(-1, 300, 600, 150, (0, 0, 200),
                           "Click to add preset name", None, None)
button_add_preset = Button(-3, 650, 200, 100, (0, 200, 0),
                           "ADD", save_preset, text_inp_preset.text)
button_cancel_preset = Button(-2, 650, 200, 100,
                              (200, 0, 0), "CANCEL", add_preset_menu.close, None)

add_preset_menu.add([text_inp_preset, button_cancel_preset, button_add_preset])
# --------------------------------
try:
    planets = load_preset("preset1")
except KeyError:
    planets = []
main_menu.open_menu()
run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()

        # Open main menu
        if pygame.key.get_pressed()[pygame.K_m]:
            main_menu.open_menu()

        # Exit fullscreen
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            win = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

        # Save preset
        if pygame.key.get_pressed()[pygame.K_s]:
            add_preset_menu.open_menu()

        # Removing planet
        if pygame.mouse.get_pressed()[1]:
            pos = pygame.mouse.get_pos()
            for pl in planets:
                pl.check_remove(pos)

        # Remove most recently added planet
        if pygame.key.get_pressed()[pygame.K_z]:
            if planets:
                del(planets[-1])

        # Clear screen
        if pygame.key.get_pressed()[pygame.K_c]:
            planets.clear()

        # lock and unlock planet
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            for pl in planets:
                pl.check_lock(pos)

        # Adding new planet
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pl = Planet(pos[0], pos[1], 0, 0, 1, False)

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
