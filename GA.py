import reader
from threading import Thread
import math
import time
import random
import numpy as np
import sys

global graph
graph = reader.read_instance('./data/fpsol2.i.1.col')

def genetic_algorithm(function, improvement_method, low, high, dimensions, population_size, crossover_prob, tournament_size):
    reset_count = 1
    mutation_prob = 0.1
    best_state_overall = None
    best_value_overall = sys.maxsize
    population = generate_initial_population(population_size, dimensions)

    for i in range(0, 100):
        initial_timer = time.perf_counter()
        fitness = [(function(scale(value, bites_number, low, high)), index) for (index, value) in enumerate(population)]
        best_fitness_value = min(fitness)

        if(best_fitness_value[0] < best_value_overall):
            best_value_overall = best_fitness_value[0]
            best_state_overall = population[best_fitness_value[1]][:]

        new_population = [population[entry[1]] for entry in elites]

        while(len(new_population) < population_size):

            first_parent_index, second_parent_index = tournament_selection(fitness, tournament_size, 2)

            first_parent = population[first_parent_index[1]]
            second_parent = population[second_parent_index[1]]

            if(random.random() < crossover_prob):
                first_parent, second_parent = get_crossover_state(first_parent, second_parent)

            if(random.random() < mutation_prob):
                first_parent = random_mutation(first_parent)
                second_parent = random_mutation(second_parent)

            new_population.append(first_parent)
            new_population.append(second_parent)

    return(best_value_overall, best_state_overall)

def get_crossover_children(first_parent, second_parent):
    cutting_point = random.randint(0, bites_number - 2)
    common_gene = first_parent ^ second_parent
    bit_mask = (1 << bites_number - cutting_point - 1) - 1
    common_gene = common_gene & bit_mask
    return(first_parent ^ common_gene, second_parent ^ common_gene)

def get_crossover_state(first_state, second_state):
    new_first_state = [0] * len(first_state)
    new_second_state = [0] * len(second_state)
    for i in range(0, len(first_state)):
        new_first_state[i], new_second_state[i] = get_crossover_children(first_state[i], second_state[i])

    return (new_first_state, new_second_state)

def random_mutation(individual):
    for index in range(0,len(individual)):
        mutation_index = random.randint(0, bites_number -  1)
        individual[index] = individual[index] ^ (1 << mutation_index)

    return individual

def generate_initial_population(population_size, colors):
    population = []
    for individual in range(0,population_size):
        population.append([random.randint(0, colors - 1) for color in range(0, colors)])

    return population

def tournament_selection(fitness_values, tournamet_size, tournament_rounds):
    selected_parents = []

    for i in range(0, tournament_rounds):
        suitors = random.sample(fitness_values, tournamet_size)
        best_suitor = min(suitors)
        selected_parents.append(best_suitor)

def coloring_function(individual):
    visited = [0] * len(individual)
    bad_edges_counter = 0
    for vertice in range(0, len(individual)):
        if(vertice + 1 in graph.edges):
            neighbours = graph.edges[vertice + 1]
            for neighbour in neighbours:
                if(individual[vertice] == individual[neighbour - 1] and visited[vertice] == 0 and visited[neighbour - 1] == 0):
                    bad_edges_counter = bad_edges_counter + 1
                    visited[vertice] = 1
                    visited[neighbour - 1] = 1

    return bad_edges_counter

population = generate_initial_population(50, graph.vertex_count)
print(coloring_function(population[0]))