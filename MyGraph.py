class MyGraph:

    def __init__(self, g={}):
        self.graph = g

    def print_graph(self):
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    def tupl(self, lst):
        #retorna todos os nós do grafo
        lst1 = []
        for tup in lst:
            lst1.append(tup[0])
        return lst1

    
    ## get basic info

    def get_nodes(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    def size(self):
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges

    def add_vertex(self, v):
        if v not in self.graph.keys():
            self.graph[v] = []

    def add_edge(self, o, d, cost):
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append((d, cost))

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        ''' Função que transforma uma lista de tuplos dada numa lista com os primeiros valores do tuplo'''
        return self.tupl(list(self.graph[v]))  # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v):
        ''' Função que transforma uma lista de tuplos dada numa lista com os primeiros valores do tuplo'''
        #para não dar erro com o tuplo acrescentei self.tupl
        res = []
        lst = self.get_nodes()
        for value in lst:
            if v in self.tupl(self.graph[value]):
                res.append(value)
        return res

    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = list(set(suc + pred))
        return res

    ## degrees

    def out_degree(self, v):
        len(self.graph[v])

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v))

    ## BFS and DFS searches

    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v:
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res

    def reachable(self, v, fs='bfs'):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if fs == 'bfs':
                    if elem not in res and elem not in l and elem != node:
                        l.append(elem)
                else:
                    if elem not in res and elem not in l:
                        l.insert(s, elem)
                        s += 1
        return res

    def shortest_path(self, s, d):
        '''Segue o trajeto dod pontos olhando apenas para os custos minimos da viagem. No entanto apresenta o erro de
        como ele apenas segue o custo mais baixo, ele pode retornar None por seguir um trajeto que acaba quando não
        consegue avançar mais (retorna None) ou quando chega ao objetivo (retorna lista de saltos e custo desse trajeto
        que será o custo mínimo). É o que falta corrigir!'''
        if s == d: return [s, d]
        l = [(s, [], 0)]
        visited = [s]
        while len(l) > 0:
            node, path, dist = l.pop(0)
            min_cost = 999999999
            for elem in self.graph[node]:
                vertice, cost = elem
                if vertice == d:
                    return path + [(node, vertice)], dist + cost
                if cost < min_cost:
                    min_cost = cost
                    vert_min_cost = vertice
            if vert_min_cost not in visited and vert_min_cost not in l and vert_min_cost != node:
                l.append((vert_min_cost, path + [(node, vert_min_cost)], dist + min_cost))
                visited.append(vert_min_cost)
        return None

    def distance(self, s, d):
        ''' Com o algoritmo djikstra a distância entre dois pontos será o custo total do trajeto calculado na função
        shortest_path. Por isso chamamos o shortest path e apenas imprimimos nesta função o custo do trajeto mais curto.
        '''

        if s == d: return 0
        way = self.shortest_path(s, d)
        if way is not None:
            return way[1]
        return None

    def reachable_with_dist(self, s):
        '''Funciona como a função dada na aula apenas acrescentamos a função self.tupl para não haver erros'''
        res = []
        l = [(s, 0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node, dist))
            for elem in self.tupl(self.graph[node]):
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem):
                    l.append((elem, dist + 1))
        return res

    ## cycles
    def node_has_cycle(self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list(tl, val):
    res = False
    for (x, y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph({1: [(2, 0)], 2: [(3, 1)], 3: [(2, 2), (4, 0)], 4: [(2, 4)]})
    gr.print_graph()
    print(gr.get_nodes())
    print(gr.get_edges())
    print(gr.graph)


def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)

    gr2.add_edge(1, 2, 0)
    gr2.add_edge(2, 3, 2)
    gr2.add_edge(3, 2, 1)
    gr2.add_edge(3, 4, 3)
    gr2.add_edge(4, 2, 4)

    gr2.print_graph()
    print(gr2.graph)


def test3():
    gr = MyGraph({1: [(2, 0)], 2: [(3, 1)], 3: [(2, 2), (4, 0)], 4: [(2, 4)]})
    gr.print_graph()

    print(gr.get_successors(2))
    print(gr.get_predecessors(2))
    print(gr.get_adjacents(2))
    print(gr.in_degree(2))
    print(gr.out_degree(2))
    print(gr.degree(2))


def test4():
    gr = MyGraph({1: [(2, 0)], 2: [(3, 1)], 3: [(2, 2), (4, 0)], 4: [(2, 4)]})

    print(gr.distance(1, 4))
    print(gr.distance(4, 3))

    print(gr.shortest_path(1, 4))
    print(gr.shortest_path(4, 3))

    print(gr.reachable_with_dist(1))
    print(gr.reachable_with_dist(3))
    print(gr.graph)

    gr2 = MyGraph({1: [(2, 0), (3, 1)], 2: [(4, 4)], 3: [(5, 0)], 4: [], 5: []})

    print(gr2.distance(2, 1))
    print(gr2.distance(1, 5))

    print(gr2.shortest_path(1, 5))
    print(gr2.shortest_path(2, 1))

    print(gr2.reachable_with_dist(1))
    print(gr2.reachable_with_dist(5))
    print(gr2.graph)


def test5():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    print(gr.node_has_cycle(2))
    print(gr.node_has_cycle(1))
    print(gr.has_cycle())

    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})
    print(gr2.node_has_cycle(1))
    print(gr2.has_cycle())
    print(gr2.graph)


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
