import pygame
pygame.init()
import os
font2 = pygame.font.Font(os.path.join("assets", "fonts", 'arcadeclassic.ttf'), 35)

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self.color = (255, 255, 255)
        self.hover_color = (0, 0, 0)
        self.hover = False

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self._x - 2, self._y - 2, self._width + 4, self._height + 4), 0)

        pygame.draw.rect(win, (255, 255, 255), (self._x, self._y, self._width, self._height), 2)
        if self.hover:
            pygame.draw.rect(win, (255, 255, 255), (self._x, self._y, self._width, self._height), 0)

        if self._text != '':
            font = pygame.font.SysFont('arial', 15)
            text = font.render(self.text, 1, self.get_text_color())
            win.blit(text,
                     (self._x + (self._width / 2 - text.get_width() / 2),
                      self._y + (self._height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self._x < pos[0] < self._x + self._width:
            if self._y < pos[1] < self._y + self._height:
                self.hover = True
                return True
        self.hover = False
        return False

    def get_text_color(self):
        if self.hover:
            return self.hover_color
        return self.color

    @property
    def text(self):
        return self._text


class MenuButton:
    def __init__(self, x, y, width, height, text='', last=False):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self.hover = False
        self.menu_images = {
            "BOTTOM": pygame.transform.scale(pygame.image.load("assets/menu_assets/also_tabla.png"), (self._width, self._height)),
            "MIDDLE": pygame.transform.scale(pygame.image.load("assets/menu_assets/koztes_tabla.png"), (self._width, self._height)),
            "LOGO": pygame.transform.scale(pygame.image.load("assets/menu_assets/logo_tabla.png"), (self._width, self._height)),
            "BG": pygame.image.load("assets/menu_assets/menu_bg.png")
        }
        self.last = last
        self.color = (255, 221, 184)
        self.hover_color = (255, 255, 0)

    def draw(self, win, outline=None):
        self.is_over(pygame.mouse.get_pos())
        # if outline:
        #     pygame.draw.rect(win, outline, (self._x - 2, self._y - 2, self._width + 4, self._height + 4), 0)
        #
        # pygame.draw.rect(win, (255, 255, 255), (self._x, self._y, self._width, self._height), 2)
        # if self.hover:
        #     pygame.draw.rect(win, (255, 255, 255), (self._x, self._y, self._width, self._height), 0)
        if self.last:
            img = self.menu_images["BOTTOM"]
        else:
            img = self.menu_images["MIDDLE"]

        if self.hover:
            color = self.hover_color
        else:
            color = self.color

        if self.last:
            eltolas = (5 * 5) / 2
        else:
            eltolas = 0

        win.blit(img, [self._x, self._y, self._width, self._height])
        if self._text != '':
            text2 = font2.render(self._text, True, (61, 51, 45))
            win.blit(text2,
                     (self._x + 4 + (self._width / 2 - text2.get_width() / 2),
                      self._y + 4 + eltolas + (self._height / 2 - text2.get_height() / 2)))

            text = font2.render(self._text, True, color)
            win.blit(text,
                     (self._x + (self._width / 2 - text.get_width() / 2),
                      self._y + eltolas + (self._height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self._x < pos[0] < self._x + self._width:
            if self._y < pos[1] < self._y + self._height:
                self.hover = True
                return True
        self.hover = False
        return False
