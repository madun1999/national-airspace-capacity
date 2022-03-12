from itertools import product
import time
import random
from graph import Graph
from flow import cxv_max_flow, max_flow
def random_graph_edges(n, p, max_f):
    # generator for edges of graph with n nodes, max flow of max_f
    # each edge is included with a probability of p 
    assert 0 < p <= 1
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < p: # no self loop
                yield str(i), str(j), random.randint(1, max_f) 

def random_graph(n, p, max_f):
    g = Graph("0", str(n-1), [str(x) for x in range(n)])
    for (i,j, w) in random_graph_edges(n, p, max_f):
        # print(i,j,w)
        g.set_edge(i,j,w)
    return g

def test_time(f, *x):
    # Given function f and arguments to apply x
    # return tuple (res, t)
    # res is the result of f(*x)
    # t is the time spent excecuting f(*x)
    t0 = time.time()
    res = f(*x)
    t1 = time.time()
    t = t1-t0
    return res, t

def test_flow_random_graphs(ns, ps, max_fs, funcs, n_iter=1,seed=42):
    random.seed(seed)
    for n,p, max_f in product(ns, ps, max_fs):
        for _ in range(n_iter):
            g = random_graph(n,p,max_f)
            for func in funcs:
                res, t = test_time(func, g, "0", str(n-1))
                print(f"func={func.__name__} {n=} {p=} {max_f=}: {res=} {t=}")

test_flow_random_graphs([1000], [0.5], [100], [cxv_max_flow, max_flow])
# test_flow_random_graphs([4], [0.5], [3], [cxv_max_flow, max_flow]) # must do cxv first