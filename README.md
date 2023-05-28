# __ProjetoTraineeIEEE__
 #### **Descrição**: Desenvolvimento de uma simulação simples de robôs sumôs, no qual serão ser possível serem treinados utilizando o método de neuroevolução, no qual baseia-se no treino de redes neurais utilizando algoritmos genéticos.

#### **Como funciona**:
Os robôs são controlados por redes neurais treinadas utilizando o algoritmo de neuroevolução. Cada robô possui sensores que detectam a distância percorrida, a presença de linhas brancas no chão da arena e sua posição em relação ao centro da arena. Com base nessas informações, a rede neural do robô toma decisões sobre como se mover.

#### **Dependências**:
>- **pygame**: Biblioteca para a criação de jogos em Python. Neste projeto, é utilizada para a renderização gráfica da simulação e para tratar eventos de entrada do usuário, como fechar a janela.

>- **pymunk**: Biblioteca de física em 2D para Python. É usada para simular a física dos corpos dos robôs e da arena, permitindo detecção de colisões e movimentação realista. 

>- **math**: Módulo matemático padrão do Python. É utilizado para realizar cálculos matemáticos, como geração de números aleatórios e cálculo de distâncias e ângulos.

>- **neat**: Biblioteca NEAT (NeuroEvolution of Augmenting Topologies) para a implementação do algoritmo de neuroevolução. Ela oferece as funcionalidades necessárias para criar e evoluir redes neurais através de reprodução genética e seleção natural.