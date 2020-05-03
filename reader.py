class Graph :
    def __init__(self, vertex_count: int, edge_count: int, edges: list) :
        if vertex_count <= 0 :
            raise Exception("Invalid vertex count")

        if edge_count < 0 and len(edges) != edge_count :
            raise Exception("Invalid edge count")

        self.vertex_count = vertex_count
        self.edge_count = edge_count
        self.edges = edges
    def __repr__(self) -> str:
        return str(self.__dict__)

def read_instance(file_path: str) -> Graph :
    f = open(file_path, 'r') 

    edges = {}
    while True: 
        line = f.readline()
  
        if not line: 
            break

        if line.find("p") == 0 :
            vertex_count = int(line.split()[2].strip())
            edge_count = int(line.split()[3].strip())
        elif line.find("e") == 0 :
            v1 = int(line.split(' ')[1].strip())
            v2 = int(line.split(' ')[2].strip())
            append_or_update(edges, v1, v2)
            append_or_update(edges, v2, v1)
        elif line.find("c") == 0 :
            pass

    return Graph(vertex_count, edge_count, edges)

def append_or_update(edges, key, value):
    if(key in edges):
        edges[key].append(value)
    else:
        edges[key] = [value]

    return edges

if __name__ == '__main__' :
    from os import listdir
    from os.path import isfile, join

    dir_path = '.\\data'
    files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f))]
    graphs = list(map(read_instance, files))

    print (graphs)
    print (len(graphs))