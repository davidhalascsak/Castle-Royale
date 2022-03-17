import pygame


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
