import pygame

#Clase que representa un disparo láser
class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad, alto_pantalla):
        super().__init__()

        #Crea la superficie del láser
        self.image = pygame.Surface((4, 15))
        self.image.fill((243, 216, 63))  #Color amarillo
        self.rect = self.image.get_rect(center=posicion)  #Posición inicial

        self.velocidad = velocidad  #Velocidad vertical del láser
        self.alto_pantalla = alto_pantalla  #Límite de la pantalla

    def update(self):
        self.rect.y -= self.velocidad  #Mueve el láser en Y

        #Elimina el láser si sale de la pantalla
        if self.rect.y > self.alto_pantalla + 15 or self.rect.y < 0:
            self.kill()
