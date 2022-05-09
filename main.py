import pygame
from src.persistence import Persistence
from src.button import Button, MenuButton
from src.game import Game
from src.contextmenu import Context
from src.soldier import *
from src.tower import *
from src.core import *
from src.tile import *
from src.tileview import *
import os

pygame.init()

SCREEN_WIDTH = 1248  # 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Royale')

simulation_starting_time = 0  # 1 second = 1000 millisecond
clock = pygame.time.Clock()
FPS = 60

hamburger = Context()

# 1 - Menu
# 2 - New Game
# 3 - Load Game
# 4 - In Game

game_state = 1

in_game_menu = ["MAIN MENU", "BUILD", "TRAIN", "MOVE", "CONTINUE"]

main_menu_scale = 5
# MENU ASSETS
menu_images = {
    "BOTTOM": pygame.image.load("assets/menu_assets/also_tabla.png"),
    "MIDDLE": pygame.image.load("assets/menu_assets/koztes_tabla.png"),
    "LOGO": pygame.image.load("assets/menu_assets/logo_tabla.png"),
    "BG": pygame.image.load("assets/menu_assets/menu_bg.png")
}
menu_images["LOGO"] = pygame.transform.scale(menu_images["LOGO"], (
menu_images["LOGO"].get_width() * main_menu_scale, menu_images["LOGO"].get_height() * main_menu_scale))

main_menu = [(1, "NEW GAME"), (4, "SAVE"), (3, "LOAD"), (2, "QUIT")]
main_menu_btn = []
menu_top_padding = 0
for i, elem in enumerate(main_menu):
    if (len(main_menu) - 1) == i:
        img = menu_images['BOTTOM']
    else:
        img = menu_images['MIDDLE']

    padding = (i * (menu_images['MIDDLE'].get_height() * main_menu_scale))

    main_menu_btn.append(MenuButton(SCREEN_WIDTH / 2 - img.get_width() * main_menu_scale / 2,
                                    menu_top_padding + menu_images["LOGO"].get_height() + padding,
                                    img.get_width() * main_menu_scale, img.get_height() * main_menu_scale, elem[1],
                                    (len(main_menu) - 1) == i))

btn_quit = Button((255, 0, 0), 18, 676, 228, 40, "MAIN MENU")
btn_build = Button((255, 0, 0), 264, 676, 228, 40, "BUILD")
btn_train = Button((255, 0, 0), 510, 676, 228, 40, "TRAIN")
btn_move = Button((255, 0, 0), 756, 676, 228, 40, "MOVE")
btn_continue = Button((255, 0, 0), 1002, 676, 228, 40, "CONTINUE")
btn_end = Button((255, 0, 0), SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT / 2 - 25, 80, 50, "MENU")

btn_back = Button((255, 0, 0), 18, 676, 228, 40, "MAIN MENU")


game = None
persistence = Persistence()

font = pygame.font.SysFont('comicsans', 20)
font2 = pygame.font.Font(os.path.join("assets", "fonts", 'arcadeclassic.ttf'), 23)
font_game_over = pygame.font.Font(os.path.join("assets", "fonts", 'arcadeclassic.ttf'), 100)
SCALE = 3

gold_coin = pygame.image.load("assets/gold_coin.png")
gold_coin = pygame.transform.scale(gold_coin, (16 * SCALE, 16 * SCALE))

game_icon = pygame.image.load("assets/tile_assets/blue_castle.png")
pygame.display.set_icon(game_icon)

sword = pygame.image.load("assets/sword.png")
sword = pygame.transform.scale(sword, (16 * 2, 16 * 2))

health_bar_left = pygame.image.load("assets/health_bar.png")
health_bar_left = pygame.transform.scale(health_bar_left, (44 * SCALE, 9 * SCALE))

health_bar_inside_left = pygame.image.load("assets/health_bar_inside.png")
health_bar_inside_left = pygame.transform.scale(health_bar_inside_left, (44 * SCALE, 9 * SCALE))

health_bar_inside_original_left = pygame.image.load("assets/health_bar_inside.png")
health_bar_inside_original_left = pygame.transform.scale(health_bar_inside_original_left, (44 * SCALE, 9 * SCALE))

health_bar_right = pygame.image.load("assets/health_bar.png")
health_bar_right = pygame.transform.flip(health_bar_right, True, False)
health_bar_right = pygame.transform.scale(health_bar_right, (44 * SCALE, 9 * SCALE))

health_bar_inside_right = pygame.image.load("assets/health_bar_inside.png")
health_bar_inside_right = pygame.transform.flip(health_bar_inside_right, True, False)
health_bar_inside_right = pygame.transform.scale(health_bar_inside_right, (44 * SCALE, 9 * SCALE))

health_bar_inside_original_right = pygame.image.load("assets/health_bar_inside.png")
health_bar_inside_original_right = pygame.transform.flip(health_bar_inside_original_right, True, False)
health_bar_inside_original_right = pygame.transform.scale(health_bar_inside_original_right, (44 * SCALE, 9 * SCALE))

buttons_background = pygame.image.load("assets/in_game_button_assets/button_background.png")
lock = pygame.image.load("assets/lock.png")
lock = pygame.transform.scale(lock, (16 * 2, 16 * 2))
lock2 = pygame.image.load("assets/lock.png")
lock2 = pygame.transform.scale(lock, (16 * 3, 16 * 3))

# Change name color based on round
name_color = (0, 0, 0)
name_color_now_playing = (255, 0, 0)

tile_view = []

load_buttons = []
def create_buttons(num_buttons):
    global load_buttons
    load_buttons = []
    for i in range(num_buttons):
        load_buttons.append(Button((255, 0, 0), (i * 228) + ((i+1) * 18), 18, 228, 40, "MAP {}".format(i)))


def fill(surface, original_surface, hue):
    if hue < 0:
        hue = 0
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            c = original_surface.get_at((x, y))
            c.hsla = (c.hsla[0] + hue, c.hsla[1], c.hsla[2], c.hsla[3])
            surface.set_at((x, y), pygame.Color(c.r, c.g, c.b, a))


def get_name_color(player):
    if game.current_player == player:
        return name_color_now_playing
    return name_color

def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min

    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)

def update_tile_view(map):
    if(tile_view == []):
        for i in range(0, 14):
            tile_view.append([])
            for j in range(0, 26):
                tile_view[i].append(TileView(game, i, j))
                tile_view[i][j]._tile = map[i][j]
    else:
        for i in range(0, 14):
            for j in range(0, 26):
                tile_view[i][j]._tile = map[i][j]


run = True
while run:
    clock.tick(FPS)
    # Background color for testing
    screen.fill((247, 217, 181))
    # Draw update function
    if game_state == 1:

        screen.blit(menu_images["BG"], [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])

        screen.blit(menu_images["LOGO"], [SCREEN_WIDTH / 2 - img.get_width() * main_menu_scale / 2, menu_top_padding,
                                          menu_images["LOGO"].get_width(), menu_images["LOGO"].get_height()])

        for elem in main_menu_btn:
            elem.draw(screen)

        if game is None:
            screen.blit(lock2, [410, 320, lock.get_width(), lock.get_height()])
        # draw
    elif game_state == 2:
        screen.blit(menu_images["BG"], [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])

        if game.winner:
            game_over_title = font_game_over.render("{} WINS".format(game.winner.name), True, (255, 215, 166))
            game_over_title_outlines = font_game_over.render("{} WINS".format(game.winner.name), True, (39, 28, 57))

            screen.blit(game_over_title_outlines, ((SCREEN_WIDTH / 2 - game_over_title.get_width() / 2) - 4,
                                                   (SCREEN_HEIGHT / 2 - game_over_title.get_height() / 2) + 4))
            screen.blit(game_over_title, (
            SCREEN_WIDTH / 2 - game_over_title.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_title.get_height() / 2))

        btn_back.draw(screen)
        btn_back.is_over(pygame.mouse.get_pos())
        # draw
    elif game_state == 3:
        pass
    elif game_state == 5:
        screen.blit(menu_images["BG"], [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])

        for i in load_buttons:
            i.draw(screen)
            i.is_over(pygame.mouse.get_pos())

        btn_back.draw(screen)
        btn_back.is_over(pygame.mouse.get_pos())

        # draw
    elif game_state == 4:
        # Draw Tiles
        
        screen.blit(buttons_background, [0, 672, SCREEN_WIDTH, 200])
        
        if not game.is_ended:
            update_tile_view(game._map)
            for i in range(0, 14):
                for j in range(0, 26):
                    tile_view[i][j].draw(screen)
            for i in range(0, 14):
                for j in range(0, 26):
                    tile_view[i][j].draw_buildings_and_soldiers(screen)
            for i in range(0, 14):
                for j in range(0, 26):
                    tile_view[i][j].draw_context_menu_for_tiles(screen)
        else:
            text = pygame.font.SysFont('Arial', 25).render("The winner is {0}.".format(game.winner), False, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - 60))
            btn_end.draw(screen)

        # Draw Player Information
        if not game.is_ended:
            p1_name = str(game.player_1.name)
            p2_name = str(game.player_2.name)

            player1_name = font2.render(p1_name, True, (255, 255, 255))
            player1_name_outlines = font2.render(p1_name, True, (39, 28, 57))
            player1_money = font2.render(str(game.player_1.gold), True, pygame.Color(39, 28, 57))
            player1_money_outline = font2.render(str(game.player_1.gold), True, pygame.Color(255, 206, 73))

            hud_pos_x = 10
            hud_pos_y = 70

            player1_hp = game.player_1.castle_tile.units[0].health
            fill(health_bar_inside_left, health_bar_inside_original_left, math.floor(player1_hp / 10))

            screen.blit(player1_name_outlines, (30, 15, 200, 200))
            screen.blit(player1_name, (30 + 2, 15 - 2, 200, 200))

            player1_display_hp = translate(player1_hp, 0, 1000, 160, 1000)
            screen.blit(health_bar_left, (20, 45, 200, 200))
            screen.blit(health_bar_inside_left, (20, 45, 200, 200),
                        (0, 0, (health_bar_inside_left.get_width() * player1_display_hp) / 1000, 200))

            screen.blit(gold_coin, (hud_pos_x, hud_pos_y))
            screen.blit(player1_money, (-5 + hud_pos_x + gold_coin.get_width(),
                                        hud_pos_y + (gold_coin.get_height() / 2 - player1_money.get_height() / 2)))
            screen.blit(player1_money_outline, (-5 + 3 + hud_pos_x + gold_coin.get_width(), hud_pos_y + (
                        gold_coin.get_height() / 2 - player1_money_outline.get_height() / 2) - 1))

            player2_name = font2.render(p2_name, True, (255, 255, 255))
            player2_name_outlines = font2.render(p2_name, True, (39, 28, 57))
            player2_money = font2.render(str(game.player_2.gold), True, pygame.Color(39, 28, 57))
            player2_money_outline = font2.render(str(game.player_2.gold), True, pygame.Color(255, 206, 73))

            if not game.start_simulation:
                if game.current_player == game.player_1:
                    screen.blit(sword, (30 + player1_name.get_width(), 8))
                else:
                    screen.blit(pygame.transform.flip(sword, flip_x=True, flip_y=False),
                                (SCREEN_WIDTH - 30 - sword.get_width() - player2_name.get_width(), 8))

            player2_hp = game.player_2.castle_tile.units[0].health
            fill(health_bar_inside_right, health_bar_inside_original_right, math.floor(player2_hp / 10))
            screen.blit(health_bar_right, (SCREEN_WIDTH - 20 - health_bar_right.get_width(), 45, 200, 200))

            player2_display_hp = translate(player2_hp, 0, 1000, 160, 1000)
            screen.blit(health_bar_inside_right, (SCREEN_WIDTH - 20 - health_bar_inside_right.get_width() + (
                        health_bar_inside_right.get_width() - (
                            (health_bar_inside_right.get_width() * player2_display_hp) / 1000)), 45, 200, 200), (
                        health_bar_inside_right.get_width() - (
                                    (health_bar_inside_right.get_width() * player2_display_hp) / 1000), 0,
                        health_bar_inside_right.get_width(), 200))

            screen.blit(player2_name_outlines, (SCREEN_WIDTH - 30 - player2_name_outlines.get_width(), 15, 200, 200))
            screen.blit(player2_name, (SCREEN_WIDTH - 30 - player2_name_outlines.get_width() + 2, 15 - 2, 200, 200))

            screen.blit(gold_coin, (SCREEN_WIDTH - gold_coin.get_width() - hud_pos_x, hud_pos_y))
            screen.blit(player2_money, (
            5 + SCREEN_WIDTH - gold_coin.get_width() - hud_pos_x - player2_money.get_width(),
            hud_pos_y + (gold_coin.get_height() / 2 - player2_money.get_height() / 2)))
            screen.blit(player2_money_outline, (
            5 + 3 + SCREEN_WIDTH - gold_coin.get_width() - hud_pos_x - player2_money_outline.get_width(),
            hud_pos_y + (gold_coin.get_height() / 2 - player2_money_outline.get_height() / 2) - 1))

            if not game.start_simulation:
                current_player_state = font2.render(str(game.current_player.state), True, (255, 255, 255))
                current_player_state_outline = font2.render(str(game.current_player.state), True, (39, 28, 57))
            else:
                current_player_state = font2.render("Simulation", True, (255, 255, 255))
                current_player_state_outline = font2.render("Simulation", True, (39, 28, 57))

            screen.blit(current_player_state_outline,
                        ((SCREEN_WIDTH / 2) - 2 - (current_player_state.get_width() / 2), 10 + 2))
            screen.blit(current_player_state, ((SCREEN_WIDTH / 2) - (current_player_state.get_width() / 2), 10))

            if game_state == 4 and game.winner:
                game_state = 2

        if not game.start_simulation:
            if not hamburger.opened:
                btn_quit.is_over(pygame.mouse.get_pos())
                btn_build.is_over(pygame.mouse.get_pos())
                btn_train.is_over(pygame.mouse.get_pos())
                btn_move.is_over(pygame.mouse.get_pos())
                btn_continue.is_over(pygame.mouse.get_pos())
                btn_end.is_over(pygame.mouse.get_pos())

        if not game.is_ended:
            btn_quit.draw(screen)
            btn_build.draw(screen)
            btn_train.draw(screen)
            btn_move.draw(screen)
            btn_continue.draw(screen)

        if game.start_simulation:
            screen.blit(lock, [17, 682, lock.get_width(), lock.get_height()])
            screen.blit(lock, [263, 682, lock.get_width(), lock.get_height()])
            screen.blit(lock, [509, 682, lock.get_width(), lock.get_height()])
            screen.blit(lock, [755, 682, lock.get_width(), lock.get_height()])
            screen.blit(lock, [1001, 682, lock.get_width(), lock.get_height()])
        # Draw Context Menu
        hamburger.draw(screen)
        hamburger.is_over(pygame.mouse.get_pos())

        if game.start_simulation:
            game.simulate()

    # Keyboard input update function
    for event in pygame.event.get():
        if game_state == 1:
            if event.type == pygame.MOUSEBUTTONUP:
                for i, btn in enumerate(main_menu_btn):
                    if btn.is_over(pygame.mouse.get_pos()):
                        if main_menu[i][0] == 1:
                            game = Game()
                            game.new_game(1000, "Player1", "Player2")
                            game_state = 4
                            tile_view = []
                        elif main_menu[i][0] == 2:
                            run = False
                        elif main_menu[i][0] == 3:
                            num_saves = persistence.get_num_saves()
                            create_buttons(num_saves)
                            game_state = 5
                        elif main_menu[i][0] == 4:
                            persistence.save(game)
                            game = None

        elif game_state == 2:
            if event.type == pygame.MOUSEBUTTONUP and (not game or not game.start_simulation):
                if btn_back.is_over(pygame.mouse.get_pos()):
                    game_state = 1

        elif game_state == 5:
            if event.type == pygame.MOUSEBUTTONUP and (not game or not game.start_simulation):
                if btn_back.is_over(pygame.mouse.get_pos()):
                    game_state = 1
                for index, btn in enumerate(load_buttons):
                    if btn.is_over(pygame.mouse.get_pos()):
                        load = persistence.load(index)
                        if load:
                            game = load
                            tile_view = []
                        game_state = 4

        elif game_state == 3:
            pass
            # keyboard input
        elif game_state == 4:
            if not game.start_simulation:
                if hamburger.opened:
                    if event.type == pygame.MOUSEBUTTONUP:
                        content = hamburger.is_over(pygame.mouse.get_pos())
                        for item in content:
                            if item[2] and item[1] == "Tower":
                                game.current_tile.build(game.current_player, "BasicTower")
                            if item[2] and item[1] == "Slow":
                                game.current_tile.build(game.current_player, "Slow")
                            if item[2] and item[1] == "Splash":
                                game.current_tile.build(game.current_player, "Splash")
                            if item[2] and item[1] == "Barracks":
                                print("barracks")
                            if item[2] and item[1] == "Upgrade":
                                game.current_tile.upgrade_tower()
                            if item[2] and item[1] == "Demolish":
                                game.current_tile.demolish_tower()
                            if item[2] and item[1] == "Remove":
                                game.current_tile.remove_tower_ruin()
                            if item[2] and item[1] == "Soldier":
                                game.current_player.castle_tile.train(game.current_player, "BasicSoldier")
                            if item[2] and item[1] == "Climber":
                                game.current_player.castle_tile.train(game.current_player, "Climber")
                            if item[2] and item[1] == "Suicide":
                                game.current_player.castle_tile.train(game.current_player, "Suicide")
                            if item[2] and item[1] == "Tank":
                                game.current_player.castle_tile.train(game.current_player, "Tank")
                            if item[2] and item[1] == "Select":
                                game.select_current_tile()
                            if item[2] and item[1] == "Waypoint":
                                game.add_waypoint()
                            if item[2] and item[1] == "Reset":
                                game.reset_waypoint()
                            hamburger.opened = False
                else:
                    for row in game.map:
                        for tile in row:
                            if tile.is_over(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                                if game.current_player.state == "BUILD":
                                    mouse_cords = pygame.mouse.get_pos()
                                    if tile.has_building and issubclass(type(tile.units[0]), Tower) and not tile.units[
                                        0].is_in_ruins:
                                        hamburger.change_content(["Upgrade", "Demolish"])
                                    elif tile.has_building and issubclass(type(tile.units[0]), Tower) and tile.units[
                                        0].is_in_ruins:
                                        hamburger.change_content(["Remove"])
                                    else:
                                        hamburger.change_content(["Tower", "Slow", "Splash"])
                                    hamburger.open(mouse_cords[0], mouse_cords[1])

                                elif game.current_player.state == "TRAIN":
                                    mouse_cords = pygame.mouse.get_pos()
                                    hamburger.change_content(["Soldier", "Climber", "Suicide", "Tank"])
                                    hamburger.open(mouse_cords[0], mouse_cords[1])

                                elif game.current_player.state == "MOVE":
                                    mouse_cords = pygame.mouse.get_pos()
                                    options = []
                                    if tile_can_be_selected(tile):
                                        options.append("Select")

                                    if game.selected_tile and tile_can_be_added_as_waypoint(tile, game.selected_tile):
                                        options.append("Waypoint")

                                    if game.selected_tile:
                                        options.append("Reset")
                                    hamburger.change_content(options)
                                    if len(options) > 0:
                                        hamburger.open(mouse_cords[0], mouse_cords[1])
                                game.current_tile = tile
                    if event.type == pygame.MOUSEBUTTONUP and not game.start_simulation:
                        if btn_continue.is_over(pygame.mouse.get_pos()):
                            btn_continue.is_over((0, 0))
                            game.next_round()
                            for row in game.map:
                                for tile in row:
                                    tile.selected = False
                                    tile.waypoint = False
                            if game.start_simulation:
                                simulation_starting_time = pygame.time.get_ticks()
                        elif btn_quit.is_over(pygame.mouse.get_pos()):
                            game_state = 1
                        elif btn_build.is_over(pygame.mouse.get_pos()):
                            game.current_player.state = "BUILD"
                        elif btn_train.is_over(pygame.mouse.get_pos()):
                            game.current_player.state = "TRAIN"
                        elif btn_move.is_over(pygame.mouse.get_pos()):
                            game.current_player.state = "MOVE"
                        elif btn_end.is_over(pygame.mouse.get_pos()):
                            pass
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()


