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

    for i in range(0, 5000):
        fitness = [(function(value), index) for (index, value) in enumerate(population)]
        best_fitness_value = min(fitness)
        elites = get_elites(fitness, int(population_size * 7 / 100))

        write_statistics(best_fitness_value)

        if(best_fitness_value[0] < best_value_overall):
            best_value_overall = best_fitness_value[0]
            best_state_overall = population[best_fitness_value[1]][:]
        
        new_population = [population[entry[1]] for entry in elites]

        while(len(new_population) < population_size):
            
            first_parent_index, second_parent_index = tournament_selection(fitness, tournament_size, 2)

            first_parent = population[first_parent_index[1]]
            second_parent = population[second_parent_index[1]]
            child = first_parent

            if(random.random() < crossover_prob):
                child = get_crossover_state(first_parent, second_parent)

            if(random.random() < mutation_prob):
                child = get_random_mutation(child)

            new_population.extend(child)

    return(best_value_overall, best_state_overall)

def get_crossover_state(first_state, second_state):
    cutting_point = random.randint(1, len(first_state) - 1)

    child = first_state[0:cutting_point]
    child.extend(second_state[cutting_point:])

    return child

def get_random_mutation(individual):

    if(coloring_function(individual) - len(set(individual)) == 0):
        valid_colors = set(individual)
        deleted_color = random.sample(valid_colors, 1)[0]
        valid_colors.remove(deleted_color)
        for (color, index) in enumerate(individual):
            if color == deleted_color:
                if(len(valid_colors) > 1):
                    individual[index] = random.sample(valid_colors, 1)[0]
        return individual

    for vertex in range(0, len(individual)):
        if(has_bad_edge(vertex, individual)):
            adjacent_colors = get_adjacent_colors(vertex, individual)
            valid_colors = set(individual)
            valid_colors = [color for color in valid_colors if color not in adjacent_colors]
            if(len(valid_colors) > 1):
                new_color = random.sample(valid_colors, 1)
                individual[vertex] = new_color[0]

    return individual

def get_random_mutationv2(individual):
    for vertex in range(0, len(individual)):
        if(has_bad_edge(vertex, individual)):
            valid_colors = range(0, len(individual))
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
    
def tournament_selectionv2(fitness_values, tournamet_size, tournament_rounds):
    selected_parents = []

    for i in range(0, tournament_rounds):
        best_suitor = min(fitness_values)
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

def get_elites(fitness, size):
    sorted_list = sorted(fitness, key = lambda val: val[0])
    return sorted_list[0:size]

def get_adjacent_colors(vertex, individual):
    neighbours = graph.edges[vertex + 1]
    colors = []

    for neighbour in neighbours:
        colors.append(individual[neighbour - 1])

    return colors

def write_statistics(fitness_value):
    file_handler= open("./fpsol2.i.1.col_stats", "a")
    file_handler.write(str(fitness_value[0]) + "\n")
    file_handler.close()

def coloring_function(individual):
    bad_edges_counter = 0
    for vertex in range(0, len(individual)):
        if(vertex + 1 in graph.edges):
            neighbours = graph.edges[vertex + 1]
            for neighbour in neighbours:
                if(individual[vertex] == individual[neighbour - 1]):
                    bad_edges_counter = bad_edges_counter + 1

    return (bad_edges_counter / 2) + len(set(individual))

val, ceva = genetic_algorithm(coloring_function, graph.vertex_count, 50, 0.8, 0.5, 2)

print(coloring_function(ceva) - len(set(ceva)))
print(len(set(ceva)))
print(ceva)

# population = generate_initial_population(50, graph.vertex_count)
# print(coloring_function(population[0]))
# print(coloring_function(get_random_mutation(population[0])))