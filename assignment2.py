from search import *
from random import randint
from assignment2aux import *

def read_tiles_from_file(filename):
    lines = [line.rstrip('\n') for line in open(filename, 'r').readlines()]
    character_to_tile = {' ': (), 'i': (0,), 'L': (0, 1), 'I': (0, 2), 'T': (0, 1, 2)}
    return tuple(tuple(character_to_tile[character] for character in line) for line in lines)

class KNetWalk(Problem):
    def __init__(self, tiles):
        if type(tiles) is str:
            self.tiles = read_tiles_from_file(tiles)
        else:
            self.tiles = tiles
        height = len(self.tiles)
        width = len(self.tiles[0])
        self.max_fitness = sum(sum(len(tile) for tile in row) for row in self.tiles)
        super().__init__(self.generate_random_state())

    def generate_random_state(self):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [randint(0, 3) for _ in range(height) for _ in range(width)]

    def actions(self, state):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [(i, j, k) for i in range(height) for j in range(width) for k in [0, 1, 2, 3] if state[i * width + j] != k]

    def result(self, state, action):
        pos = action[0] * len(self.tiles[0]) + action[1]
        return state[:pos] + [action[2]] + state[pos + 1:]

    def goal_test(self, state):
        return self.value(state) == self.max_fitness
    
    def value(self, state):
        # Task 1
        # Return an integer fitness value of a given state.
        # Replace the line below with your code.
        
        height = len(self.tiles)
        width = len(self.tiles[0])
        connections = 0

        for row in range(height):
            for col in range(width):
                tile = self.tiles[row][col]
                rotation = state[row * width + col]
                rotated = [(d + rotation) % 4 for d in tile]

                for direction in rotated:
                    if direction == 0:   nr, nc = row, col + 1
                    elif direction == 1: nr, nc = row - 1, col
                    elif direction == 2: nr, nc = row, col - 1
                    elif direction == 3: nr, nc = row + 1, col

                    if not (0 <= nr < height and 0 <= nc < width):
                        continue

                    neighbour_tile = self.tiles[nr][nc]
                    neighbour_rotation = state[nr * width + nc]
                    neighbour_rotated = [(d + neighbour_rotation) % 4 for d in neighbour_tile]

                    opposite = (direction + 2) % 4
                    if opposite in neighbour_rotated:
                        connections += 1

        return connections

        

# Task 2
# Configure an exponential schedule for simulated annealing.
sa_schedule = exp_schedule(k=20, lam=0.05, limit=1000)

# Task 3
# Configure parameters for the genetic algorithm.
pop_size = 100
num_gen = 1000
mutation_prob = 0.05

def local_beam_search(problem, population):
    # Task 4
    # Implement local beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the next population contains no fitter state.
    # Replace the line below with your code.
    beam_width = len(population)
    
    while True:
        children = []
        for state in population:
            for action in problem.actions(state):
                children.append(problem.result(state, action))
        
        for child in children:
            if problem.goal_test(child):
                return child
        
        next_population = sorted(children, key=problem.value, reverse=True)[:beam_width]
        
        if problem.value(next_population[0]) <= problem.value(population[0]):
            return max(population, key=problem.value)
        
        population = next_population

def stochastic_beam_search(problem, population, limit=1000):
    # Task 5
    # Implement stochastic beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the generation limit is reached.
    # Replace the line below with your code.
    import numpy as np
    beam_width = len(population)
    
    for _ in range(limit):
        children = []
        for state in population:
            for action in problem.actions(state):
                children.append(problem.result(state, action))
        
        for child in children:
            if problem.goal_test(child):
                return child
        
        fitnesses = [problem.value(child) for child in children]
        total = sum(fitnesses)
        probabilities = [f / total for f in fitnesses]
        
        indices = np.random.choice(len(children), beam_width, replace=False, p=probabilities)
        population = [children[i] for i in indices]
    
    return max(population, key=problem.value)

network = KNetWalk('assignment2config.txt')
goal_state = [3, 0, 2, 3, 0, 2, 3, 1, 0, 0, 1, 1]
print("max fitness:", network.max_fitness)
print("goal fitness:", network.value(goal_state))
if __name__ == '__main__':

    network = KNetWalk('assignment2config.txt')
    visualise(network.tiles, network.initial)

    # Task 1 test code
    
    run = 0
    method = 'hill climbing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = hill_climbing(network)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    

    # Task 2 test code

    run = 0
    method = 'simulated annealing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = simulated_annealing(network, schedule=sa_schedule)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)


    # Task 3 test code

    run = 0
    method = 'genetic algorithm'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = genetic_algorithm([network.generate_random_state() for _ in range(pop_size)], network.value, [0, 1, 2, 3], network.max_fitness, num_gen, mutation_prob)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)


    # Task 4 test code
    run = 0
    method = 'local beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = local_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)


    # Task 5 test code

    run = 0
    method = 'stochastic beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = stochastic_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
