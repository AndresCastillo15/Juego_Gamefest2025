import pygame
import sys

# Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Beach Volly")
clock = pygame.time.Clock()

# Constantes
PLAYER_SIZE = 50
GROUND_Y = 300
GRAVITY = 0.5
PUNTOS_MAX = 3
DELAY_PELOTA = 60

# Fuente de texto
font = pygame.font.SysFont("Arial", 30, bold=True)

# Cargar imágenes
logo = pygame.image.load("img/logo.png")
logo = pygame.transform.scale(logo, (150, 150))

fondo = pygame.image.load("img/cancha.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

player1_img = pygame.image.load("img/player1.png")
player1_img = pygame.transform.scale(player1_img, (150, 150))

player2_img = pygame.image.load("img/player2.png")
player2_img = pygame.transform.scale(player2_img, (150, 150))

# Cargar sonidos
pygame.mixer.music.load("sonidos/canciondefondo.mp3")
pygame.mixer.music.play(-1)

sonido_pelota = pygame.mixer.Sound("sonidos/pelota.mp3")

# Funciones
def crear_jugador(x):
    return {"x": x, "y": GROUND_Y - 10, "vel": 5, "is_jumping": False, "jump_vel": 10}

def reiniciar_pelota(hacia_izquierda):
    return {
        "x": ANCHO // 2,
        "y": 150,
        "radius": 15,
        "vel_x": -4 if hacia_izquierda else 4,
        "vel_y": 0,
        "min_rebote": 1
    }

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

def verificar_colision(j, pelota, jugador_actual):
    jr = pygame.Rect(j["x"], j["y"], PLAYER_SIZE, PLAYER_SIZE)
    pr = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"], pelota["radius"]*2, pelota["radius"]*2)
    if jr.colliderect(pr) and jugador_actual != j:
        pelota["vel_x"] = 4 if j == p1 else -4
        pelota["vel_x"] *= 1.05
        pelota["vel_y"] = -7 * pelota["min_rebote"]
        pelota["min_rebote"] = min(pelota["min_rebote"] + 0.05, 1.5)
        sonido_pelota.play()
        return j
    return jugador_actual

def verificar_colision_red(pelota):
    red = pygame.Rect(ANCHO//2 - 5, 200, 10, 200)
    pr = pygame.Rect(pelota["x"] - pelota["radius"], pelota["y"] - pelota["radius"], pelota["radius"]*2, pelota["radius"]*2)
    if pr.colliderect(red):
        pelota["vel_x"] *= -1
        if pelota["x"] < ANCHO//2:
            pelota["x"] = ANCHO//2 - pelota["radius"] - 6
        else:
            pelota["x"] = ANCHO//2 + 6 + pelota["radius"]

def dibujar_fondo():
    pantalla.blit(fondo, (0, 0))

def mostrar_texto(txt, color, x, y):
    contorno = 3
    negro = (0, 0, 0)
    for dx in range(-contorno, contorno+1):
        for dy in range(-contorno, contorno+1):
            if dx != 0 or dy != 0:
                render = font.render(txt, True, negro)
                pantalla.blit(render, (x+dx, y+dy))
    render = font.render(txt, True, color)
    pantalla.blit(render, (x, y))

# Inicialización
p1, p2 = crear_jugador(100), crear_jugador(650)
ball = reiniciar_pelota(False)
p1_score, p2_score = 0, 0
juego_terminado = False
contador_reinicio = 0
ultimo_golpeador = None

# Pantalla inicial
mostrar_pantalla = True
while mostrar_pantalla:
    dibujar_fondo()
    pantalla.blit(logo, (ANCHO//2 - 75, 20))

    titulo = "Beach Volly"
    mostrar_texto(titulo, (255, 255, 255), ANCHO//2 - font.size(titulo)[0]//2, 180)

    subtitulo = "Un juego de voleibol con figuras geométricas"
    mostrar_texto(subtitulo, (255, 255, 255), ANCHO//2 - font.size(subtitulo)[0]//2, 220)

    autores = "Andres Castillo, Carlos Galvis, Eyersson Montaña"
    mostrar_texto(autores, (255, 255, 255), ANCHO//2 - font.size(autores)[0]//2, 260)

    colegio = "Colegio San José de Guanentá - 2025"
    mostrar_texto(colegio, (255, 255, 255), ANCHO//2 - font.size(colegio)[0]//2, 290)

    iniciar = "Presiona ENTER para comenzar"
    mostrar_texto(iniciar, (2, 6, 149), ANCHO//2 - font.size(iniciar)[0]//2, 320)

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            mostrar_pantalla = False

# Bucle principal
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
                    ultimo_golpeador = None
                else:
                    p1_score += 1
                    contador_reinicio = DELAY_PELOTA
                    ball = reiniciar_pelota(True)
                    ultimo_golpeador = None

            ultimo_golpeador = verificar_colision(p1, ball, ultimo_golpeador)
            ultimo_golpeador = verificar_colision(p2, ball, ultimo_golpeador)
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
            ultimo_golpeador = None

    # Dibujo
    dibujar_fondo()

    # Jugadores
    img_offset_x = (150 - PLAYER_SIZE) // 2
    img_offset_y = (150 - PLAYER_SIZE)
    pantalla.blit(player1_img, (p1["x"] - img_offset_x, p1["y"] - img_offset_y))
    pantalla.blit(player2_img, (p2["x"] - img_offset_x, p2["y"] - img_offset_y))

    # Pelota
    pygame.draw.circle(pantalla, (255, 255, 255), (int(ball["x"]), int(ball["y"])), ball["radius"])

    # Red simple - bloque gris claro neutro
    pygame.draw.rect(pantalla, (190, 190, 190), (ANCHO//2 - 5, 200, 10, 200))

    # Puntos
    mostrar_texto(f"{p1_score}", (255, 0, 0), 50, 20)
    mostrar_texto(f"{p2_score}", (255, 0, 0), 730, 20)

    if juego_terminado:
        texto = "¡Jugador 1 gana!" if p1_score > p2_score else "¡Jugador 2 gana!"
        mostrar_texto(texto, (194, 11, 11), ANCHO//2 - 100, 100)
        mostrar_texto("Presiona R para reiniciar", (2, 6, 149), ANCHO//2 - 140, 140)

    pygame.display.flip()
