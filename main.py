import pygame, sys, random
from game import Game
from game_two_players import GameTwoPlayers
from ranking import guardar_ranking, obtener_top_3

pygame.init()

ANCHO_VENTANA = 750
ALTO_VENTANA = 700
MARGEN = 50
GRIS = (29, 29, 27)
AMARILLO = (243, 216, 63)
BLANCO = (255, 255, 255)
AMARILLO_OSCURO = (200, 180, 50)

fuente = pygame.font.Font("Font/monogram.ttf", 40)
fuente_titulo = pygame.font.Font("Font/monogram.ttf", 60)
fuente_boton = pygame.font.Font("Font/monogram.ttf", 30)
fuente_instrucciones = pygame.font.Font("Font/monogram.ttf", 20)
fuente_ranking = pygame.font.Font("Font/monogram.ttf", 20)
fuente_input = pygame.font.Font("Font/monogram.ttf", 25)

ventana = pygame.display.set_mode((ANCHO_VENTANA + MARGEN, ALTO_VENTANA + 2 * MARGEN))
pygame.display.set_caption("Python Space Invaders")

reloj = pygame.time.Clock()

DISPARO_LASER = pygame.USEREVENT
NAVE_MISTERIOSA = pygame.USEREVENT + 1

estrellas = [[random.randint(0, ANCHO_VENTANA), random.randint(0, ALTO_VENTANA), random.randint(1, 3)] for _ in range(100)]
sonido_seleccion = pygame.mixer.Sound("Sounds/laser.ogg")
CENTRO_X = (ANCHO_VENTANA + MARGEN) // 2

# Estados
menu_activo = True
juego = None
modo_seleccionado = 0
esperando_nombre = False
nombre_jugador = ""
texto_activo = 0

boton_1_jugador = pygame.Rect((CENTRO_X - 100, 300, 200, 60))
boton_2_jugadores = pygame.Rect((CENTRO_X - 100, 380, 200, 60))
boton_empezar = pygame.Rect((CENTRO_X - 80, 480, 160, 50))

input_rect1 = pygame.Rect(CENTRO_X - 100, 360, 200, 40)
color_input = pygame.Color("white")

def dibujar_boton(texto, rect, posicion_mouse):
    color = AMARILLO_OSCURO if rect.collidepoint(posicion_mouse) else AMARILLO
    pygame.draw.rect(ventana, color, rect, border_radius=12)
    superficie_texto = fuente_boton.render(texto, True, GRIS)
    rect_texto = superficie_texto.get_rect(center=rect.center)
    ventana.blit(superficie_texto, rect_texto)

def dibujar_ranking():
    top = obtener_top_3()
    y1 = 100
    ventana.blit(fuente_boton.render("TOP 3 JUGADORES", True, BLANCO), (CENTRO_X - 120, y1))
    for i, entrada in enumerate(top):
        texto = f"{i+1}. {entrada['nombre']} - {entrada['puntaje']}"
        ventana.blit(fuente_ranking.render(texto, True, BLANCO), (CENTRO_X - 120, y1 + 30 + i * 20))

while True:
    posicion_mouse = pygame.mouse.get_pos()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_activo and not esperando_nombre:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_1_jugador.collidepoint(posicion_mouse):
                    sonido_seleccion.play()
                    esperando_nombre = True
                    modo_seleccionado = 1
                    nombre_jugador = ""
                elif boton_2_jugadores.collidepoint(posicion_mouse):
                    sonido_seleccion.play()
                    juego = GameTwoPlayers(ANCHO_VENTANA, ALTO_VENTANA, MARGEN)
                    juego.nombre_jugador = "Jugador1"
                    juego.nombre_jugador2 = "Jugador2"
                    modo_seleccionado = 2
                    menu_activo = False
                    esperando_nombre = False
                    pygame.time.set_timer(DISPARO_LASER, 300)
                    pygame.time.set_timer(NAVE_MISTERIOSA, random.randint(4000, 8000))

        elif esperando_nombre:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre_jugador.strip():
                    juego = Game(ANCHO_VENTANA, ALTO_VENTANA, MARGEN)
                    juego.nombre_jugador = nombre_jugador.strip()
                    modo_seleccionado = 1
                    menu_activo = False
                    esperando_nombre = False
                    pygame.time.set_timer(DISPARO_LASER, 300)
                    pygame.time.set_timer(NAVE_MISTERIOSA, random.randint(4000, 8000))
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                else:
                    char = evento.unicode
                    if len(nombre_jugador) < 12:
                        nombre_jugador += char

        elif not menu_activo:
            if evento.type == DISPARO_LASER and juego.run:
                juego.alien_shoot_laser()
            if evento.type == NAVE_MISTERIOSA and juego.run:
                juego.create_mystery_ship()
                pygame.time.set_timer(NAVE_MISTERIOSA, random.randint(4000, 8000))
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not juego.run:
                    if modo_seleccionado == 1:
                        guardar_ranking(juego.nombre_jugador, juego.score)
                    else:
                        s1 = list(juego.score.values())[0]
                        s2 = list(juego.score.values())[1]
                        guardar_ranking("Jugador1", s1)
                        guardar_ranking("Jugador2", s2)
                    juego.reset()

    # Fondo
    ventana.fill(GRIS)
    for estrella in estrellas:
        pygame.draw.circle(ventana, BLANCO, (estrella[0], estrella[1]), estrella[2])
        estrella[1] += estrella[2]
        if estrella[1] > ALTO_VENTANA:
            estrella[0] = random.randint(0, ANCHO_VENTANA)
            estrella[1] = 0
            estrella[2] = random.randint(1, 3)

    if menu_activo:
        superficie_titulo = fuente_titulo.render("SPACE INVADERS", True, AMARILLO)
        rect_titulo = superficie_titulo.get_rect(center=(CENTRO_X, 40))
        ventana.blit(superficie_titulo, rect_titulo)

        if esperando_nombre:
            texto1 = fuente_input.render("Nombre Jugador:", True, BLANCO)
            ventana.blit(texto1, (CENTRO_X - 100, 330))
            pygame.draw.rect(ventana, color_input, input_rect1, 2)
            txt_surface = fuente_input.render(nombre_jugador, True, BLANCO)
            ventana.blit(txt_surface, (input_rect1.x + 5, input_rect1.y + 5))
            dibujar_boton("EMPEZAR (ENTER)", boton_empezar, posicion_mouse)
        else:
            dibujar_boton("1 JUGADOR", boton_1_jugador, posicion_mouse)
            dibujar_boton("MULTIJUGADOR", boton_2_jugadores, posicion_mouse)
            dibujar_ranking()

            texto_controles = [
                "CONTROLES:",
                "Jugador 1: Izq/Der(flechas), Arriba(flecha) para disparar",
                "Jugador 2: A/D para moverse, W para disparar"
            ]
            y = 560
            for linea in texto_controles:
                superficie_texto = fuente_instrucciones.render(linea, True, AMARILLO)
                rect_texto = superficie_texto.get_rect(center=(CENTRO_X, y))
                ventana.blit(superficie_texto, rect_texto)
                y += 25

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

        pygame.draw.rect(ventana, AMARILLO, (10, 10, 780, 780), 2)
        pygame.draw.line(ventana, AMARILLO, (25, 730), (775, 730), 3)

        if not juego.run:
            ventana.blit(fuente.render("GAME OVER", False, AMARILLO), (570, 740))
        else:
            ventana.blit(fuente.render("LEVEL 01", False, AMARILLO), (570, 740))

        if modo_seleccionado == 1:
            x = 50
            for vida in range(juego.lives):
                ventana.blit(juego.spaceship_group.sprite.image, (x, 745))
                x += 50
            ventana.blit(fuente.render(str(juego.score).zfill(5), False, AMARILLO), (50, 40))
        else:
            x1 = 50
            ventana.blit(fuente_instrucciones.render("P1", True, AMARILLO), (x1, 730))
            for vida in range(juego.lives[juego.player1]):
                ventana.blit(juego.player1.image, (x1, 745))
                x1 += 40

            x2 = 400
            ventana.blit(fuente_instrucciones.render("P2", True, AMARILLO), (x2, 730))
            for vida in range(juego.lives[juego.player2]):
                ventana.blit(juego.player2.image, (x2, 745))
                x2 += 40

            s1 = list(juego.score.values())[0]
            s2 = list(juego.score.values())[1]
            ventana.blit(fuente.render(f"{str(s1).zfill(5)} | {str(s2).zfill(5)}", False, AMARILLO), (50, 40))

        ventana.blit(fuente.render("SCORE", False, AMARILLO), (50, 15))
        ventana.blit(fuente.render("HIGH-SCORE", False, AMARILLO), (550, 15))
        ventana.blit(fuente.render(str(juego.highscore).zfill(5), False, AMARILLO), (625, 40))

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

    pygame.display.update()
    reloj.tick(60)
