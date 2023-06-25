
import os
import sys
import random
import pygame
import speech_recognition as sr
from collections import deque

class Player(object):
    def __init__(self, initial_position):
        self.rect = pygame.Rect(initial_position[0], initial_position[1], 16, 16)

    def move(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if not collides_with_walls(new_rect):
            self.rect = new_rect

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)

def collides_with_walls(rect):
    for wall in walls:
        if rect.colliderect(wall.rect):
            return True
    return False

def bfs(start, target):
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

        x, y = current
        neighbors = [(x-18, y), (x+18, y), (x, y-18), (x, y+18)]

        for neighbor in neighbors:
            if neighbor not in visited and not collides_with_walls(pygame.Rect(neighbor[0], neighbor[1], 16, 16)):
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)

    return None

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((730, 520))

clock = pygame.time.Clock()
walls = []
player = Player((18,108))

# Holds the level layout in a matrix of arrays.
level = [
    list("                                         "),
    list("                                         "),
    list("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"),
    list("WWWWW WWWWWWWWWWWW WWWWWWWWWWWWWWW WWWWWW"),
    list("WWWWW WWWWWWWWWWWW WWWWWWWWWWWWWWWHWWWWWW"),
    list("WWWWW WWWWWWWWWWWW WWWWWWWWWWWWWWW WWWWWW"),
    list("WA                                      W"),
    list("WWWWW WWWWWWWWWWWW WWWWWWWWWWWWWWW WWWWWW"),
    list("WWWWWBWWWWWWWWWWWW WWWWWWWWWWWWWWW WWWWWW"),
    list("WWWWW WWWWWWWWWWWW WWWWWWWWWWWWWWW WWWWWW"),
    list("WWWWW WWWWWWWWWWWW WWWWWWWWWWWWWWW WWWWWW"),
    list("WWWWW WWWW   G                          W"),
    list("WWWWW WWWW WWWWWWW WWWWWWWWWWWWWWWWWWW  W"),
    list("WWWWW WWWW WWWWWWW WWWWWWWWWWWWWWWWWWW IW"),
    list("WWWWW WWWW WWWWWW  WWWWWWWWWWWWWWWWWWW  W"),
    list("WWWWW WWWW WWWWW     WWWWWWWWWWWWWWWW  WW"),
    list("WWWWW  WWW WWWWW WWW                  WWW"),
    list("W         O      WWWE   N             WWW"),
    list("WWWWW WWWW WWWWW  J  WWWWWW WWWW WWW  WWW"),
    list("WWWWW WWWW WWWWWW   WWWWWWW WWWWPWWWW  WW"),
    list("WWWWWCWWWW WWWWWWW WWWWWWWW WWWW WWWWW  W"),
    list("WWWWW WWWW WWWWWWW WWWWWWWWLWWWW WWWWWW W"),
    list("WWWWW WWWW WWWWWWW WWWWWWWW WWWW WWWWWWWW"),
    list("W  D               WWWWWWWW         Q   W"),
    list("WWWWW WWWW WWWWWWWKWWWWWWWW WWWW WWWWWWWW"),
    list("WWWWW WWWWFWWWWWWW WWWWWWWW WWWW WWWWWWWW"),
    list("WWWWW WWWW WWWWWWW WWWWWWWW WWWW WWWWWWWW"),
    list("WWWWW WWWW WWWWWWW WWWWWWWW WWWW WWWWWWWW"),
    list("W  M               WWWWWWWW        R    W"),
    list("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
]

# Find empty positions
def find_empty_positions():
    empty_positions = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] != "W":
                empty_positions.append((x * 18, y * 18))
    return empty_positions

empty_positions = find_empty_positions()

def get_player_positions(recognized_text):
    positions = []
    for char in recognized_text:
        if char.isalpha():
            target_char = char.lower()
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x].lower() == target_char:
                        positions.append((x * 18, y * 18))
    return positions


# Load the transparent image
transparent_image = pygame.Surface((10, 10), pygame.SRCALPHA)
transparent_image.fill((0, 0, 0, 0))

# Parse the level matrix. W = wall
for y in range(len(level)):
    for x in range(len(level[y])):
        if level[y][x] == "W":
            Wall((x * 18, y * 18))

running = True
back = pygame.image.load("ReconocimientoDeVoz/mapaProyecto1.jpg")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Voice command recognition
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="es-ES")
        print("Recognized text:", recognized_text.lower())
        x, y = player.rect.x, player.rect.y
        target_position=(36,108)
        target_x, target_y = target_position
        # Process recognized text and move the player accordingly
        if ("calle" in recognized_text.lower() or "avenida" in recognized_text.lower()) and not "esquina" in recognized_text.lower():
            
            if "profe inolvidable" in recognized_text.lower():
                target_position=(36,108)
            elif "del vocabulario" in recognized_text.lower():
                target_position=(432,108)
            elif "del ser y estar" in recognized_text.lower():
                target_position=(216,198)
            elif "del institutocervantes" in recognized_text.lower():
                target_position=(450,198)
            elif "hablo español" in recognized_text.lower():
                target_position=(126,306)
            elif "del del profeDeEle.es" in recognized_text.lower():
                target_position=(504,306)
            elif "del sustantivo" in recognized_text.lower():
                target_position=(144,414)
            elif "del me gusta" in recognized_text.lower():
                target_position=(612,414)
            elif "de los errores" in recognized_text.lower():
                target_position=(612,414)
            elif "por y para" in recognized_text.lower():
                target_position=(612,414)
            elif "de las dudas" in recognized_text.lower():
                target_position=(612,90)
            elif "de los verbos" in recognized_text.lower():
                target_position=(486,414)

        elif "esquina" in recognized_text.lower():
            if "profe inolvidable"  in recognized_text.lower() and "adjetivo" in recognized_text.lower():
                target_position=(90,108)
            elif "hablo español" in recognized_text.lower() and "adjetivo" in recognized_text.lower():
                target_position=(90,306)
            elif "sustantivo" in recognized_text.lower() and "siele" in recognized_text.lower():
                target_position=(90,414)
            elif "errores" in recognized_text.lower() and "siele" in recognized_text.lower():
                target_position=(90,504)
            elif "deberes hechos" in recognized_text.lower() and "errores" in recognized_text.lower():
                target_position=(180,504)
            elif "deberes hechos" in recognized_text.lower() and "sustantivo" in recognized_text.lower():
                target_position=(180,414)
            elif "deberes hechos" in recognized_text.lower() and "hablo español" in recognized_text.lower():
                target_position=(180,306)
            elif "deberes hechos" in recognized_text.lower() and "ser y estar" in recognized_text.lower():
                target_position=(180,198)
            elif "errores" in recognized_text.lower() and "indicativo" in recognized_text.lower():
                target_position=(324,504)
            elif "sustantivo" in recognized_text.lower() and "indicativo" in recognized_text.lower():
                target_position=(324,414)
            elif "ser y estar"  in recognized_text.lower() and "subjuntivo" in recognized_text.lower():
                target_position=(324,342)
            elif "profe inolvidable" in recognized_text.lower() and "subjuntivo" in recognized_text.lower():
                target_position=(324,198)
            elif "vocabulario" in recognized_text.lower() and "subjuntivo" in recognized_text.lower():
                target_position=(324,108)
            elif "vocabulario" in recognized_text.lower() and "dudas" in recognized_text.lower():
                target_position=(612,108)
            elif "instituto cervantes" in recognized_text.lower() and "dudas" in recognized_text.lower():
                target_position=(612,198)
            elif "profedeele.es" in recognized_text.lower() and "verbos" in recognized_text.lower():
                target_position=(486,306)
            elif "por y para" in recognized_text.lower() and "verbos" in recognized_text.lower():
                target_position=(486,504)
            elif "por y para" in recognized_text.lower() and "gramatica" in recognized_text.lower():
                target_position=(576,504)
            elif "me gusta" in recognized_text.lower() and "gramatica" in recognized_text.lower():
                target_position=(576,414)
            elif "me gusta" in recognized_text.lower() and "verbos" in recognized_text.lower():
                target_position=(486,414)
        
        else:
            if "juguetería"  in recognized_text.lower():
                target_position=(36,108)
            elif "lavandería" in recognized_text.lower():
                target_position=(144,108)
            elif "frutería" in recognized_text.lower():
                target_position=(234,108)
            elif "supermercado" in recognized_text.lower():
                target_position=(288,108)
            elif "restaurante" in recognized_text.lower():
                target_position=(360,108)
            elif "panadería" in recognized_text.lower():
                target_position=(432,108)
            elif "pescadería" in recognized_text.lower():
                target_position=(522,108)
            elif "vetenerinario" in recognized_text.lower():
                target_position=(576,108)
            elif "gasolinería" in recognized_text.lower():
                target_position=(666,108)
            elif "escuela" in recognized_text.lower():
                target_position=(90,180)
            elif "carnicería" in recognized_text.lower():
                target_position=(90,180)
            elif "tienda de instrumentos" in recognized_text.lower():
                target_position=(216,198)
            elif "librería" in recognized_text.lower():
                target_position=(270,198)
            elif "sala de conciertos" in recognized_text.lower():
                target_position=(378,198)
            elif "cine" in recognized_text.lower():
                target_position=(450,198)
            elif "quiosco" in recognized_text.lower():
                target_position=(522,198)
            elif "academia de idiomas" in recognized_text.lower():
                target_position=(576,198)
            elif "pizzería" in recognized_text.lower():
                target_position=(684,198)
            elif "aparcamiento" in recognized_text.lower():
                target_position=(90,234)
            elif "iglesia" in recognized_text.lower():
                target_position=(180,234)
            elif "ayuntamiento" in recognized_text.lower():
                target_position=(324,234)
            elif "cafetería" in recognized_text.lower():
                target_position=(180,306)
            elif "herboristería" in recognized_text.lower():
                target_position=(126,306)
            elif "correos" in recognized_text.lower():
                target_position=(234,306)
            elif "parada de autobus" in recognized_text.lower():
                target_position=(234,306)
            elif "banco" in recognized_text.lower():
                target_position=(450,306)
            elif "embajada" in recognized_text.lower():
                target_position=(504,306)
            elif "hotel" in recognized_text.lower():
                target_position=(558,306)
            elif "comisaría de policía" in recognized_text.lower():
                target_position=(630,306)
            elif "monumento" in recognized_text.lower():
                target_position=(666,306)
            elif "estación de bomberos" in recognized_text.lower():
                target_position=(540,414)
            elif "museo" in recognized_text.lower():
                target_position=(144,414)
            elif "hospital" in recognized_text.lower():
                target_position=(216,414)
            elif "floristería" in recognized_text.lower():
                target_position=(288,414)
            elif "parque ele" in recognized_text.lower() or "biblioteca" in recognized_text.lower() or "teatro" in recognized_text.lower():
                target_position=(324,414)
            elif "universidad" in recognized_text.lower():
                target_position=(540,414)
            elif "bar" in recognized_text.lower():
                target_position=(612,414)
            elif "estación de tren" in recognized_text.lower():
                target_position=(684,414)
            elif "peluquería" in recognized_text.lower():
                target_position=(540,504)
            elif "centro comercial" in recognized_text.lower():
                target_position=(144,504)
            elif "farmacia" in recognized_text.lower():
                target_position=(270,504)
            elif "tienda de ropa" in recognized_text.lower():
                target_position=(558,504)
            elif "casa de pepe" in recognized_text.lower():
                target_position=(630,504)
            elif "ambulatorio" in recognized_text.lower():
                target_position=(684,504)
        #for target_position in target_positions:
        target_x, target_y = target_position
        if x == target_x and y == target_y:
            print("Ya se encuentra en el lugar")
        else:    
            path = bfs((x, y),target_position)
        if path:
                    for step in path:
                        x, y = step
                        player.move(x - player.rect.x, y - player.rect.y)
                        pygame.time.delay(100)  # Delay between each step
                        # Draw the scene after each step
                        screen.blit(back, (0, 0, 1000, 540))
                        for wall in walls:
                            screen.blit(transparent_image, wall.rect)
                        pygame.draw.rect(screen, (255, 20, 0), player.rect)
                        pygame.display.flip()
        else:
                    print("No se encontró un camino")
        print("Player Position:", player.rect.x, player.rect.y)
    except sr.UnknownValueError:
        print("Unable to recognize audio.")
    except sr.RequestError as e:
        print("Error occurred during recognition:", str(e))

    # Draw the scene
    screen.blit(back, (0, 0, 1000, 540))
    for wall in walls:
        screen.blit(transparent_image, wall.rect)
    pygame.draw.rect(screen, (255, 20, 0), player.rect)
    pygame.display.flip()

pygame.quit()
