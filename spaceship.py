import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
	def __init__(self, screen_width, screen_height, offset,
	             left_key=pygame.K_LEFT, right_key=pygame.K_RIGHT, shoot_key=pygame.K_UP):
		super().__init__()
		self.offset = offset
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.image = pygame.image.load("Graphics/spaceship.png")
		self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
		self.speed = 6
		self.lasers_group = pygame.sprite.Group()
		self.laser_ready = True
		self.laser_time = 0
		self.laser_delay = 300
		self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")

		# Controles personalizables
		self.left_key = left_key
		self.right_key = right_key
		self.shoot_key = shoot_key

	def get_user_input(self):
		keys = pygame.key.get_pressed()

		if keys[self.right_key]:
			self.rect.x += self.speed

		if keys[self.left_key]:
			self.rect.x -= self.speed

		if keys[self.shoot_key] and self.laser_ready:
			self.laser_ready = False
			laser = Laser(self.rect.center, 5, self.screen_height)
			self.lasers_group.add(laser)
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	def update(self):
		self.get_user_input()
		self.constrain_movement()
		self.lasers_group.update()
		self.recharge_laser()

	def constrain_movement(self):
		if self.rect.right > self.screen_width:
			self.rect.right = self.screen_width
		if self.rect.left < self.offset:
			self.rect.left = self.offset

	def recharge_laser(self):
		if not self.laser_ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_delay:
				self.laser_ready = True

	def reset(self):
		self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
		self.lasers_group.empty()