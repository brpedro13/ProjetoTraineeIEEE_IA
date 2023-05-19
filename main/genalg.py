import random
import math
from robots import Robot
import pymunk 

height = 1800
width = 900



def create_population(space: 'pymunk.Space', circle_positions: tuple, population_size: int) -> list:
    population = []
    for _ in range(population_size):
        x_pos = circle_positions[0]
        y_pos = circle_positions[1]
        radius = 20
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        robot = Robot(1, x_pos, y_pos, radius, color)
        population.append(robot)
        robot.shape.sensor = True  # Definir a forma do robô como sensor (intangível)
        space.add(robot.body, robot.shape)
    return population

