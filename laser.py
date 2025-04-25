import pygame

# Clase que representa un disparo láser
class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad, alto_pantalla):
        super().__init__()

        # Crea una superficie pequeña que representa el láser
        self.image = pygame.Surface((4, 15))  # Tamaño del láser
        self.image.fill((243, 216, 63))  # Color amarillo brillante
        self.rect = self.image.get_rect(center=posicion)  # Posición inicial basada en el centro

        self.velocidad = velocidad  # Velocidad vertical con la que se mueve el láser
        self.alto_pantalla = alto_pantalla  # Altura de la pantalla para verificar límites

    def update(self):
        # Mueve el láser en el eje Y
        self.rect.y -= self.velocidad

        # Si el láser sale de los límites verticales de la pantalla, se elimina
        if self.rect.y > self.alto_pantalla + 15 or self.rect.y < 0:
            self.kill()  # Quita el sprite del grupo al que pertenece
