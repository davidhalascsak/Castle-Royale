import pygame

from src.button import Button
from src.game import Game

pygame.init()

SCREEN_WIDTH = 1248 # 1280
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

button1 = Button((255, 255, 255), 10, 10, 100, 30, "TEST")

game = Game()
game.new_game(1000, 10, "Player1", "Player2")

font = pygame.font.SysFont('comicsans', 20)


# Change name color based on round
name_color = (0, 0, 0)
name_color_now_playing = (255, 0, 0)


def get_name_color(player):
    if game.now_playing == player:
        return name_color_now_playing
    return name_color


run = True
while run:
    clock.tick(FPS)
    # Background color for testing
    screen.fill((0, 100, 200))
    # Draw update function
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
        # Draw Tiles
        for row in game.map:
            for tile in row:
                tile.draw(screen)

        # Draw Player Information
        player1_name = font.render(str(game.player_1.get_name()), True, get_name_color(game.player_1))
        player1_money = font.render(str(game.player_1.get_gold()), True, get_name_color(game.player_1))

        screen.blit(player1_name, (10, 10))
        screen.blit(player1_money, (10, 35))

        player2_name = font.render(str(game.player_2.get_name()), True, get_name_color(game.player_2))
        player2_money = font.render(str(game.player_2.get_gold()), True, get_name_color(game.player_2))

        screen.blit(player2_name, (SCREEN_WIDTH - max(player2_money.get_width(), player2_name.get_width()) - 10, 10))
        screen.blit(player2_money, (SCREEN_WIDTH - max(player2_money.get_width(), player2_name.get_width()) - 10, 35))

    # Keyboard input update function
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
            for row in game.map:
                for tile in row:
                    tile.isOver(pygame.mouse.get_pos())

        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()