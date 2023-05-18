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
