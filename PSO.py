from threading import Thread
import math
import random
import time
import numpy as np
import sys
import reader

global graph
graph = reader.read_instance('./data/myciel5.col')

iterations = 1000
particles = 100

def swarm_optimization(function, dimensions, alfa, cognition, social, low, high):
    positions = generate_random_position(particles,dimensions, low, high)
    velocitys = generate_random_velocity(particles,dimensions, low, high)
    best_local_positions = [position[:] for position in positions]
    best_team_position = positions[np.argmin([function(position) for position in positions])][:]

    for i in range(0,iterations):
        for particle in range(0,particles):
            for dimension in range(0, dimensions):
                velocitys[particle][dimension] = alfa * velocitys[particle][dimension] + random.random() * cognition * (best_local_positions[particle][dimension] - positions[particle][dimension]) + random.random() * social * (best_team_position[dimension] - positions[particle][dimension])
            positions[particle] = np.add(positions[particle], velocitys[particle])
            if(function(positions[particle]) < function(best_local_positions[particle]) and has_bad_edge(positions[particle]) == False):
                best_local_positions[particle] = positions[particle][:]
                if(function(best_local_positions[particle]) < function(best_team_position)):
                    best_team_position = best_local_positions[particle][:]

        if(alfa > 0.01):
            alfa = alfa - 0.0001

    print(function.__name__, function(best_team_position), function(best_team_position) - len(set(translate_to_colors(best_team_position))), translate_to_colors(best_team_position))

def generate_random_position(population_size, dimensions, low, high):
    population = []
    for individual in range(0, population_size):
        population.append([random.uniform(low, high) for dimension in range(0, dimensions)])

    return population

def generate_random_velocity(population_size, dimensions, low, high):
    population = []
    for individual in range(0, population_size):
        population.append([random.uniform(-abs(high-low), abs(high-low)) for dimension in range(0, dimensions)])

    return population


def translate_to_colors(individual, newMin = 0, newMax = graph.vertex_count - 1):
    result = [0] * len(individual)

    min_val = min(individual)
    max_val = max(individual)

    for (index,value) in enumerate(individual):
        result[index] = (newMax - newMin) * (value - min_val) / (max_val - min_val) + newMin
        result[index] = round(result[index])

    return result

def coloring_function(individual_continous):
    individual = translate_to_colors(individual_continous)
    bad_edges_counter = 0
    for vertex in range(0, len(individual)):
        if(vertex + 1 in graph.edges):
            neighbours = graph.edges[vertex + 1]
            for neighbour in neighbours:
                if(individual[vertex] == individual[neighbour - 1]):
                    bad_edges_counter = bad_edges_counter + 1

    return (bad_edges_counter / 2) + len(set(individual))


def has_bad_edge(individual_continous):
    individual = translate_to_colors(individual_continous)
    for vertex in range(0, len(individual)):
        if(vertex + 1 in graph.edges):
            neighbours = graph.edges[vertex + 1]
            for neighbour in neighbours:
                if(individual[vertex] == individual[neighbour - 1]):
                    return True

    return False

def write_statistics(function, fitness_value):
    file_handler= open("./time_stats_2_six", "a")
    file_handler.write(function.__name__ + " " + str(fitness_value) + "\n")
    file_handler.close()

swarm_optimization(coloring_function, graph.vertex_count, 0.5, 2, 2, 0, graph.vertex_count - 1)