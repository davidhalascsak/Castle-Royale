import pygame


class Tile:
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()
