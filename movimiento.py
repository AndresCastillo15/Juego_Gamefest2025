import pygame
import sys

# Inicialización
pygame.init()

# Pantalla
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego con Pelota")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()

# Constantes
PLAYER_SIZE = 50
GROUND_Y = 300
GRAVITY = 0.5

# Jugadores
def crear_jugador(x):
    return {"x": x, "y": GROUND_Y, "vel": 5, "is_jumping": False, "jump_vel": 10}

p1 = crear_jugador(100)
p2 = crear_jugador(600)

# Pelota
ball = {"x": WIDTH // 2, "y": HEIGHT // 2, "radius": 15, "vel_x": 4, "vel_y": 0}

# Función para movimiento
def mover_jugador(jugador, izq, der, salto, keys):
    if keys[izq]:
        jugador["x"] -= jugador["vel"]
    if keys[der]:
        jugador["x"] += jugador["vel"]
    if keys[salto] and not jugador["is_jumping"]:
        jugador["is_jumping"] = True
        jugador["jump_vel"] = 10

# Función para saltos
def actualizar_salto(jugador):
    if jugador["is_jumping"]:
        jugador["y"] -= jugador["jump_vel"]
        jugador["jump_vel"] -= GRAVITY
        if jugador["y"] >= GROUND_Y:
            jugador["y"] = GROUND_Y
            jugador["is_jumping"] = False

# Función para colisiones con jugadores
def verificar_colision(jugador, pelota):
    jugador_rect = pygame.Rect(jugador["x"], jugador["y"], PLAYER_SIZE, PLAYER_SIZE)
    pelota_rect = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"],
                              pelota["radius"] * 2, pelota["radius"] * 2)
    if jugador_rect.colliderect(pelota_rect):
        # Rebotar dependiendo de dirección
        if pelota["vel_x"] > 0 and pelota["x"] < jugador["x"]:
            pelota["vel_x"] *= -1
        elif pelota["vel_x"] < 0 and pelota["x"] > jugador["x"]:
            pelota["vel_x"] *= -1

        # Rebote vertical mínimo para que no se quede pegada
        pelota["vel_y"] = -3

# Bucle principal
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    mover_jugador(p2, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, keys)
    mover_jugador(p1, pygame.K_a, pygame.K_d, pygame.K_w, keys)

    actualizar_salto(p1)
    actualizar_salto(p2)

    # Movimiento de la pelota
    ball["x"] += ball["vel_x"]
    ball["y"] += ball["vel_y"]

    # Rebote en bordes
    if ball["x"] - ball["radius"] <= 0 or ball["x"] + ball["radius"] >= WIDTH:
        ball["vel_x"] *= -1
    if ball["y"] - ball["radius"] <= 0 or ball["y"] + ball["radius"] >= HEIGHT:
        ball["vel_y"] *= -1

    # Colisiones con jugadores
    verificar_colision(p1, ball)
    verificar_colision(p2, ball)

    # Dibujar jugadores y pelota
    pygame.draw.rect(screen, BLUE, (p1["x"], p1["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, BLUE, (p2["x"], p2["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.circle(screen, RED, (int(ball["x"]), int(ball["y"])), ball["radius"])

    pygame.display.update()
    clock.tick(60)


## BETA


