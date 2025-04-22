import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien, MysteryShip
from laser import Laser

class GameTwoPlayers:
	def __init__(self, screen_width, screen_height, offset):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.offset = offset

		# Dos naves espaciales con controles distintos
		self.spaceships = pygame.sprite.Group()
		self.player1 = Spaceship(screen_width, screen_height, offset, left_key=pygame.K_LEFT, right_key=pygame.K_RIGHT, shoot_key=pygame.K_UP)
		self.player2 = Spaceship(screen_width, screen_height, offset, left_key=pygame.K_a, right_key=pygame.K_d, shoot_key=pygame.K_w)
		self.player2.rect.bottom += 40  # un poco más arriba para diferenciar
		self.spaceships.add(self.player1, self.player2)

		self.obstacles = self.create_obstacles()
		self.aliens_group = pygame.sprite.Group()
		self.create_aliens()
		self.aliens_direction = 1
		self.alien_lasers_group = pygame.sprite.Group()
		self.mystery_ship_group = pygame.sprite.GroupSingle()
		self.lives = {self.player1: 3, self.player2: 3}
		self.score = {self.player1: 0, self.player2: 0}
		self.highscore = 0
		self.run = True
		self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
		pygame.mixer.music.load("Sounds/music.ogg")
		pygame.mixer.music.play(-1)
		self.load_highscore()

	def create_obstacles(self):
		obstacle_width = len(grid[0]) * 3
		gap = (self.screen_width + self.offset - (4 * obstacle_width))/5
		obstacles = []
		for i in range(4):
			offset_x = (i + 1) * gap + i * obstacle_width
			obstacle = Obstacle(offset_x, self.screen_height - 100)
			obstacles.append(obstacle)
		return obstacles

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
				alien = Alien(alien_type, x + self.offset/2, y)
				self.aliens_group.add(alien)

	def move_aliens(self):
		self.aliens_group.update(self.aliens_direction)
		for alien in self.aliens_group:
			if alien.rect.right >= self.screen_width + self.offset/2:
				self.aliens_direction = -1
				self.alien_move_down(2)
			elif alien.rect.left <= self.offset/2:
				self.aliens_direction = 1
				self.alien_move_down(2)

	def alien_move_down(self, distance):
		for alien in self.aliens_group:
			alien.rect.y += distance

	def alien_shoot_laser(self):
		if self.aliens_group:
			alien = random.choice(self.aliens_group.sprites())
			laser = Laser(alien.rect.center, -6, self.screen_height)
			self.alien_lasers_group.add(laser)

	def create_mystery_ship(self):
		self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

	def check_for_collisions(self):
		for ship in self.spaceships:
			for laser in ship.lasers_group:
				aliens_hit = pygame.sprite.spritecollide(laser, self.aliens_group, True)
				if aliens_hit:
					self.explosion_sound.play()
					for alien in aliens_hit:
						self.score[ship] += alien.type * 100
						self.check_for_highscore(ship)
						laser.kill()
				if pygame.sprite.spritecollide(laser, self.mystery_ship_group, True):
					self.score[ship] += 500
					self.explosion_sound.play()
					self.check_for_highscore(ship)
					laser.kill()
				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser, obstacle.blocks_group, True):
						laser.kill()

		for laser in self.alien_lasers_group:
			for ship in self.spaceships:
				if pygame.sprite.collide_rect(laser, ship):
					laser.kill()
					self.lives[ship] -= 1
					if self.lives[ship] == 0:
						self.spaceships.remove(ship)
			for obstacle in self.obstacles:
				if pygame.sprite.spritecollide(laser, obstacle.blocks_group, True):
					laser.kill()

		for alien in self.aliens_group:
			for obstacle in self.obstacles:
				pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)
				for ship in self.spaceships:
					if pygame.sprite.collide_rect(alien, ship):
						self.run = False

		if len(self.spaceships) == 0:
			self.run = False

	def check_for_highscore(self, ship):
		if self.score[ship] > self.highscore:
			self.highscore = self.score[ship]
			with open("highscore.txt", "w") as f:
				f.write(str(self.highscore))

	def load_highscore(self):
		try:
			with open("highscore.txt", "r") as f:
				self.highscore = int(f.read())
		except FileNotFoundError:
			self.highscore = 0

	def reset(self):
		self.__init__(self.screen_width, self.screen_height, self.offset)
