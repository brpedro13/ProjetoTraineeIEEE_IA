import pygame
import pymunk
import math
import sys
import os
import neat
import random
from robots import Robot
from p_graph import Plot_Graphic

# Iniciando o pygame
pygame.init()

# Configurações da janela
WIDTH = 1800                                        # Comprimento da janela
HEIGHT = 900                                        # Largura da janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Criação do display no pygame
pygame.display.set_caption('Robo Sumo')             # Título da aba
geracao = -1                                        # Indicador de geração
clock = pygame.time.Clock()                         # Tempo do pygame

# Configurações da arena
ARENA_RADIUS = 200      # Raio da arena
CENTER_RADIUS = 180     # Raio interno da linha branca
OUTER_RADIUS = 225      # Raio externo da linha branca

# Configurações do espaço físico
space = pymunk.Space()

# Posição inicial dos robos
circle_positions = (WIDTH / 2, HEIGHT / 2)

# Fonte para exibir texto na tela
fontsize = 40
font = pygame.font.SysFont(None, fontsize)


def main():
    # Buscando o arquivo de configuração da simulação
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_neat.txt")
    
    # Executando a simulação
    run(config_path)


def draw_window(robos: list[Robot],
                circle_positions: tuple[int],
                ARENA_RADIUS: int,
                CENTER_RADIUS: int,
                OUTER_RADIUS: int,
                geracao: int
                ) -> None:
    """
    Constrói a interface gráfica via Pygame.

    robos: lista com os Robot objects da atual simulação
    circle_postions: tupla com a posição inicial dos robots
    ARENA_RADIUS: raio da arena
    CENTER_RADIUS: raio interno da linha branca
    OUTER_RADIUS: raio externo da linha branca
    """
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
    text = font.render(f'Geração: {geracao}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Exibir número de robos vivos
    text = font.render(f'Nº de indivíduos vivos: {len(robos)}', True, (255, 255, 255))
    screen.blit(text, (10, fontsize))

    # Exibir tempo da simulação
    time = pygame.time.get_ticks() - last_gen_time
    tempo = f'Tempo: {int(time/1000)}'
    text = font.render(tempo, True, (255, 255, 255))
    screen.blit(text, (WIDTH - len(tempo)*16, 10))

    # Exibir legenda de comandos
    text = font.render('[F] - Forçar próxima geração', True, (255, 255, 255))
    screen.blit(text, (WIDTH - 640, HEIGHT - fontsize*3))
    text = font.render('[G] - Plotar gráfico Fitness x Geração', True, (255, 255, 255))
    screen.blit(text, (WIDTH - 640, HEIGHT - fontsize*2))
    text = font.render('[H] - Plotar gráfico Espécies x Nº de indivíduos', True, (255, 255, 255))
    screen.blit(text, (WIDTH - 640, HEIGHT - fontsize))

    # Atualizar tela
    pygame.display.flip()


def eval_genomes(genomes: list[neat.DefaultGenome], config: str):
    """
    Função responsável por avaliar os genomas e executar a simulação.

    genomes: lista de genomas
    config: string com endereço do arquivo de configuração da simulação
    """
    ge = []         # Criação da lista de genomas
    robos = []      # Criação da lsita de robos
    nets = []       # Criação das redes neurais associadas ao genoma
    global geracao  # Exportando varíavel geracao 
    geracao += 1    # Aumentar as gerações com o decorrer do código

    # Preenchendo as listas de genomas (ge), robos (robos) e redes neurais (nets) 
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        robos.append(Robot(1, circle_positions[0],circle_positions[1]))
        g.fitness = 0
        ge.append(g)
    
    # Tempo da última geração
    global last_gen_time
    if geracao == 0:
        last_gen_time = 0
    else:
        last_gen_time = pygame.time.get_ticks()

    run = True  # Estado do loop

    # Loop principal // Até todos os robos morrerem
    while run and len(robos) > 0:

        # Interações da simulação
        for event in pygame.event.get():

            # Botão "X" na aba da simulação
            if event.type == pygame.QUIT:
                sys.exit('\033[1;31mSimulation closed\033[m\n')  # Parando a simulação
            
            # Verificando comandos do teclado
            if event.type == pygame.KEYDOWN:

                # Ao pressionar "f" a simulação é forçada a passar de geração
                if event.key == pygame.K_f:
                    run = False

                # Ao pressionar "g" é plotado um gráfico Fitness x Geração
                if event.key == pygame.K_g:
                    Plot_Graphic.plot_stats(stats)
                
                # Ao pressionar "h" é plotado um gráfico Espécies x nº de indivídos
                if event.key == pygame.K_h:
                    Plot_Graphic.plot_species(stats)

        # Atualizar posição dos robôs
        vartmp = clock.tick(60) / 1000.0

        # Iterando entre cada robo
        for i, robo in enumerate(robos):

            angle = random.uniform(0, 2*math.pi)  # Defina um ângulo aleatório
            robo.move(angle, robo.speed)          # Robo anda em direção esse ângulo
            ge[i].fitness += 5                    # Incentivando robo a não ficar parado

            # Verificar se o robô está se movendo em uma velocidade baixa
            if robo.is_slow:
                ge[i].fitness -= 80  # Reduzir o fitness do genoma correspondente            

            # Enviar a posição atual para a rede neural e obter as saídas
            outputs = nets[i].activate((robo.body.position.x,
                                        robo.body.position.y,
                                        robo.whiteline_sensor()
                                        ))

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

        # Atualizando dados dos robos   
        for robo in robos:
            robo.update_distance_traveled()       
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

            # Se 50% do robô sair da arena
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
        draw_window(robos,
                    circle_positions,
                    ARENA_RADIUS,
                    CENTER_RADIUS,
                    OUTER_RADIUS,
                    geracao
                    )

def run(config_file: str) -> None:
    """
    Função responsável por rodar o algoritmo de Neuroevolução
    
    config_file: string com o endereço do arquivo de configuração da simulação
    """
    # Configuração do neat
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_file
                                )

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
    
   
if __name__ == '__main__':
    main()