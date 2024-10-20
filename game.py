import pygame

import sys

import random
 
# Inicializar Pygame

pygame.init()
 
# Definir dimensiones de la ventana

ancho = 1024

alto = 768

size = (ancho, alto)
 
# Crear la ventana

pygame.display.set_caption("mi primer juego")

screen = pygame.display.set_mode(size)
 
# Definir colores

blanco = (255, 255, 255)

negro = (0, 0, 0)

gris_oscuro = (64, 64, 64)

gris_claro = (192, 192, 192)
 
# Fuente para el texto de la historia y el inventario

fuente = pygame.font.Font(None, 40)
 
# Definir la historia y las imágenes correspondientes (JPG)

historia = [

    "Era una noche oscura y tormentosa...",

    "El joven héroe, cansado pero decidido, se levantó.",

    "Sabía que su misión no sería fácil, pero estaba listo.",

    "A lo lejos, una sombra se movía entre los árboles...",

    "¿Sería un amigo o un enemigo? Solo el tiempo lo diría."

]
 
# Cargar las imágenes de la historia (formato JPG)

imagenes_historia = [

    pygame.image.load("imagen1.jpg"),

    pygame.image.load("imagen2.jpg"),

    pygame.image.load("imagen3.jpg"),

    pygame.image.load("imagen4.jpg"),

    pygame.image.load("imagen5.jpg")

]
 
# Redimensionar las imágenes para que se ajusten a la ventana (parte superior)

imagenes_historia = [pygame.transform.scale(img, (ancho, alto // 2)) for img in imagenes_historia]
 
# Variables de control

indice_historia = 0

texto_actual = ""  # Texto que se va escribiendo

escribiendo = True  # Controla si estamos escribiendo la historia

contador_letra = 0  # Contador de letras para mostrar una a una

en_historia = True  # Variable para controlar las escenas (historia/aventura)
 
# Botón para cambiar de imagen y texto

ancho_boton = 300

alto_boton = 50

x_boton = (ancho - ancho_boton) // 2

y_boton = alto - alto_boton - 30
 
fuente_boton = pygame.font.Font(None, 40)

texto_boton = "Siguiente"

color_texto = blanco

color_boton = gris_oscuro
 
# Tamaño del tablero

filas = 8

columnas = 8

tamaño_cuadro = ancho // columnas  # Tamaño de cada cuadro del tablero
 
# Posición inicial del "personaje"

pos_x = 0

pos_y = 0

velocidad = tamaño_cuadro  # El personaje se moverá un cuadro a la vez
 
# Cargar la imagen del personaje (formato PNG)

personaje_img = pygame.image.load("personaje.png")

personaje_img = pygame.transform.scale(personaje_img, (tamaño_cuadro, tamaño_cuadro))  # Ajustar al tamaño del cuadro
 
# Cargar la imagen del objeto (formato PNG)

objeto_img = pygame.image.load("objeto.png")

objeto_img = pygame.transform.scale(objeto_img, (tamaño_cuadro, tamaño_cuadro))  # Ajustar al tamaño del cuadro
 
# Generar posiciones aleatorias para los objetos

num_objetos = 5

objetos = [(random.randint(0, columnas-1) * tamaño_cuadro, random.randint(0, filas-1) * tamaño_cuadro) for _ in range(num_objetos)]
 
# Contador de objetos en el inventario

contador_objetos = 0
 
# Función para escribir el texto gradualmente

def escribir_texto(texto, velocidad):

    global contador_letra, texto_actual

    if contador_letra < len(texto):

        texto_actual += texto[contador_letra]

        contador_letra += 1
 
# Función para dibujar el tablero de ajedrez

def dibujar_tablero():

    for fila in range(filas):

        for columna in range(columnas):

            # Alternar entre gris claro y gris oscuro

            if (fila + columna) % 2 == 0:

                color = gris_claro

            else:

                color = gris_oscuro

            # Dibujar el cuadrado

            pygame.draw.rect(screen, color, pygame.Rect(columna * tamaño_cuadro, fila * tamaño_cuadro, tamaño_cuadro, tamaño_cuadro))
 
# Función para dibujar el "personaje"

def dibujar_personaje():

    # Dibujar la imagen del personaje (PNG) en su posición actual

    screen.blit(personaje_img, (pos_x, pos_y))
 
# Función para dibujar los objetos en el tablero

def dibujar_objetos():

    for objeto in objetos:

        screen.blit(objeto_img, objeto)
 
# Función para comprobar si el personaje ha recogido un objeto

def recoger_objetos():

    global contador_objetos, objetos

    for objeto in objetos:

        if pos_x == objeto[0] and pos_y == objeto[1]:

            objetos.remove(objeto)  # Eliminar el objeto del tablero

            contador_objetos += 1  # Incrementar el inventario

            # Generar un nuevo objeto en una posición aleatoria

            nuevo_objeto = (random.randint(0, columnas-1) * tamaño_cuadro, random.randint(0, filas-1) * tamaño_cuadro)

            objetos.append(nuevo_objeto)
 
# Bucle principal

while True:

    # Manejar eventos

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            pygame.quit()

            sys.exit()
 
        # Detectar clic en el botón para avanzar en la historia o cambiar de escena

        if evento.type == pygame.MOUSEBUTTONDOWN and en_historia:

            if x_boton <= evento.pos[0] <= x_boton + ancho_boton and y_boton <= evento.pos[1] <= y_boton + alto_boton:

                if indice_historia < len(historia) - 1:

                    indice_historia += 1

                    texto_actual = ""  # Reiniciar el texto actual

                    contador_letra = 0  # Reiniciar el contador de letras

                    escribiendo = True  # Volver a escribir la siguiente parte

                else:

                    en_historia = False  # Cambiar a la escena del tablero
 
        # Detectar el movimiento del personaje por teclado (arriba, abajo, izquierda, derecha)

        if evento.type == pygame.KEYDOWN and not en_historia:

            if evento.key == pygame.K_LEFT:

                pos_x = max(0, pos_x - velocidad)  # No salir del tablero

            if evento.key == pygame.K_RIGHT:

                pos_x = min(ancho - tamaño_cuadro, pos_x + velocidad)

            if evento.key == pygame.K_UP:

                pos_y = max(0, pos_y - velocidad)

            if evento.key == pygame.K_DOWN:

                pos_y = min(alto - tamaño_cuadro, pos_y + velocidad)
 
    # Escena de la historia

    if en_historia:

        # Mostrar la imagen correspondiente en la parte superior

        screen.blit(imagenes_historia[indice_historia], (0, 0))
 
        # Dibujar el cuadro de texto en la parte inferior

        pygame.draw.rect(screen, negro, (0, alto // 2, ancho, alto // 2))
 
        # Escribir el texto progresivamente

        if escribiendo:

            escribir_texto(historia[indice_historia], velocidad=2)  # Velocidad de escritura
 
        # Dibujar el texto en pantalla

        texto_renderizado = fuente.render(texto_actual, True, blanco)

        screen.blit(texto_renderizado, (50, alto // 2 + 50))
 
        # Cambiar el texto del botón a "Comienza tu aventura" si es la última parte de la historia

        if indice_historia == len(historia) - 1:

            texto_boton = "Comienza tu aventura"

        else:

            texto_boton = "Siguiente"
 
        # Dibujar el botón

        pygame.draw.rect(screen, color_boton, (x_boton, y_boton, ancho_boton, alto_boton))

        texto_boton_renderizado = fuente_boton.render(texto_boton, True, color_texto)

        screen.blit(texto_boton_renderizado, (x_boton + 20, y_boton + 10))
 
    # Escena de la aventura (tablero con movimiento del personaje)

    else:

        # Dibujar el tablero de ajedrez

        dibujar_tablero()
 
        # Dibujar el "personaje" (imagen PNG)

        dibujar_personaje()
 
        # Dibujar los objetos en el tablero

        dibujar_objetos()
 
        # Comprobar si el personaje ha recogido algún objeto

        recoger_objetos()
 
        # Mostrar el contador de objetos recogidos en la pantalla

        texto_inventario = fuente.render(f"Objetos en inventario: {contador_objetos}", True, blanco)

        screen.blit(texto_inventario, (50, alto - 50))
 
    # Actualizar la pantalla

    pygame.display.update()

 