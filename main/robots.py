import math
import pymunk
import random

# Dados da janela
WIDTH = 1800
HEIGHT = 900

# Dados da Arena
OUTER_RADIUS = 225
ARENA_RADIUS = 200 
CENTER_RADIUS = 180

# Dados dos robos
circle_positions = (WIDTH / 2, HEIGHT / 2)
SPEED = 200
colors = ('blue', 'green', 'pink', 'yellow', 'gray', 'purple', 'cyan', 'orange')

# Criar a classe robô 
class Robot:
    def __init__(self, mass: int, x: int, y: int, radius: int=25) -> None:
        """
        Classe para criar os robôs do jogo.

        Args:
            mass: A massa do robô.
            x: A posição x inicial do robô.
            y: A posição y inicial do robô.
            radius: O raio do robô. Padrão é 25.

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
        
        Functions:
            sensor_triggered (bool): Indica se o sensor de faixa branca foi acionado.
            is_slow (bool): Indica se o robô está se movendo em uma velocidade baixa.
        """
        # Dados do robo
        self.mass = mass
        self.body = pymunk.Body(mass=mass, moment=pymunk.moment_for_circle(mass, 0, radius))
        self.body.position = x, y
        self.speed = SPEED
        self.shape = pymunk.Circle(self.body, radius)
        self.elasticity = 0.8
        self.friction = 1
        self.radius = radius 
        self.color = random.choice(colors)
        self.alive = True 
        self.distance_traveled = 0
        self.last_position = (x, y)  
        self.sensor_triggered = False
        self.is_slow = False

    def set_speed(self, x_speed: int, y_speed: int) -> None:
        self.body.velocity = x_speed, y_speed
        """
        Define a velocidade do robô.

        x_speed: A velocidade em x do robô.
        y_speed: A velocidade em y do robô.
        """

    def move(self, angle: float, speed: int) -> None:
        """
        Move o robô em uma direção específica com uma determinada velocidade.

        angle: O ângulo de movimento em radianos.
        speed: A velocidade de movimento do robô.
        """
        x_speed = speed * math.cos(angle)
        y_speed = speed * math.sin(angle)
        self.set_speed(x_speed, y_speed)
        
    def update_position(self, vartmp: float) -> None:
        """
        Atualiza a posição do robô de acordo com a velocidade.

        vartmp: O tempo decorrido desde a última atualização.
        """
        # Atualziando posição
        self.body.position += self.body.velocity * vartmp
        self.distance_traveled += math.sqrt(self.body.velocity.x ** 2 + self.body.velocity.y ** 2)

        speed_threshold = 60  # Velocidade mínima considerada como baixa

        # Verificar se o robô está se movendo em uma velocidade baixa
        if abs(self.body.velocity.x) < speed_threshold and abs(self.body.velocity.y) < speed_threshold:
            self.is_slow = True
        else:
            self.is_slow = False        
        

    def whiteline_sensor(self) -> bool:
        """
        Verifica se o sensor de linha branca está acionado.

        return: True se o sensor estiver acionado, False caso contrário.
        """

        dx = self.body.position.x - circle_positions[0]
        dy = self.body.position.y - circle_positions[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Analise da posição do robô em relação à faixa branca
        if distance <= ARENA_RADIUS and distance >= CENTER_RADIUS:
            self.sensor_triggered = True
        else:
            self.sensor_triggered = False
        
        return self.sensor_triggered

    def update_distance_traveled(self) -> None:

        """
        Atualiza a distância total percorrida pelo robô.
        """

        current_position = self.body.position
        distance = math.sqrt((current_position.x - self.last_position[0]) ** 2 + (current_position.y - self.last_position[1]) ** 2)
        self.distance_traveled += distance
        self.last_position = (current_position.x, current_position.y)