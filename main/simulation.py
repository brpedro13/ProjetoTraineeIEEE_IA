import pygame
import pymunk
import math
import sys
from robots import Robot
import os
import neat
import random
import matplotlib.pyplot as plt
import numpy as np

pygame.init()

# Configurações da janela
WIDTH = 1800
HEIGHT = 900
geracao = -1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Robo Sumo')

# Configurações do espaço físico
space = pymunk.Space()

# Posição dos círculos
circle_positions = (WIDTH / 2, HEIGHT / 2)

# Criar a arena
ARENA_RADIUS = 200

# Criar o círculo central
CENTER_RADIUS = 180

# Criar o círculo externo (quando 50% do diametro do robô sai, o robô perde).
OUTER_RADIUS = 225

# Fonte para exibir texto na tela
font = pygame.font.SysFont(None, 30)

def plot_stats(stats):
    """ Plota a média de fitness da população e do melhor indivíduo."""

    generation = range(len(stats.most_fit_genomes))
    best_fitness = [c.fitness for c in stats.most_fit_genomes]
    avg_fitness = np.array(stats.get_fitness_mean())
    stdev_fitness = np.array(stats.get_fitness_stdev())

    plt.plot(generation, avg_fitness, 'b-', label="Média")
    plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="Melhor")

    plt.title("Média de fitness da população e fitness do melhor indivíduo")
    plt.xlabel("Gerações")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    plt.show()

def plot_species(stats):
    """ Visualiza a especiação ao longo da evolução. """

    species_sizes = stats.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    fig, ax = plt.subplots()
    ax.stackplot(range(num_generations), *curves)

    plt.title("Especiação")
    plt.ylabel("Tamanho por espécie")
    plt.xlabel("Gerações")
    plt.show()

    return fig


def draw_window(robos, circle_positions, ARENA_RADIUS, CENTER_RADIUS, OUTER_RADIUS, geracao):
    # Background
    screen.fill((0, 0, 0))

    # Desenhar e definir o raio da arena
    color = (255, 255, 255)
    pygame.draw.circle(screen, color, circle_positions, int(ARENA_RADIUS), 2)

    # Desenhar e definir o raio e círculo central 
    color = (255, 255, 255)
    pygame.draw.circle(screen, color, circle_positions, int(CENTER_RADIUS), 2)

    # Preencher a área entre a arena e o círculo central
    color = (255, 255, 255)
    pygame.draw.circle(screen, color, circle_positions, int(CENTER_RADIUS), 0)
    pygame.draw.circle(screen, (0, 0, 0), circle_positions, int(CENTER_RADIUS - 10), 0)
    pygame.draw.circle(screen, color, circle_positions, int(ARENA_RADIUS), 0)
    pygame.draw.circle(screen, (0, 0, 0), circle_positions, int(ARENA_RADIUS - 10), 0)

    # Desenhar o círculo externo
    color = (255, 0, 0)
    pygame.draw.circle(screen, color, circle_positions, int(OUTER_RADIUS), 2)

    # Desenhar robôs
    for robo in robos:
        pygame.draw.circle(screen, robo.color, (int(robo.body.position[0]), int(HEIGHT - robo.body.position[1])), robo.radius)

    # Exibir número da geração
    font_size = 40  
    font = pygame.font.SysFont(None, font_size)
    text = font.render(f'Geração: {geracao}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Atualizar tela
    pygame.display.flip()

def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_neat.txt")
    run(config_path)

def eval_genomes (genomes, config):

    """
    Função responsável por avaliar os genomas e executar a simulação.
    Recebe uma lista de genomas e uma configuração.
    """
    global geracao
    ge = [] # Criação do genoma
    nets = [] # Criação das redes neurais associadas ao genoma
    robos = [] # Criação do robô 
    geracao += 1 # Aumentar as gerações com o decorrer do código


    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        robos.append(Robot(1, circle_positions[0],circle_positions[1]))
        g.fitness = 0
        ge.append(g)
    # Loop principal
    run = True
    clock = pygame.time.Clock()
    while run and len(robos) > 0:
        # Tratar eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit('Simulation closed')
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    run = False
                if event.key == pygame.K_g:
                    plot_stats(stats)
                if event.key == pygame.K_h:
                    plot_species(stats)

        # Atualizar posição dos robôs
        vartmp = clock.tick(60) / 1000.0

        for i, robo in enumerate(robos):
            angle = random.uniform(0, 2*math.pi)  # Defina um ângulo aleatório
            speed = 200
            robo.move(angle, speed)
            ge[i].fitness += 5

            # Verificar se o robô está se movendo em uma velocidade baixa
            if robo.is_slow:
                ge[i].fitness -= 80  # Reduzir o fitness do genoma correspondente            

            # Enviar a posição atual para a rede neural e obter as saídas
            outputs = nets[i].activate((robo.body.position.x, robo.body.position.y, robo.whiteline_sensor()))

            # Obter a movimentação em x e y a partir das saídas da rede neural
            move_x = outputs[0]
            move_y = outputs[1]
            angle = outputs[2] * 2 * math.pi - math.pi

            # Atualizar a posição do robô com base na movimentação em x e y
            dx = robo.body.position.x - circle_positions[0]
            dy = robo.body.position.y - circle_positions[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Atualizar a posição do robô com base na movimentação em x e y
            new_x = robo.body.position.x + move_x
            new_y = robo.body.position.y + move_y

           # Verificar se a nova posição está dentro da arena e é diferente da posição anterior
            if distance + robo.radius < OUTER_RADIUS and (new_x, new_y) != robo.last_position:
                robo.body.position = new_x, new_y

                # Definir a velocidade com base na movimentação em x e y
                speed = math.sqrt(move_x ** 2 + move_y ** 2)
                angle = math.atan2(move_y, move_x)
                robo.set_speed(speed * math.cos(angle), speed * math.sin(angle))
                # Atualizar a última posição
                robo.last_position = (new_x, new_y)                

        for robo in robos:
            robo.update_distance_traveled()  # Atualiza a distância percorrida        
            robo.update_position(vartmp)

        # Verificar a distância percorrida pelos robôs e incrementar o fitness pelo indivíduo que andar mais
        for i, robo in enumerate(robos):
            distance_traveled = robo.distance_traveled
            ge[i].fitness += (distance_traveled)/100

        # Verificar se os robôs estão dentro do círculo externo.   
        for i,robo in enumerate(robos):
            dx = robo.body.position.x - circle_positions[0]
            dy = robo.body.position.y - circle_positions[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Se 50% do robô sair da arena:
            if distance + robo.radius > OUTER_RADIUS:
                # Remover o robô da simulação
                if robo.body in space.bodies:
                    space.remove(robo.body, robo.shape)
                # Diminuir fitness e eliminar os genes do indivíduo que sair
                ge[i].fitness -= 10
                robos.pop(i)
                nets.pop(i)
                ge.pop(i)
                # Definir o robô como morto
                robo.alive = False

        # Aumentar fitness para todos os robôs vivos    
        if robo.alive == True:
            g.fitness += 4

        # Verificar o acionamento do sensor de linha branca e da distancia andada
        for i, robo in enumerate(robos):
            sensor_triggered = robo.whiteline_sensor()
            if sensor_triggered:
                ge[i].fitness -= 10 # Diminuir a fitness individual quando o sensor é acionado

        # Atualizar a simulação física
        space.step(vartmp)

        # Desenhar a janela
        draw_window(robos, circle_positions, ARENA_RADIUS, CENTER_RADIUS, OUTER_RADIUS, geracao)

# Roda o algoritmo de Neuroevolução, que faz com que o robô aprenda a se mover pela arena seguindo as especificações
def run(config_file):
    """
    Função responsável por rodar o algoritmo de Neuroevolução.
    Recebe o caminho do arquivo de configuração como parâmetro.
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Criação da população
    population = neat.Population(config)

    # Printa um relatório no terminal que demonstra o progresso da evolução
    population.add_reporter(neat.StdOutReporter(True))
    global stats
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Roda a simulação até 50 gerações
    winner = population.run(eval_genomes, 50)

    # Printa o resultado final
    print('Melhor genoma:\n{!s}'.format(winner))
    
# Determina o caminho do arquivo, está presente para o código rodar independente do diretório ativo.    
if __name__ == '__main__':
    main()