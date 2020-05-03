import reader
from threading import Thread
import math
import time
import random
import numpy as np
import sys

global graph
graph = reader.read_instance('./data/fpsol2.i.1.col')

def genetic_algorithm(function, colors, population_size, mutation_prob, crossover_prob, tournament_size):
    best_state_overall = None
    best_value_overall = sys.maxsize
    population = generate_initial_population(population_size, colors)

    for i in range(0, 2000):
        fitness = [(function(value), index) for (index, value) in enumerate(population)]
        best_fitness_value = min(fitness)

        if(best_fitness_value[0] < best_value_overall):
            best_value_overall = best_fitness_value[0]
            best_state_overall = population[best_fitness_value[1]][:]
        
        if(best_fitness_value[0] == 0):
            return(best_value_overall, best_state_overall)

        new_population = []

        while(len(new_population) < population_size):

            first_parent_index, second_parent_index = tournament_selection(fitness, tournament_size, 2)

            first_parent = population[first_parent_index[1]]
            second_parent = population[second_parent_index[1]]

            if(random.random() < crossover_prob):
                first_parent, second_parent = get_crossover_state(first_parent, second_parent)

            if(random.random() < mutation_prob):
                first_parent = get_random_mutation(first_parent)
                second_parent = get_random_mutation(second_parent)
                
            new_population.extend(first_parent)
            new_population.extend(second_parent)

    return(best_value_overall, best_state_overall)

def get_crossover_state(first_state, second_state):
    cutting_point = random.randint(1, len(first_state) - 1)

    first_child = first_state[0:cutting_point]
    first_child.extend(second_state[cutting_point:])
    second_child = second_state[0:cutting_point]
    second_child.extend(first_state[cutting_point:])

    return (first_child , second_child)

def get_random_mutation(individual):
    for vertex in range(0, len(individual)):
        if(has_bad_edge(vertex, individual)):
            adjacent_colors = get_adjacent_colors(vertex, individual)
            valid_colors = range(0, len(individual))
            valid_colors = [color for color in valid_colors if color not in adjacent_colors]
            new_color = random.sample(valid_colors, 1)
            individual[vertex] = new_color[0]

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
    
    return selected_parents

def has_bad_edge(vertex, individual):
    if(vertex + 1 not in graph.edges):
        return False

    neighbours = graph.edges[vertex + 1]
    for neighbour in neighbours:
        if(individual[vertex] == individual[neighbour - 1]):
            return True

    return False

def get_adjacent_colors(vertex, individual):
    neighbours = graph.edges[vertex + 1]
    colors = []

    for neighbour in neighbours:
        colors.append(individual[neighbour - 1])

    return colors

def coloring_function(individual):
    visited = [0] * len(individual)
    bad_edges_counter = 0
    for vertex in range(0, len(individual)):
        if(vertex + 1 in graph.edges):
            neighbours = graph.edges[vertex + 1]
            for neighbour in neighbours:
                if(individual[vertex] == individual[neighbour - 1] and visited[vertex] == 0 and visited[neighbour - 1] == 0):
                    bad_edges_counter = bad_edges_counter + 1
                    visited[vertex] = 1
                    visited[neighbour - 1] = 1

    return bad_edges_counter

value, colors = genetic_algorithm(coloring_function, graph.vertex_count, 50, 0.1, 0.6, 6)

ceva = set(colors)
print(len(ceva))