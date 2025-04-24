import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle, grid
from alien import Alien, MysteryShip
from laser import Laser
from ranking import guardar_ranking

# Clase principal para el modo de un jugador
class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        # Inicialización de la nave del jugador
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(screen_width, screen_height, offset))

        self.obstacles = self.create_obstacles()  # Lista de obstáculos
        self.aliens_group = pygame.sprite.Group()  # Grupo de alienígenas
        self.create_aliens()
        self.aliens_direction = 1  # Dirección del movimiento alienígena
        self.alien_lasers_group = pygame.sprite.Group()  # Disparos de los alienígenas
        self.mystery_ship_group = pygame.sprite.GroupSingle()  # Nave misteriosa
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.nombre_jugador = ""

        self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
        self.load_highscore()
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    # Crea los obstáculos a partir del grid
    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    # Crea los alienígenas organizados en filas
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55
                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1
                alien = Alien(alien_type, x + self.offset / 2, y)
                self.aliens_group.add(alien)

    # Mueve a los alienígenas y cambia su dirección al llegar a un borde
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)
        for alien in self.aliens_group:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    # Baja los alienígenas en la pantalla
    def alien_move_down(self, distance):
        for alien in self.aliens_group:
            alien.rect.y += distance

    # Un alienígena aleatorio dispara un láser
    def alien_shoot_laser(self):
        if self.aliens_group:
            alien = random.choice(self.aliens_group.sprites())
            laser = Laser(alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser)

    # Crea la nave misteriosa
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    # Maneja todas las colisiones posibles
    def check_for_collisions(self):
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        for laser_sprite in self.alien_lasers_group:
            if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                laser_sprite.kill()
                self.lives -= 1
                if self.lives == 0:
                    self.game_over()
            for obstacle in self.obstacles:
                if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                    laser_sprite.kill()

        for alien in self.aliens_group:
            for obstacle in self.obstacles:
                pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)
            if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                self.game_over()

    # Acción cuando termina el juego
    def game_over(self):
        self.run = False
        guardar_ranking(self.nombre_jugador, self.score)

    # Reinicia el juego
    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    # Verifica si el puntaje actual es el más alto
    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    # Carga el puntaje más alto guardado
    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0
