import matplotlib.pyplot as plt
import numpy as np

class Plot_Graphic:

    @staticmethod
    def plot_stats(self):
        """ Plota a média de fitness da população e do melhor indivíduo."""

        generation = range(len(self.most_fit_genomes))
        best_fitness = [c.fitness for c in self.most_fit_genomes]
        avg_fitness = np.array(self.get_fitness_mean())
        stdev_fitness = np.array(self.get_fitness_stdev())

        plt.plot(generation, avg_fitness, 'b-', label="Média")
        plt.plot(generation, best_fitness, 'r-', label="Melhor")
        plt.title("Média de fitness da população e fitness do melhor indivíduo")
        plt.xlabel("Gerações")
        plt.ylabel("Fitness")
        plt.grid()
        plt.yscale('log')
        plt.legend(loc="best")
        plt.show()

    @staticmethod
    def plot_species(self):
        """ Visualiza a especiação ao longo da evolução. """

        species_sizes = self.get_species_sizes()
        num_generations = len(species_sizes)
        curves = np.array(species_sizes).T

        fig, ax = plt.subplots()
        ax.stackplot(range(num_generations), *curves)

        plt.title("Especiação")
        plt.ylabel("Tamanho por espécie")
        plt.xlabel("Gerações")
        plt.show()