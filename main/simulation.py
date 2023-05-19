import pygame
import pymunk
import random
import math
from robot import Robot
from genalg import create_population

pygame.init()

# Configurações da janela
width = 1800
height = 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Robo Sumo')

# Configurações do espaço físico
space = pymunk.Space()

# Posição dos círculos
circle_positions = (width / 2, height / 2)

# Criar a arena
arena_radius = 200

# Criar o círculo central
center_radius = 180

# Criar o círculo externo (quando 50% do diametro do robô sai, o robô perde).
outer_radius = 225

# População 

population = create_population(space, circle_positions, 100)

# Timer
timer_duration = 10  # Duração do timer em segundos
start_time = pygame.time.get_ticks()  # Tempo inicial em milissegundos
reset_simulation = False

# Contador de simulações
simulation_counter = 0

# Fonte para exibir texto na tela
font = pygame.font.SysFont(None, 36)


# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    # Tratar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Atualizar posição dos robôs
    vartmp = clock.tick(60) / 1000.0
    for robo in population:
        robo.update_position(vartmp)
        robo.random_movement()

    # Verificar se os robôs estão dentro do círculo externo.   
    for robo in population:
        dx = robo.body.position.x - circle_positions[0]
        dy = robo.body.position.y - circle_positions[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
       
        # Se 50% do robô sair da arena:
        if distance + robo.radius > outer_radius:

            # Remover o robô da simulação
            space.remove(robo.body, robo.shape)
            population.remove(robo)

    # Atualizar a simulação física
    space.step(vartmp)

    # Verificar o tempo decorrido
    current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
    elapsed_time = (current_time - start_time) // 1000  # Tempo decorrido em segundos

    # Resetar a simulação após 10 segundos
    if elapsed_time >= timer_duration:
        # Resetar as variáveis
        start_time = current_time
        reset_simulation = True

    # Resetar a simulação
    if reset_simulation:
        # Incrementar o contador de simulações
        simulation_counter += 1

        # Reiniciar a população de robôs
        population = create_population(space, circle_positions, 100)

        # Resetar a variável de controle
        reset_simulation = False


    # Desenhar
    screen.fill((0, 0, 0))

    # Desenhar e definir o raio da arena
    color = (255, 255, 255)
    pygame.draw.circle(screen, color, circle_positions, int(arena_radius), 2)

    # Desenhar e definir o raio e círculo central 
    color = (255, 255, 255)
    pygame.draw.circle(screen, color, circle_positions, int(center_radius), 2)

    # Preencher a área entre a arena e o círculo central
    color = (255, 255, 255)
    pygame.draw.circle(screen, color, circle_positions, int(center_radius), 0)
    pygame.draw.circle(screen, (0, 0, 0), circle_positions, int(center_radius - 10), 0)
    pygame.draw.circle(screen, color, circle_positions, int(arena_radius), 0)
    pygame.draw.circle(screen, (0, 0, 0), circle_positions, int(arena_radius - 10), 0)

    # Desenhar o círculo externo
    color = (255, 0, 0)
    pygame.draw.circle(screen, color, circle_positions, int(outer_radius), 2)

    # Desenhar robôs
    for robo in population:
        pygame.draw.circle(screen, robo.color, (int(robo.body.position[0]), int(height - robo.body.position[1])), robo.radius)

    # Desenhar o timer
    timer_text = font.render("Timer: " + str(timer_duration - elapsed_time), True, (255, 255, 255))
    screen.blit(timer_text, (20, 20))

    # Desenhar o contador
    counter_text = font.render("Generation number: " + str(simulation_counter), True, (255, 255, 255))
    screen.blit(counter_text, (20, 60))

    # Atualizar tela
    pygame.display.flip()