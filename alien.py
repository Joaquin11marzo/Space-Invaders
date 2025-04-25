import pygame, random

# Clase que representa a un alienígena enemigo
class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type  # Tipo de alien (1, 2 o 3)
        path = f"Graphics/alien_{type}.png"  # Ruta de la imagen correspondiente según el tipo
        self.image = pygame.image.load(path)  # Carga la imagen del alien
        self.rect = self.image.get_rect(topleft=(x, y))  # Define la posición inicial del alien

    def update(self, direction):
        self.rect.x += direction  # Mueve el alien horizontalmente según la dirección indicada

# Clase que representa una nave misteriosa que aparece aleatoriamente
class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width  # Ancho de la pantalla para determinar límites
        self.offset = offset  # Margen lateral
        self.image = pygame.image.load("Graphics/mystery.png")  # Carga la imagen de la nave misteriosa

        # Posición inicial aleatoria: entra desde izquierda o derecha
        x = random.choice([self.offset/2, self.screen_width + self.offset - self.image.get_width()])
        self.speed = 3 if x == self.offset/2 else -3  # Determina la dirección según el punto de entrada
        self.rect = self.image.get_rect(topleft=(x, 90))  # Posición fija en el eje Y (altura)

    def update(self):
        self.rect.x += self.speed  # Mueve la nave horizontalmente según su velocidad

        # Elimina la nave si sale completamente de los límites visibles de la pantalla
        if self.rect.right > self.screen_width + self.offset/2:
            self.kill()  # Elimina el sprite del grupo
        elif self.rect.left < self.offset/2:
            self.kill()
