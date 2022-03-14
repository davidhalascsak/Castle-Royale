import pygame

import soldier
import tower
import tile

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Royale')


clock = pygame.time.Clock()
FPS = 60

# 1 - Menu
# 2 - New Game
# 3 - Load Game
# 4 - In Game

game_state = 4

# tile1 = tile.Tile()

map = []

for x in range(0, 26):
    map.append([])
    for y in range(0, 15):
        map[len(map) - 1].append(tile.Tile(x, y))

print(map)

run = True
while run:
    clock.tick(FPS)
    if game_state == 1:
        pass
        # draw
    elif game_state == 2:
        pass
        # draw
    elif game_state == 3:
        pass
        # draw
    elif game_state == 4:
        # pass
        for row in map:
            for tile in row:
                tile.draw(screen)
        # tile1.draw(screen)

    for event in pygame.event.get():
        if game_state == 1:
            pass
            # keyboard input
        elif game_state == 2:
            pass
            # keyboard input
        elif game_state == 3:
            pass
            # keyboard input
        elif game_state == 4:
            pass
            # keyboard input

        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()



