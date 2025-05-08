import pygame
import sys

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
cian = (0, 255, 255)
gris = (130, 131, 128)
gris_oscuro = (63, 63, 63)
amarillo = (240, 255, 0)
rojo = (194, 11, 11)
dorado = (213, 173, 25)
marron = (218, 113, 15)
azul = (2, 6, 149)
verde = (34, 139, 34)  # Verde para las palmeras
azul_claro = (135, 206, 235)  # Cielo azul claro

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Voleibol de Playa")

# Reloj para controlar la tasa de actualización
clock = pygame.time.Clock()

# Función para dibujar el fondo de la playa
def draw_background():
    # Cielo
    ventana.fill(azul_claro)

    # Arena (parte inferior)
    pygame.draw.rect(ventana, dorado, (0, 400, 800, 200))

    # Olas (dibujadas con círculos)
    for i in range(5):
        pygame.draw.circle(ventana, blanco, (i * 160 + 80, 450), 30, 0)
        pygame.draw.circle(ventana, blanco, (i * 160 + 120, 460), 30, 0)

    # Detalles: Palmera en el lado izquierdo
    pygame.draw.rect(ventana, marron, (100, 300, 20, 100))  # Tronco
    pygame.draw.circle(ventana, verde, (110, 280), 50, 0)  # Copa de la palmera

    # Detalles: Palmera en el lado derecho
    pygame.draw.rect(ventana, marron, (650, 320, 20, 100))  # Tronco
    pygame.draw.circle(ventana, verde, (660, 290), 50, 0)  # Copa de la palmera

    # Sol (en el horizonte)
    pygame.draw.circle(ventana, amarillo, (700, 100), 60, 0)

# Bucle principal
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar el fondo
        draw_background()

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar FPS
        clock.tick(60)

if __name__ == "__main__":
    main()
