import pygame

# Clase que representa un disparo (láser)
class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad, alto_pantalla):
        super().__init__()  # Inicializa la clase base Sprite

        # Crear la superficie del láser: un rectángulo de 4x15 píxeles
        self.imagen = pygame.Surface((4, 15))
        self.imagen.fill((243, 216, 63))  # Color amarillo

        # Obtener el rectángulo de colisión centrado en la posición recibida
        self.rectangulo = self.imagen.get_rect(center=posicion)

        self.velocidad = velocidad  # Velocidad del láser (negativa hacia arriba)
        self.alto_pantalla = alto_pantalla  # Límite vertical de la pantalla

    # Método que actualiza la posición del láser
    def actualizar(self):
        # Mover el láser en el eje Y
        self.rectangulo.y -= self.velocidad

        # Eliminar el láser si sale de la pantalla
        if self.rectangulo.y > self.alto_pantalla + 15 or self.rectangulo.y < 0:
            self.kill()  # Quita el sprite del grupo