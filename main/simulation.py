import pygame
import pymunk
import random
import math
from robots import Robot

pygame.init()

# Configurações da janela
width = 600
height = 600
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

# TODO não permitir que saia da arena
    
# Criação do Robo Azul e Vermelho

robo1 = Robot(mass=1, x=300, y=350, radius=25, color=(0, 0, 255))
robo1.set_speed(x_speed=0, y_speed=0)

robo2 = Robot(mass=1, x=300, y=250, radius=25, color=(255, 0, 0))

# Adicionar os corpos ao espaço físico
space.add(robo1.body, robo1.shape)
space.add(robo2.body, robo2.shape)

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
    robo1.update_position(vartmp)
    robo2.update_position(vartmp)

    # Movimento randômico do robô vermelho
    robo2.random_movement()

    # Verificar se os robôs estão dentro do círculo externo.

    for robo in [robo1, robo2]:
        dx = robo.body.position.x - circle_positions[0]
        dy = robo.body.position.y - circle_positions[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
       
        # Se 50% do robô sair da arena:
        if distance + 50 > outer_radius + robo.radius:

            # Definindo novas posições para os robôs
            new_pos_robo1 = (300, 350)
            new_pos_robo2 = (300, 250)

            # Resete a posição dos robôs
            robo1.body.position = new_pos_robo1
            robo2.body.position = new_pos_robo2

            # Resete a posição dos robôs
            robo1.body.position = new_pos_robo1
            robo2.body.position = new_pos_robo2

    ########## TODO Resetar momento e velocidade para a próxima ITERAÇÃO #########


    # Atualizar a simulação física
    space.step(vartmp)

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
    color = (0, 255, 0)
    pygame.draw.circle(screen, color, circle_positions, int(outer_radius), 2)

    # Desenhar robôs
    pygame.draw.circle(screen, robo1.color, (int(robo1.body.position[0]), int(height - robo1.body.position[1])), robo1.radius)
    pygame.draw.circle(screen, robo2.color, (int(robo2.body.position[0]), int(height - robo2.body.position[1])), robo2.radius)

    # Atualizar tela
    pygame.display.flip()