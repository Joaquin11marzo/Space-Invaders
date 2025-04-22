import pygame, sys, random
from game import Game
from game_two_players import GameTwoPlayers

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana de juego
ANCHO_VENTANA = 750
ALTO_VENTANA = 700
MARGEN = 50

# Colores utilizados
GRIS = (29, 29, 27)
AMARILLO = (243, 216, 63)
BLANCO = (255, 255, 255)
AMARILLO_OSCURO = (200, 180, 50)

# Fuentes utilizadas en el juego
fuente = pygame.font.Font("Font/monogram.ttf", 40)
fuente_titulo = pygame.font.Font("Font/monogram.ttf", 60)
fuente_boton = pygame.font.Font("Font/monogram.ttf", 30)
fuente_instrucciones = pygame.font.Font("Font/monogram.ttf", 20)

# Crear la ventana principal del juego
ventana = pygame.display.set_mode((ANCHO_VENTANA + MARGEN, ALTO_VENTANA + 2 * MARGEN))
pygame.display.set_caption("Python Space Invaders")

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Eventos personalizados para disparos y nave misteriosa
DISPARO_LASER = pygame.USEREVENT
NAVE_MISTERIOSA = pygame.USEREVENT + 1

# Generar fondo de estrellas animadas
estrellas = [[random.randint(0, ANCHO_VENTANA), random.randint(0, ALTO_VENTANA), random.randint(1, 3)] for _ in range(100)]

# Sonido de selección de opción en menú
sonido_seleccion = pygame.mixer.Sound("Sounds/laser.ogg")

# Función para dibujar botones en el menú
def dibujar_boton(texto, rect, posicion_mouse):
	color = AMARILLO_OSCURO if rect.collidepoint(posicion_mouse) else AMARILLO
	pygame.draw.rect(ventana, color, rect, border_radius=12)
	superficie_texto = fuente_boton.render(texto, True, GRIS)
	rect_texto = superficie_texto.get_rect(center=rect.center)
	ventana.blit(superficie_texto, rect_texto)

# Variables de estado del juego
menu_activo = True
juego = None
modo_seleccionado = 0

# Centro horizontal de la ventana
CENTRO_X = (ANCHO_VENTANA + MARGEN) // 2

# Definición de botones del menú
boton_1_jugador = pygame.Rect((CENTRO_X - 100, 300, 200, 60))
boton_2_jugadores = pygame.Rect((CENTRO_X - 100, 380, 200, 60))

# Bucle principal del juego
while True:
	posicion_mouse = pygame.mouse.get_pos()
	for evento in pygame.event.get():
		# Salir del juego
		if evento.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Interacción en el menú
		if menu_activo:
			if evento.type == pygame.MOUSEBUTTONDOWN:
				# Selección de modo 1 jugador
				if boton_1_jugador.collidepoint(posicion_mouse):
					sonido_seleccion.play()
					juego = Game(ANCHO_VENTANA, ALTO_VENTANA, MARGEN)
					modo_seleccionado = 1
					menu_activo = False
					pygame.time.set_timer(DISPARO_LASER, 300)
					pygame.time.set_timer(NAVE_MISTERIOSA, random.randint(4000, 8000))
				# Selección de modo multijugador
				elif boton_2_jugadores.collidepoint(posicion_mouse):
					sonido_seleccion.play()
					juego = GameTwoPlayers(ANCHO_VENTANA, ALTO_VENTANA, MARGEN)
					modo_seleccionado = 2
					menu_activo = False
					pygame.time.set_timer(DISPARO_LASER, 300)
					pygame.time.set_timer(NAVE_MISTERIOSA, random.randint(4000, 8000))
		else:
			# Disparo automático de aliens
			if evento.type == DISPARO_LASER and juego.run:
				juego.alien_shoot_laser()
			# Creación de nave misteriosa
			if evento.type == NAVE_MISTERIOSA and juego.run:
				juego.create_mystery_ship()
				pygame.time.set_timer(NAVE_MISTERIOSA, random.randint(4000, 8000))
			# Reiniciar juego
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_SPACE and not juego.run:
					juego.reset()

	# Dibujar fondo de estrellas
	ventana.fill(GRIS)
	for estrella in estrellas:
		pygame.draw.circle(ventana, BLANCO, (estrella[0], estrella[1]), estrella[2])
		estrella[1] += estrella[2]
		if estrella[1] > ALTO_VENTANA:
			estrella[0] = random.randint(0, ANCHO_VENTANA)
			estrella[1] = 0
			estrella[2] = random.randint(1, 3)

	# Pantalla del menú principal
	if menu_activo:
		superficie_titulo = fuente_titulo.render("SPACE INVADERS", True, AMARILLO)
		rect_titulo = superficie_titulo.get_rect(center=(CENTRO_X, 100))
		ventana.blit(superficie_titulo, rect_titulo)

		dibujar_boton("1 JUGADOR", boton_1_jugador, posicion_mouse)
		dibujar_boton("MULTIJUGADOR", boton_2_jugadores, posicion_mouse)

		# Instrucciones de control
		texto_controles = [
			"CONTROLES:",
			"Jugador 1: Izquierda/Derecha(flechas) para moverse, Arriba(flecha) para disparar",
			"Jugador 2: A/D para moverse, W para disparar"
		]
		y = 480
		for linea in texto_controles:
			superficie_texto = fuente_instrucciones.render(linea, True, AMARILLO)
			rect_texto = superficie_texto.get_rect(center=(CENTRO_X, y))
			ventana.blit(superficie_texto, rect_texto)
			y += 25

	# Pantalla de juego activa
	else:
		if juego.run:
			if modo_seleccionado == 1:
				juego.spaceship_group.update()
			elif modo_seleccionado == 2:
				juego.spaceships.update()
			juego.move_aliens()
			juego.alien_lasers_group.update()
			juego.mystery_ship_group.update()
			juego.check_for_collisions()

		# Bordes del área de juego
		pygame.draw.rect(ventana, AMARILLO, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
		pygame.draw.line(ventana, AMARILLO, (25, 730), (775, 730), 3)

		# Texto GAME OVER o nivel
		if not juego.run:
			superficie_game_over = fuente.render("GAME OVER", False, AMARILLO)
			ventana.blit(superficie_game_over, (570, 740))
		else:
			superficie_nivel = fuente.render("LEVEL 01", False, AMARILLO)
			ventana.blit(superficie_nivel, (570, 740))

		# Vidas y puntaje
		if modo_seleccionado == 1:
			x = 50
			for vida in range(juego.lives):
				ventana.blit(juego.spaceship_group.sprite.image, (x, 745))
				x += 50
			puntaje_formateado = str(juego.score).zfill(5)
			superficie_puntaje = fuente.render(puntaje_formateado, False, AMARILLO)
			ventana.blit(superficie_puntaje, (50, 40))
		else:
			x = 50
			for nave in juego.spaceships:
				for vida in range(juego.lives[nave]):
					ventana.blit(nave.image, (x, 745))
					x += 50
			s1 = list(juego.score.values())[0]
			s2 = list(juego.score.values())[1]
			puntaje_formateado = str(s1).zfill(5) + " | " + str(s2).zfill(5)
			superficie_puntaje = fuente.render(puntaje_formateado, False, AMARILLO)
			ventana.blit(superficie_puntaje, (50, 40))

		# Etiquetas UI
		ventana.blit(fuente.render("SCORE", False, AMARILLO), (50, 15))
		ventana.blit(fuente.render("HIGH-SCORE", False, AMARILLO), (550, 15))
		highscore_formateado = str(juego.highscore).zfill(5)
		superficie_highscore = fuente.render(highscore_formateado, False, AMARILLO)
		ventana.blit(superficie_highscore, (625, 40))

		# Dibujar entidades del juego
		if modo_seleccionado == 1:
			juego.spaceship_group.draw(ventana)
			juego.spaceship_group.sprite.lasers_group.draw(ventana)
		else:
			juego.spaceships.draw(ventana)
			for nave in juego.spaceships:
				nave.lasers_group.draw(ventana)

		for obstaculo in juego.obstacles:
			obstaculo.blocks_group.draw(ventana)
		juego.aliens_group.draw(ventana)
		juego.alien_lasers_group.draw(ventana)
		juego.mystery_ship_group.draw(ventana)

	# Actualizar pantalla
	pygame.display.update()
	reloj.tick(60)