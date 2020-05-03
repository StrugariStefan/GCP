from reader import read_instance, Graph
from random import randint, sample, shuffle, random

def generate_initial_population(population_size: int, colors: int) -> list:
    population = []
    for individual in range(0, population_size) :
        population.append([randint(0, colors - 1) for color in range(0, colors)])

    return population

def get_crossover_state(first_state, second_state):
    cutting_point = randint(1, len(first_state) - 1)

    first_child = first_state[0:cutting_point]
    first_child.extend(second_state[cutting_point:])
    second_child = second_state[0:cutting_point]
    second_child.extend(first_state[cutting_point:])

    return (first_child , second_child)



def genetic_graph_coloring(graph : Graph) :

    def evaluate(individual: list) -> int :
        n = graph.vertex_count
        score = 0
        k = len(set(individual))

        for vertex in range(n) :
            color = individual[vertex]
            if vertex + 1 in graph.edges.keys() :
                neighbours = graph.edges[vertex + 1]
            else :
                neighbours = []
            same_color_neighbours_count = len(list(filter(lambda neighbour: individual[neighbour - 1] == color, neighbours)))
            score += same_color_neighbours_count

        return (k + score) * n

    def has_bad_edge(vertex, individual):
        if(vertex + 1 not in graph.edges):
            return False

        neighbours = graph.edges[vertex + 1]
        for neighbour in neighbours:
            if(individual[vertex] == individual[neighbour - 1]):
                return True

        return False

    def has_conflict(individual) :
        n = len(individual)
        for vertex in range(n) :
            if has_bad_edge(vertex, individual) == True :
                return True
        return False

    def get_best_fitness(population) :
        colors_count = graph.vertex_count
        color_set = set(range(colors_count))
        n = graph.vertex_count

        for p in population :
            if has_conflict(p) == False :
                colors = set(p)
                if len(colors) < colors_count :
                    colors_count = len(colors)
                    color_set = colors
        return colors_count, color_set

    def squeeze(population) :
        n = graph.vertex_count
        population_copy = population.copy()
        for p in population_copy :
            for g in p :
                if g not in set_of_colors :
                    g = sample(set_of_colors, 1)[0]
        return population_copy

    def select(population, offspring) :
        po = []
        po.extend(population)
        po.extend(offspring)

        po.sort(key = lambda i: evaluate(i))
        return po[:M] + sample(po[M:], M // 2)

    def get_random_mutation(individual):
        if has_conflict(individual) == False :
            colors = set(individual)
            colors.remove(sample(colors, 1)[0])
            for g in individual :
                if g not in colors :
                    g = sample(colors, 1)[0]
            return individual
        else :
            for vertex in range(len(individual)) :
                print (vertex)
                color = individual[vertex]
                if vertex + 1 in graph.edges.keys() :
                    neighbours = graph.edges[vertex + 1]
                else :
                    neighbours = []

                best_score = evaluate(individual)
                best_color = color
                best_mutation = individual

                for neighbour in neighbours :
                    neighbour_color = individual[neighbour - 1]
                    if color == neighbour_color :
                        
                        for c in set_of_colors :
                            ic = individual[:]
                            ic[vertex] = c
                            score = evaluate(ic)
                            if score < best_score :
                                best_color = c
                                best_mutation = ic[:]
                                best_score = score  

                            nic = individual[:]
                            nic[neighbour - 1] = c
                            score = evaluate(nic)
                            if score < best_score :
                                best_color = c
                                best_mutation = nic[:]
                                best_score = score
                        break

            return best_mutation

    M = 50
    G = int(2e+2)
    O = M // 2

    crossover_prob = 0.3
    mutation_prob = 0.8

    P = generate_initial_population(M, graph.vertex_count)
    S = [graph.vertex_count ** 2 for _ in range(M)]

    for i in range(M) :
        S[i] = evaluate(P[i])

    number_of_colors = graph.vertex_count
    set_of_colors = set(range(number_of_colors)) 

    for i in range(G) :
        best_fitness, color_set = get_best_fitness(P)
        print (best_fitness)
        if best_fitness < number_of_colors :
            number_of_colors = best_fitness
            set_of_colors = color_set
            P = squeeze(P)

        shuffle(P)
        offspring = []

        for i in range(O) :
            p1, p2 = tuple(sample(P[:O], 2))

            print ("I: ", i)

            if random() < crossover_prob :
                o1, o2 = get_crossover_state(p1, p2)
                offspring.append(o1)
                offspring.append(o2)

            p = sample(P[O:], 1)[0]

            if random() < mutation_prob :
                o = get_random_mutation(p)
                offspring.append(o)

        P = select(P, offspring)

    best_p = P[0]
    best_score = evaluate(best_p)
    for p in P[:1] :
        if has_conflict(p) == False :
            score = evaluate(p)
            if score < best_score :
                best_score = score
                best_p = p

    print (best_p)
    print (score)

g = read_instance('.\\data\\fpsol2.i.1.col') 

genetic_graph_coloring(g)