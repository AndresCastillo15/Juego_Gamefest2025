import pygame
import sys

# Inicializar Pygame
pygame.init()

# Tamaño de la ventana
ANCHO = 800
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Beach Volly")

# Colores
AZUL_CIELO = (135, 206, 235)
DORADO = (213, 173, 25)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
MARRON = (218, 113, 15)
VERDE = (34, 139, 34)
ROJO = (194, 11, 11)
AZUL_FUERTE = (2, 6, 149)
NEGRO = (0, 0, 0)

# Fuente para pantalla inicial
fuente_grande = pygame.font.SysFont("Arial", 60)
fuente_pequena = pygame.font.SysFont("Arial", 30)

# Mostrar pantalla de inicio
def mostrar_inicio():
    pantalla.fill((50, 150, 255))
    titulo = fuente_grande.render("Beach Volly", True, BLANCO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))
    texto1 = fuente_pequena.render("Voleibol con figuras geométricas", True, BLANCO)
    pantalla.blit(texto1, (ANCHO//2 - texto1.get_width()//2, 160))
    autores = fuente_pequena.render("Por: Andres, Carlos, Eyersson", True, BLANCO)
    pantalla.blit(autores, (ANCHO//2 - autores.get_width()//2, 220))
    colegio = fuente_pequena.render("San José de Guanentá - 2025", True, BLANCO)
    pantalla.blit(colegio, (ANCHO//2 - colegio.get_width()//2, 260))
    continuar = fuente_pequena.render("Presiona ENTER para comenzar", True, NEGRO)
    pantalla.blit(continuar, (ANCHO//2 - continuar.get_width()//2, 330))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

# Mostrar inicio
mostrar_inicio()

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Jugadores
PLAYER_SIZE = 50
GROUND_Y = 300
GRAVEDAD = 0.5

def crear_jugador(x):
    return {"x": x, "y": GROUND_Y, "vel": 5, "saltando": False, "vel_salto": 10}

p1 = crear_jugador(100)
p2 = crear_jugador(650)

# Pelota
pelota = {"x": ANCHO // 2, "y": 200, "radio": 15, "vel_x": 4, "vel_y": 0}

# Funciones de movimiento
def mover_jugador(j, izq, der, salto, teclas, min_x, max_x):
    if teclas[izq] and j["x"] > min_x:
        j["x"] -= j["vel"]
    if teclas[der] and j["x"] + PLAYER_SIZE < max_x:
        j["x"] += j["vel"]
    if teclas[salto] and not j["saltando"]:
        j["saltando"] = True
        j["vel_salto"] = 10

def actualizar_salto(j):
    if j["saltando"]:
        j["y"] -= j["vel_salto"]
        j["vel_salto"] -= GRAVEDAD
        if j["y"] >= GROUND_Y:
            j["y"] = GROUND_Y
            j["saltando"] = False

def colision_jugador(j, bola):
    rect_j = pygame.Rect(j["x"], j["y"], PLAYER_SIZE, PLAYER_SIZE)
    rect_b = pygame.Rect(bola["x"] - bola["radio"], bola["y"] - bola["radio"], bola["radio"]*2, bola["radio"]*2)
    if rect_j.colliderect(rect_b):
        bola["vel_x"] *= -1
        bola["vel_y"] = -7

def colision_red(bola):
    red = pygame.Rect(ANCHO//2 - 5, 200, 10, 200)
    rect_b = pygame.Rect(bola["x"] - bola["radio"], bola["y"] - bola["radio"], bola["radio"]*2, bola["radio"]*2)
    if rect_b.colliderect(red):
        if bola["x"] < ANCHO // 2:
            bola["x"] = ANCHO//2 - 5 - bola["radio"]
        else:
            bola["x"] = ANCHO//2 + 5 + bola["radio"]
        bola["vel_x"] *= -1

# Dibujar fondo y decoraciones
def dibujar_fondo():
    pantalla.fill(AZUL_CIELO)
    pygame.draw.rect(pantalla, DORADO, (0, 350, ANCHO, 50))  # Arena
    pygame.draw.circle(pantalla, AMARILLO, (700, 50), 30)    # Sol
    pygame.draw.rect(pantalla, MARRON, (100, 250, 15, 100))  # Árbol
    pygame.draw.circle(pantalla, VERDE, (108, 230), 40)
    pygame.draw.rect(pantalla, MARRON, (680, 270, 15, 100))
    pygame.draw.circle(pantalla, VERDE, (688, 250), 40)

# Bucle principal
while True:
    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    mover_jugador(p1, pygame.K_a, pygame.K_d, pygame.K_w, teclas, 0, ANCHO//2 - 10)
    mover_jugador(p2, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, teclas, ANCHO//2 + 10, ANCHO)

    actualizar_salto(p1)
    actualizar_salto(p2)

    pelota["x"] += pelota["vel_x"]
    pelota["y"] += pelota["vel_y"]
    pelota["vel_y"] += 0.2

    if pelota["x"] - pelota["radio"] <= 0 or pelota["x"] + pelota["radio"] >= ANCHO:
        pelota["vel_x"] *= -1
    if pelota["y"] + pelota["radio"] >= GROUND_Y + PLAYER_SIZE:
        pelota["y"] = GROUND_Y + PLAYER_SIZE - pelota["radio"]
        pelota["vel_y"] *= -0.7

    colision_jugador(p1, pelota)
    colision_jugador(p2, pelota)
    colision_red(pelota)

    dibujar_fondo()
    pygame.draw.rect(pantalla, ROJO, (p1["x"], p1["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(pantalla, ROJO, (p2["x"], p2["y"], PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.circle(pantalla, BLANCO, (int(pelota["x"]), int(pelota["y"])), pelota["radio"])
    pygame.draw.rect(pantalla, AZUL_FUERTE, (ANCHO//2 - 5, 200, 10, 200))  # Red

    pygame.display.flip()
