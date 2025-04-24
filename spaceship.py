import pygame
from laser import Laser

#Clase que representa una nave espacial controlada por un jugador
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset,
                 left_key=pygame.K_LEFT, right_key=pygame.K_RIGHT, shoot_key=pygame.K_UP,
                 image_path="Graphics/spaceship.png"):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # Imagen de la nave
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height - 20))
        self.speed = 6
        self.screen_width = screen_width
        self.offset = offset
        self.lasers_group = pygame.sprite.Group()  #Grupo de disparos
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600  #Tiempo entre disparos en ms
        self.shoot_sound = pygame.mixer.Sound("Sounds/laser.ogg")  #Sonido de disparo
        self.left_key = left_key
        self.right_key = right_key
        self.shoot_key = shoot_key

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.rect.x -= self.speed
        if keys[self.right_key]:
            self.rect.x += self.speed
        if keys[self.shoot_key] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers_group.add(Laser(self.rect.center, 6, self.screen_width))
        self.shoot_sound.play()

    def update(self):
        self.get_keys()
        self.recharge()
        self.lasers_group.update()

    def reset(self):
        self.rect.midbottom = (self.screen_width // 2, self.rect.bottom)
        self.lasers_group.empty()
        self.ready = True
