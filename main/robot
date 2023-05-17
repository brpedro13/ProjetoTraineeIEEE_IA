import math
import pymunk
import random

# Criar a classe robô 

class Robot:
    """
    Classe para criar os robôs do jogo.

    Args:
        mass (int): A massa do robô.
        x (int): A posição x inicial do robô.
        y (int): A posição y inicial do robô.
        radius (float): O raio do robô. Padrão é 25.
        color (tuple): A cor do robô em RGB.

    Attributes:
        mass (int): A massa do robô.
        body (pymunk.Body): O corpo do robô no espaço físico.
        shape (pymunk.Circle): O formato do corpo do robô.
        elasticity (float): A elasticidade do robô.
        friction (float): O atrito do robô.
        radius (int): O raio do robô.
        color (tuple): A cor do robô em RGB.

    """

    def __init__(self, mass, x, y, radius=25, color=(255, 255, 255)):
        self.mass = mass
        self.body = pymunk.Body(mass=mass, moment=pymunk.moment_for_circle(mass, 0, radius))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.elasticity = 0.8
        self.friction = 1
        self.radius = radius 
        self.color = color
    
    def set_speed(self, x_speed, y_speed):
        self.body.velocity = x_speed, y_speed

        """
        Define a velocidade do robô.

        Args:
            x_speed (int): A velocidade em x do robô.
            y_speed (int): A velocidade em y do robô.

        """
        
    def update_position(self, vartmp):
        self.body.position += self.body.velocity * vartmp

        """
        Atualiza a posição do robô de acordo com a velocidade.

        Args:
            vartmp (float): O tempo decorrido desde a última atualização.

        """
    def random_movement(self):

        """
        Permite que o segundo robô se mova de forma randômica pela arena
        """

        # Definir a velocidade máxima que pode ser aplicada
        max_speed = 450

        # Definição de um intervalo randômico

        if random.randint(0,70) == 35:
            # Escolher uma rotação aleatória
            rand_rotation = random.uniform(0,2 * math.pi)
            # Aplicar a rotação no corpo do robô
            self.body.angle += rand_rotation

            # Calcular as coordenadas x e y da direção com base no ângulo escolhido
            direction_x = math.cos(self.body.angle)
            direction_y = math.sin(self.body.angle)

            # Escolher uma velocidade aleatória
            rand_speed = random.uniform(max_speed - ((1/4) * max_speed), max_speed)

            # Aplicar a velocidade na direção escolhida
            self.body.apply_force_at_local_point((direction_x  * rand_speed, direction_y  * rand_speed))

            # Status do Robô vermelho
            print(f"Status do Robô Vermelho:\nVelocidade = {rand_speed}\n")
