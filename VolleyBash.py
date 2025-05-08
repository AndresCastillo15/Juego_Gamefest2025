import pygame
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Beach Volly")
clock = pygame.time.Clock()

# Colores
AZUL_FONDO = (2, 6, 149)
AZUL_CIELO = (135, 206, 235)
DORADO = (213, 173, 25)
BLANCO = (255, 255, 255)
MARRON = (218, 113, 15)
VERDE = (34, 139, 34)
ROJO = (194, 11, 11)

# Constantes y físicas
PLAYER_SIZE = 50
GROUND_Y = 300
GRAVITY = 0.5
PUNTOS_MAX = 3
DELAY_PELOTA = 60  # frames (1 segundo si el juego va a 60 FPS)

# Tipografías
fuente_titulo = pygame.font.SysFont("Arial", 36, True, False)
fuente_subtitulo = pygame.font.SysFont("Arial", 28, True, False)
fuente_info = pygame.font.SysFont("Arial", 24, False, False)
fuente_texto = pygame.font.SysFont("Arial", 20, False, False)

# Función para crear jugadores
def crear_jugador(x):
    return {"x": x, "y": GROUND_Y, "vel": 5, "is_jumping": False, "jump_vel": 10}

# Función para reiniciar pelota
def reiniciar_pelota(hacia_izquierda):
    return {
        "x": ANCHO // 2,
        "y": 150,
        "radius": 15,
        "vel_x": -4 if hacia_izquierda else 4,
        "vel_y": 0
    }

# Jugadores y pelota
p1, p2 = crear_jugador(100), crear_jugador(650)
ball = reiniciar_pelota(False)
p1_score, p2_score = 0, 0
juego_terminado = False
contador_reinicio = 0

# Movimiento y salto del jugador
def mover_jugador(j, izq, der, salto, keys, min_x, max_x):
    if keys[izq] and j["x"] > min_x:
        j["x"] -= j["vel"]
    if keys[der] and j["x"] + PLAYER_SIZE < max_x:
        j["x"] += j["vel"]
    if keys[salto] and not j["is_jumping"]:
        j["is_jumping"] = True
        j["jump_vel"] = 10

def actualizar_salto(j):
    if j["is_jumping"]:
        j["y"] -= j["jump_vel"]
        j["jump_vel"] -= GRAVITY
        if j["y"] >= GROUND_Y:
            j["y"] = GROUND_Y
            j["is_jumping"] = False

# Colisión jugador-pelota
def verificar_colision(j, pelota):
    jr = pygame.Rect(j["x"], j["y"], PLAYER_SIZE, PLAYER_SIZE)
    pr = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"], pelota["radius"]*2, pelota["radius"]*2)
    if jr.colliderect(pr):
        pelota["vel_x"] *= -1
        pelota["vel_y"] = -7

# Colisión pelota-red
def verificar_colision_red(pelota):
    red = pygame.Rect(ANCHO//2 - 5, 200, 10, 200)
    pr = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"], pelota["radius"]*2, pelota["radius"]*2)
    if pr.colliderect(red):
        pelota["vel_x"] *= -1
        if pelota["x"] < ANCHO//2:
            pelota["x"] = ANCHO//2 - pelota["radius"] - 6
        else:
            pelota["x"] = ANCHO//2 + 6 + pelota["radius"]

# Fondo del juego
def dibujar_fondo():
    pantalla.fill(AZUL_CIELO)
    pygame.draw.rect(pantalla, DORADO, (0, 350, 800, 50))  # Arena
    pygame.draw.circle(pantalla, BLANCO, (700, 50), 30)    # Sol
    pygame.draw.rect(pantalla, MARRON, (100, 250, 15, 100))
    pygame.draw.circle(pantalla, VERDE, (108, 230), 40)
    pygame.draw.rect(pantalla, MARRON, (680, 270, 15, 100))
    pygame.draw.circle(pantalla, VERDE, (688, 250), 40)

# Mostrar texto en pantalla
def mostrar_texto(txt, fuente, color, x, y):
    render = fuente.render(txt, True, color)
    pantalla.blit(render, (x, y))

# Pantalla inicial
mostrar_pantalla = True
while mostrar_pantalla:
    dibujar_fondo()
    mostrar_texto("Beach Volly", fuente_titulo, BLANCO, ANCHO//2 - 100, 100)
    mostrar_texto("Un juego de voleibol con figuras geométricas", fuente_subtitulo, BLANCO, ANCHO//2 - 240, 150)
    mostrar_texto("Andres Castillo, Carlos Galvis, Eyersson Montaña", fuente_info, BLANCO, ANCHO//2 - 250, 200)
    mostrar_texto("Colegio San José de Guanentá - 2025", fuente_info, BLANCO, ANCHO//2 - 200, 240)
    mostrar_texto("Presiona ENTER para comenzar", fuente_subtitulo, AZUL_FONDO, ANCHO//2 - 180, 300)
    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                mostrar_pantalla = False

# Bucle principal del juego
while True:
    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not juego_terminado:
        mover_jugador(p1, pygame.K_a, pygame.K_d, pygame.K_w, keys, 0, ANCHO//2 - 10)
        mover_jugador(p2, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, keys, ANCHO//2 + 10, ANCHO)
        actualizar_salto(p1)
        actualizar_salto(p2)

        if contador_reinicio == 0:
            ball["x"] += ball["vel_x"]
            ball["y"] += ball["vel_y"]
            ball["vel_y"] += 0.2

            if ball["x"] - ball["radius"] <= 0 or ball["x"] + ball["radius"] >= ANCHO:
                ball["vel_x"] *= -1

            if ball["y"] + ball["radius"] >= GROUND_Y + PLAYER_SIZE:
                if ball["x"] < ANCHO // 2:
                    p2_score += 1
                    contador_reinicio = DELAY_PELOTA
                    ball = reiniciar_pelota(False)
                else:
                    p1_score += 1
                    contador_reinicio = DELAY_PELOTA
                    ball = reiniciar_pelota(True)

            verificar_colision(p1, ball)
            verificar_colision(p2, ball)
            verificar_colision_red(ball)

            if p1_score >= PUNTOS_MAX or p2_score >= PUNTOS_MAX:
                juego_terminado = True
        else:
            contador_reinicio -= 1

    else:
        if keys[pygame.K_r]:
            p1_score, p2_score = 0, 0
            juego_terminado = False
            ball = reiniciar_pelota(False)
            contador_reinicio = 0

    # Dibujo de elementos
    dibujar_fondo()
    pygame.draw.rect(pantalla, ROJO, (p1["x"], p1["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(pantalla, ROJO, (p2["x"], p2["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.circle(pantalla, BLANCO, (int(ball["x"]), int(ball["y"])), ball["radius"])
    pygame.draw.rect(pantalla, AZUL_FONDO, (ANCHO//2 - 5, 200, 10, 200))

    mostrar_texto(f"{p1_score}", fuente_titulo, AZUL_FONDO, 50, 20)
    mostrar_texto(f"{p2_score}", fuente_titulo, AZUL_FONDO, 730, 20)

    if juego_terminado:
        texto = "¡Jugador 1 gana!" if p1_score > p2_score else "¡Jugador 2 gana!"
        mostrar_texto(texto, fuente_info, ROJO, ANCHO//2 - 100, 100)
        mostrar_texto("Presiona R para reiniciar", fuente_info, AZUL_FONDO, ANCHO//2 - 140, 140)

    pygame.display.flip()
