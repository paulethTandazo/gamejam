import pygame
import sys
import random
from typing import Callable, Iterator

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
ancho = 600
alto = 500
size = (ancho, alto)

# Crear la ventana
pygame.display.set_caption("mi primer juego")
screen = pygame.display.set_mode(size)

# Definir colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
gris_oscuro = (64, 64, 64)
gris_claro = (192, 192, 192)

# Fuente para el texto de la historia y botones
fuente = pygame.font.Font(None, 24)  # Fuente más pequeña

# Definir la historia y las imágenes correspondientes (JPG)
historia = [
    "El mundo que una vez estuvo lleno de vida ahora es una sombra de lo que fue...",
    "En su interminable caminar por el mundo destruido, el chico se detiene...",
    "Con la semilla en sus manos, el chico siente una nueva responsabilidad...",
    "De rodillas en el suelo de su humilde hogar, el chico cava cuidadosamente...",
    "Han pasado seis meses desde que el chico encontró y plantó la semilla..."
]

# Cargar las imágenes de la historia (formato JPG)
imagenes_historia = [
    pygame.image.load("gamejam/PantallaInicio.jpg"),
    pygame.image.load("gamejam/ChicoConPlantita.jpg"),
    pygame.image.load("gamejam/LlegandoCasa.jpg"),
    pygame.image.load("gamejam/PlantandoPlanta.jpg"),
    pygame.image.load("gamejam/6meses.jpg")
]

# Redimensionar las imágenes para que se ajusten a la ventana (parte superior)
imagenes_historia = [pygame.transform.scale(img, (ancho, alto // 2)) for img in imagenes_historia]

# Cargar la imagen de fondo para la pantalla de inicio
fondo_inicio = pygame.image.load("gamejam/background.png")
fondo_inicio = pygame.transform.scale(fondo_inicio, size)  # Ajustar la imagen al tamaño de la ventana

# Variables de control de la historia
indice_historia = 0
texto_actual = ""  # Texto que se va escribiendo
escribiendo = True  # Controla si estamos escribiendo la historia
contador_letra = 0  # Contador de letras para mostrar una a una

# Estado del juego (inicio o historia)
en_historia = False  # Comienza en la pantalla de inicio
en_pantalla_inicio = True  # Variable para la pantalla de inicio

# Botón para cambiar de imagen y texto en la historia
ancho_boton = 300
alto_boton = 50
x_boton = (ancho - ancho_boton) // 2  # Centrado horizontalmente

# Posición del botón "Start" en la parte inferior
y_boton_start = alto - alto_boton - 30  # Posicionado cerca del borde inferior

# Definir `y_boton` para la historia (justo por encima del borde inferior)
y_boton = alto - alto_boton - 30

fuente_boton = pygame.font.Font(None, 24)  # Fuente para los botones
texto_boton = "Siguiente"
color_texto = blanco
color_boton = gris_oscuro

# Botón "Start" para la pantalla de inicio
texto_boton_start = "Start"

# Función para ajustar el texto dentro de un área específica
def layout_text_in_area(text: str, font_width: Callable[[str], int], width: int) -> Iterator[str]:
    if len(text) == 0:
        yield ""
        return

    start = 0
    end = 0
    while True:
        if end >= len(text):
            yield text[start:]
            return
        substr = text[start:end + 1]
        overflow = font_width(substr)[0] > width  # Tomar solo el ancho
        if overflow:
            if text[end] == ' ':
                yield text[start:end]
                start = end
            else:
                found = False
                for i in range(end - 1, start, -1):
                    if text[i] == ' ':
                        yield text[start:i + 1]
                        start = end = i + 1
                        found = True
                        break
                if not found:
                    yield text[start:end]
                    start = end
        else:
            end += 1

# Función para escribir el texto gradualmente (letra por letra)
def escribir_texto_progresivamente(historia_completa, velocidad):
    global contador_letra, texto_actual
    if contador_letra < len(historia_completa):
        texto_actual += historia_completa[contador_letra]
        contador_letra += 1

# Función para dibujar el texto en el área inferior
def dibujar_texto_area(texto, area_ancho):
    lineas = layout_text_in_area(texto, fuente.size, area_ancho)
    y_pos = alto // 2 + 20  # Posición Y inicial para el texto
    for linea in lineas:
        texto_renderizado = fuente.render(linea, True, blanco)
        screen.blit(texto_renderizado, (20, y_pos))  # Posición del texto
        y_pos += 30  # Ajustar la distancia entre las líneas (más pequeño)

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar clic en el botón de la pantalla de inicio o la historia
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if en_pantalla_inicio:
                # Detectar clic en el botón "Start" en la pantalla de inicio
                if x_boton <= evento.pos[0] <= x_boton + ancho_boton and y_boton_start <= evento.pos[1] <= y_boton_start + alto_boton:
                    en_pantalla_inicio = False  # Cambiar a la escena de la historia
                    en_historia = True
            elif en_historia:
                # Detectar clic en el botón de la historia
                if x_boton <= evento.pos[0] <= x_boton + ancho_boton and y_boton <= evento.pos[1] <= y_boton + alto_boton:
                    if indice_historia < len(historia) - 1:
                        indice_historia += 1
                        texto_actual = ""  # Reiniciar el texto actual
                        contador_letra = 0  # Reiniciar el contador de letras
                        escribiendo = True  # Volver a escribir la siguiente parte
                    else:
                        en_historia = False  # Fin de la historia

    # Escena de la pantalla de inicio
    if en_pantalla_inicio:
        # Mostrar la imagen de fondo en lugar del fondo negro
        screen.blit(fondo_inicio, (0, 0))  # Mostrar la imagen de fondo de inicio

        # Dibujar el botón "Start"
        pygame.draw.rect(screen, color_boton, (x_boton, y_boton_start, ancho_boton, alto_boton))
        texto_boton_renderizado = fuente_boton.render(texto_boton_start, True, color_texto)
        screen.blit(texto_boton_renderizado, (x_boton + 100, y_boton_start + 15))

    # Escena de la historia
    elif en_historia:
        # Mostrar la imagen correspondiente en la parte superior
        screen.blit(imagenes_historia[indice_historia], (0, 0))

        # Dibujar el cuadro de texto en la parte inferior
        pygame.draw.rect(screen, negro, (0, alto // 2, ancho, alto // 2))

        # Escribir el texto progresivamente
        if escribiendo:
            escribir_texto_progresivamente(historia[indice_historia], velocidad=2)

        # Dibujar el texto ajustado en pantalla
        dibujar_texto_area(texto_actual, ancho - 40)  # Ajustar el texto dentro de un área más pequeña

        # Cambiar el texto del botón a "Comienza tu aventura" si es la última parte de la historia
        if indice_historia == len(historia) - 1:
            texto_boton = "Comienza tu aventura"
        else:
            texto_boton = "Siguiente"

        # Dibujar el botón
        pygame.draw.rect(screen, color_boton, (x_boton, y_boton, ancho_boton, alto_boton))
        texto_boton_renderizado = fuente_boton.render(texto_boton, True, color_texto)
        screen.blit(texto_boton_renderizado, (x_boton + 20, y_boton + 10))

    # Actualizar la pantalla
    pygame.display.update()
