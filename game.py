from time import sleep

import pygame
import random

import sys

# Tamaño de la celda del laberinto
GRID_SIZE = 30
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450


def draw_maze(screen, maze):
    wall_color = (0, 0, 255)  # Color de la pared (en este caso, azul)
    path_color = (255, 255, 255)  # Color del camino (en este caso, blanco)
    start_color = (0, 255, 0)  # Color del punto inicial (en este caso, verde)
    end_color = (255, 0, 230)  # Color del punto final (en este caso, violeta)

    screen.fill((0, 0, 0))  # Rellena la pantalla con color negro

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:  # Pared
                pygame.draw.rect(screen, wall_color, (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == 0:  # Camino
                pygame.draw.rect(screen, path_color, (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == 'S':  # Punto inicial
                pygame.draw.rect(screen, start_color, (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == 'E':  # Punto final
                pygame.draw.rect(screen, end_color, (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()  # Actualiza la pantalla


def _maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def recursive_backtracker(x, y):
        maze[y][x] = 0  # Marcar la celda como parte del camino

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0  # Marcar el camino que se está abriendo
                recursive_backtracker(x + dx * 2, y + dy * 2)  # Llamada recursiva

    # Comenzar desde celda aleatoria
    recursive_backtracker(random.randrange(width // 2) * 2, random.randrange(height // 2) * 2)

    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    maze[start_y][start_x] = 'S'  # Marcar punto inicial

    end_x, end_y = start_x, start_y
    while (end_x, end_y) == (start_x, start_y) or maze[end_y][end_x] == 1:
        end_x = random.randint(0, width - 1)
        end_y = random.randint(0, height - 1)

    maze[end_y][end_x] = 'E'  # Marcar el punto final

    return maze


def place_start_and_end(maze):
    start_x, start_y, end_x, end_y = 0, 0, 0, 0  # Inicializar las variables de posición
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'S':
                start_x, start_y = x, y
            if maze[y][x] == 'E':
                end_x, end_y = x, y
    return maze, (start_x, start_y), (end_x, end_y)


def find_starting_position(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'S':
                return (x, y)
    return None


def move_player(event, player_position, maze):
    dx, dy = 0, 0
    if event.key == pygame.K_LEFT:
        dx = -1
    elif event.key == pygame.K_RIGHT:
        dx = 1
    elif event.key == pygame.K_UP:
        dy = -1
    elif event.key == pygame.K_DOWN:
        dy = 1

    new_x = player_position[0] + dx
    new_y = player_position[1] + dy
    if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
        if maze[new_y][new_x] == 0 or maze[new_y][new_x] == 'E' or maze[new_y][new_x] == 'S':
            player_position = (new_x, new_y)

    return player_position


def check_victory(player_position, maze):
    x, y = player_position

    if maze[y][x] == 'E':
        return True
    else:
        return False


def generate_enemies(maze, num_enemies):
    enemies = []
    for _ in range(num_enemies):
        while True:
            x = random.randint(0, len(maze[0]) - 1)
            y = random.randint(0, len(maze) - 1)
            if maze[y][x] == 0:
                enemies.append((x, y))
                break
    return enemies


def move_enemies(maze, enemies):
    for i in range(len(enemies)):
        x, y = enemies[i]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] == 0:
                enemies[i] = (new_x, new_y)
                break
    pygame.time.wait(220)


def check_collision(player_position, enemies):
    return player_position in enemies


def show_menu(screen):
    font = pygame.font.SysFont(None, 50)
    play_option = font.render("Jugar", True, (255, 255, 255))
    exit_option = font.render("Salir", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    play_x = (SCREEN_WIDTH - play_option.get_width()) // 2  # Centrar según ancho de la pantalla
    play_y = (SCREEN_HEIGHT - play_option.get_height() - exit_option.get_height()) // 2  # Centrar verticalmente
    exit_x = (SCREEN_WIDTH - exit_option.get_width()) // 2  # Centrar según ancho de la pantalla
    exit_y = play_y + play_option.get_height()  # Colocar debajo de la opción "Jugar"

    screen.blit(play_option, (play_x, play_y))
    screen.blit(exit_option, (exit_x, exit_y))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_x < mouse_x < play_x + play_option.get_width() and play_y < mouse_y < play_y + play_option.get_height():
                    return True
                elif exit_x < mouse_x < exit_x + exit_option.get_width() and exit_y < mouse_y < exit_y + exit_option.get_height():
                    pygame.quit()
                    sys.exit()


def show_result(screen, result):
    font = pygame.font.SysFont(None, 50)
    if result == 'win':
        text = font.render("¡Has ganado! Presiona cualquier tecla para volver al menu.", True, (255, 255, 255))
    else:
        text = font.render("¡Has perdido! Presiona cualquier tecla para volver al menu.", True, (255, 255, 255))

    text_x = (SCREEN_WIDTH - text.get_width()) // 2  # Centrar según el ancho de la pantalla
    text_y = (SCREEN_HEIGHT - text.get_height()) // 2  # Centrar verticalmente

    screen.fill((0, 0, 0))
    screen.blit(text, (text_x, text_y))
    pygame.display.update()
    pygame.time.wait(500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return True


def main_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Laberinto Increíble")

    running = True
    while running:
        play = show_menu(screen, )
        if not play:
            break

        # Restablecer el juego
        maze = _maze(20, 15)
        place_start_and_end(maze)
        player_position = find_starting_position(maze)
        num_enemies = 2
        enemies = generate_enemies(maze, num_enemies)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    player_position = move_player(event, player_position, maze)

            if check_victory(player_position, maze):
                show_result(screen, 'win')
                break

            move_enemies(maze, enemies)

            if check_collision(player_position, enemies):
                show_result(screen, 'lose')
                break

            draw_maze(screen, maze)
            pygame.draw.rect(screen, (255, 0, 0),
                             (player_position[0] * GRID_SIZE, player_position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            for enemy in enemies:
                pygame.draw.rect(screen, (255, 255, 0),
                                 (enemy[0] * GRID_SIZE, enemy[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            pygame.display.update()

    pygame.quit()

main_game()
