import pygame
SCREEN_WIDTH = 1248


class Context:
    def __init__(self):
        self.content = []
        self.opened = False
        self.x = 0
        self.y = 0
        self.height = 20
        self.width = 160
        self.font = pygame.font.SysFont('arial', 15)
        self.color = (255, 255, 255)
        self.hover_color = (0, 0, 0)

    def draw(self, surface):
        if self.opened:
            for item in self.content:
                text = self.font.render(item[1], 1, self.get_text_color(item[2]))
                pygame.draw.rect(surface, self.get_color(item[2]), pygame.Rect(self.x, self.y + ((item[0]-1) * self.height), self.width, self.height))
                surface.blit(text,
                         (self.x + (self.width / 2 - text.get_width() / 2),
                          self.y + ((item[0]-1) * self.height) + (self.height / 2 - text.get_height() / 2)))

    def open(self, x, y):
        if x + self.width > SCREEN_WIDTH:
            self.x = x-self.width
        else:
            self.x = x
        self.y = y
        self.opened = True

    def change_content(self, content):
        self.content = []
        for index, item in enumerate(content):
            self.content.append((index + 1, item, False))

    def get_color(self, hover):
        if hover:
            return self.hover_color
        return self.color

    def get_text_color(self, hover):
        if hover:
            return self.color
        return self.hover_color

    def is_over(self, pos):
        for index, item in enumerate(self.content):
            if self.x < pos[0] < self.x + self.width:
                if (self.y + ((item[0]-1) * self.height)) < pos[1] < (self.y + ((item[0]-1) * self.height)) + self.height:
                    self.content[index] = (item[0], item[1], True)
                else:
                    self.content[index] = (item[0], item[1], False)
            else:
                self.content[index] = (item[0], item[1], False)
        return self.content

    def is_outside(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height * len(self.content):
                return False
        return True

