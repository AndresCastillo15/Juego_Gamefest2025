import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
ANCHO = 800
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("VolleyBash - Pantalla Inicial")

# Colores
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)
NEGRO = (0, 0, 0)

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 60)
fuente_texto = pygame.font.SysFont("Arial", 30)

# Función para mostrar la pantalla inicial
def mostrar_pantalla_inicial():
    pantalla.fill(AZUL)
    
    # Título
    titulo = fuente_titulo.render("VolleyBash", True, BLANCO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))
    
    # Subtítulo
    subtitulo = fuente_texto.render("Un juego de voleibol con figuras geométricas", True, BLANCO)
    pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 180))

    # Autores
    autores = fuente_texto.render("Creado por: Andres Castillo, Carlos Galvis, Eyersson Montaña", True, BLANCO)
    pantalla.blit(autores, (ANCHO // 2 - autores.get_width() // 2, 250))

    colegio = fuente_texto.render("Colegio San José de Guanentá - 2025", True, BLANCO)
    pantalla.blit(colegio, (ANCHO // 2 - colegio.get_width() // 2, 290))

    # Instrucción para continuar
    instruccion = fuente_texto.render("Presiona ENTER para comenzar", True, NEGRO)
    pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, 500))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

# Ejecutar pantalla inicial
mostrar_pantalla_inicial()

# Aquí iría el resto del código del juego (main loop)
print("¡Comienza el juego!")


## BETA