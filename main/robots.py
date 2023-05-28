import math
import pymunk

WIDTH = 1800
HEIGHT = 900
circle_positions = (WIDTH / 2, HEIGHT / 2)
outer_radius = 225 # Raio do circulo externo
arena_radius = 200 # Raio da arena
center_radius = 180 # Raio do círculo central


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
        alive (bool): Indica se o robô está vivo ou não.
        distance_traveled (float): A distância total percorrida pelo robô.
        last_position (tuple): As coordenadas da última posição do robô.
        sensor_triggered (bool): Indica se o sensor de faixa branca foi acionado.
        is_slow (bool): Indica se o robô está se movendo em uma velocidade baixa.

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
        self.alive = True 
        self.distance_traveled = 0
        self.last_position = (x, y)  
        self.sensor_triggered = False
        self.is_slow = False  

    def set_speed(self, x_speed, y_speed):
        self.body.velocity = x_speed, y_speed

        """
        Define a velocidade do robô.

        Args:
            x_speed (int): A velocidade em x do robô.
            y_speed (int): A velocidade em y do robô.
        """

    def move(self, angle, speed):
        """
        Move o robô em uma direção específica com uma determinada velocidade.

        Args:
            angle (float): O ângulo de movimento em radianos.
            speed (float): A velocidade de movimento do robô.
        """
        x_speed = speed * math.cos(angle)
        y_speed = speed * math.sin(angle)
        self.set_speed(x_speed, y_speed)
        
    def update_position(self, vartmp):
        self.body.position += self.body.velocity * vartmp
        self.distance_traveled += math.sqrt(self.body.velocity.x ** 2 + self.body.velocity.y ** 2)

        speed_threshold = 50  # Velocidade mínima considerada como baixa

        # Verificar se o robô está se movendo em uma velocidade baixa
        if abs(self.body.velocity.x) < speed_threshold and abs(self.body.velocity.y) < speed_threshold:
            self.is_slow = True
        else:
            self.is_slow = False        

        """
        Atualiza a posição do robô de acordo com a velocidade.

        Args:
            vartmp (float): O tempo decorrido desde a última atualização.

        """

    def whiteline_sensor(self):

        """
        Verifica se o sensor de linha branca está acionado.

        Returns:
            bool: True se o sensor estiver acionado, False caso contrário.
        """

        dx = self.body.position.x - circle_positions[0]
        dy = self.body.position.y - circle_positions[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Analise da posição do robô em relação à faixa branca
        if distance <= arena_radius and distance >= center_radius:
            self.sensor_triggered = True
        else:
            self.sensor_triggered = False
        
        return self.sensor_triggered

    def update_distance_traveled(self):

        """
        Atualiza a distância total percorrida pelo robô.
        """

        current_position = self.body.position
        distance = math.sqrt((current_position.x - self.last_position[0]) ** 2 + (current_position.y - self.last_position[1]) ** 2)
        self.distance_traveled += distance
        self.last_position = (current_position.x, current_position.y)