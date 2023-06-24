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
back = pygame.image.load("mapaProyecto1.jpg")

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
        print("Recognized text:", recognized_text)

        # Process recognized text and move the player accordingly
        if  recognized_text.upper() in ["A", "B", "C", "D", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]:
            target_positions = get_player_positions(recognized_text)
            x, y = player.rect.x, player.rect.y

            for target_position in target_positions:
                target_x, target_y = target_position
                
                if x == target_x and y == target_y:
                    print("Already at the target position.")
                else:
                    print("Enters here")
                    print(target_x, target_y)
                    
                    path = bfs((x, y), target_position)
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
                        print("No path found.")
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
