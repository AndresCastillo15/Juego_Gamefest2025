# Beach Volly
import pygame, sys

# Inicialización de Pygame
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

# Jugadores, pelota y física
PLAYER_SIZE = 50
GROUND_Y = 300
GRAVITY = 0.5
PUNTOS_MAX = 3
DELAY_PELOTA = 60  # Frames (1 segundo si va a 60 FPS)

# Fuente de texto
font = pygame.font.SysFont("Arial", 30, 1, 1)

# Cargar imagen del logo
logo = pygame.image.load("img/logo.png")
logo = pygame.transform.scale(logo, (150, 150))

# Función para crear jugador

def crear_jugador(x):
    return {"x": x, "y": GROUND_Y, "vel": 5, "is_jumping": False, "jump_vel": 10}

# Función para reiniciar pelota con dirección

def reiniciar_pelota(hacia_izquierda):
    return {
        "x": ANCHO // 2,
        "y": 150,
        "radius": 15,
        "vel_x": -4 if hacia_izquierda else 4,
        "vel_y": 0
    }

# Inicializar jugadores y estado del juego
p1, p2 = crear_jugador(100), crear_jugador(650)
ball = reiniciar_pelota(False)
p1_score, p2_score = 0, 0
juego_terminado = False
contador_reinicio = 0

# Movimiento de los jugadores

def mover_jugador(j, izq, der, salto, keys, min_x, max_x):
    if keys[izq] and j["x"] > min_x:
        j["x"] -= j["vel"]
    if keys[der] and j["x"] + PLAYER_SIZE < max_x:
        j["x"] += j["vel"]
    if keys[salto] and not j["is_jumping"]:
        j["is_jumping"] = True
        j["jump_vel"] = 10

# Física del salto

def actualizar_salto(j):
    if j["is_jumping"]:
        j["y"] -= j["jump_vel"]
        j["jump_vel"] -= GRAVITY
        if j["y"] >= GROUND_Y:
            j["y"] = GROUND_Y
            j["is_jumping"] = False

# Colisión entre jugador y pelota

def verificar_colision(j, pelota):
    jr = pygame.Rect(j["x"], j["y"], PLAYER_SIZE, PLAYER_SIZE)
    pr = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"], pelota["radius"]*2, pelota["radius"]*2)
    if jr.colliderect(pr):
        pelota["vel_x"] *= -1
        pelota["vel_y"] = -7

# Colisión con la red

def verificar_colision_red(pelota):
    red = pygame.Rect(ANCHO//2 - 5, 200, 10, 200)
    pr = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"], pelota["radius"]*2, pelota["radius"]*2)
    if pr.colliderect(red):
        pelota["vel_x"] *= -1
        if pelota["x"] < ANCHO//2:
            pelota["x"] = ANCHO//2 - pelota["radius"] - 6
        else:
            pelota["x"] = ANCHO//2 + 6 + pelota["radius"]

# Dibujar fondo

def dibujar_fondo():
    pantalla.fill(AZUL_CIELO)
    pygame.draw.rect(pantalla, DORADO, (0, 350, 800, 50))  # Arena
    pygame.draw.circle(pantalla, BLANCO, (700, 50), 30)    # Sol
    pygame.draw.rect(pantalla, MARRON, (100, 250, 15, 100))
    pygame.draw.circle(pantalla, VERDE, (108, 230), 40)
    pygame.draw.rect(pantalla, MARRON, (680, 270, 15, 100))
    pygame.draw.circle(pantalla, VERDE, (688, 250), 40)

# Mostrar texto en pantalla

def mostrar_texto(txt, color, x, y):
    render = font.render(txt, True, color)
    pantalla.blit(render, (x, y))

# Pantalla inicial con logo y presentación
mostrar_pantalla = True
while mostrar_pantalla:
    dibujar_fondo()
    pantalla.blit(logo, (ANCHO//2 - 75, 20))

    fuente = pygame.font.SysFont("Arial", 30, 1, 1)
    titulo = fuente.render("Beach Volly", True, BLANCO)
    subtitulo = pygame.font.SysFont("Arial", 24).render("Un juego de voleibol con figuras geométricas", True, BLANCO)
    autores = pygame.font.SysFont("Arial", 20).render("Andres Castillo, Carlos Galvis, Eyersson Montaña", True, BLANCO)
    colegio = pygame.font.SysFont("Arial", 20).render("Colegio San José de Guanentá - 2025", True, BLANCO)
    iniciar = pygame.font.SysFont("Arial", 20).render("Presiona ENTER para comenzar", True, AZUL_FONDO)

    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 180))
    pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 220))
    pantalla.blit(autores, (ANCHO//2 - autores.get_width()//2, 260))
    pantalla.blit(colegio, (ANCHO//2 - colegio.get_width()//2, 290))
    pantalla.blit(iniciar, (ANCHO//2 - iniciar.get_width()//2, 320))

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

    dibujar_fondo()
    pygame.draw.rect(pantalla, ROJO, (p1["x"], p1["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(pantalla, ROJO, (p2["x"], p2["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.circle(pantalla, BLANCO, (int(ball["x"]), int(ball["y"])), ball["radius"])
    pygame.draw.rect(pantalla, AZUL_FONDO, (ANCHO//2 - 5, 200, 10, 200))

    mostrar_texto(f"{p1_score}", AZUL_FONDO, 50, 20)
    mostrar_texto(f"{p2_score}", AZUL_FONDO, 730, 20)

    if juego_terminado:
        texto = "¡Jugador 1 gana!" if p1_score > p2_score else "¡Jugador 2 gana!"
        mostrar_texto(texto, ROJO, ANCHO//2 - 100, 100)
        mostrar_texto("Presiona R para reiniciar", AZUL_FONDO, ANCHO//2 - 140, 140)

    pygame.display.flip()


## BETA