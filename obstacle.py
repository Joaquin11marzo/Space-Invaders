import pygame

# Clase que representa un bloque individual de un obstáculo
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3,3))  # Cada bloque es un cuadrado pequeño
        self.image.fill((243,216,63))  # Color amarillo brillante
        self.rect = self.image.get_rect(topleft=(x, y))  # Posición del bloque

# Mapa de diseño (grid) para los obstáculos
# 1 indica la presencia de un bloque, 0 indica vacío
grid = [
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
]

# Clase que construye un conjunto de bloques (obstáculo)
class Obstacle:
    def __init__(self, x, y):
        self.blocks_group = pygame.sprite.Group()  # Grupo de bloques que forman el obstáculo
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 1:
                    pos_x = x + column * 3  # Calcula la posición X del bloque
                    pos_y = y + row * 3     # Calcula la posición Y del bloque
                    block = Block(pos_x, pos_y)
                    self.blocks_group.add(block)  # Agrega el bloque al grupo
