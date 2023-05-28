# __ProjetoTraineeIEEE__
 #### **Descrição**: Desenvolvimento de uma simulação simples de robôs sumôs, no qual serão ser possível serem treinados utilizando o método de neuroevolução, no qual baseia-se no treino de redes neurais utilizando algoritmos genéticos.

#### **Como funciona**: Os robôs são controlados por redes neurais treinadas utilizando o algoritmo de neuroevolução. Cada robô possui sensores que detectam a distância percorrida, a presença de linhas brancas no chão da arena e sua posição em relação ao centro da arena. Com base nessas informações, a rede neural do robô toma decisões sobre como se mover.

#### **Dependências**:O projeto utiliza a biblioteca Pygame para a renderização gráfica da simulação e a biblioteca Pymunk para a simulação física dos corpos dos robôs e da arena. Além disso, é necessário instalar a biblioteca NEAT (NeuroEvolution of Augmenting Topologies) para a implementação do algoritmo de neuroevolução.