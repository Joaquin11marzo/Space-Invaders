import pygame, random

# Clase que representa a un alienígena enemigo
class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type  # Tipo de alien (1, 2 o 3)
        path = f"Graphics/alien_{type}.png"  # Ruta de la imagen correspondiente
        self.image = pygame.image.load(path)  # Carga la imagen
        self.rect = self.image.get_rect(topleft=(x, y))  # Posición inicial

    def update(self, direction):
        self.rect.x += direction  # Mueve el alien horizontalmente

# Clase que representa una nave misteriosa que aparece aleatoriamente
class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("Graphics/mystery.png")  # Imagen de la nave misteriosa

        # Decide si entra desde la izquierda o derecha aleatoriamente
        x = random.choice([self.offset/2, self.screen_width + self.offset - self.image.get_width()])
        self.speed = 3 if x == self.offset/2 else -3  # Dirección de movimiento
        self.rect = self.image.get_rect(topleft=(x, 90))  # Posición fija en Y

    def update(self):
        self.rect.x += self.speed  # Mueve la nave horizontalmente

        # Elimina la nave si sale de los límites de la pantalla
        if self.rect.right > self.screen_width + self.offset/2:
            self.kill()
        elif self.rect.left < self.offset/2:
            self.kill()
