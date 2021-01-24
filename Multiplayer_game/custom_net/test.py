import timeit
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
import random

def build_deque(n):
    items = [random.randint(0,50) for i in range(n)]
    
    return deque(items)

def iter_index(d):
    val = d[0]
    temp = deque()
    for x in d:
        if x != val:
            temp.appendleft(x)
    d = deque(temp)

def iter_it(d):
    val = d[0]
    temp = list(d)
    for x in range(len(temp)):
        if temp[x] == val:
            temp[x] = None
    temp = set(temp)
    d = deque(temp)

def new(d):
    val = d[0]
    for i,v in enumerate(d):
        if v == val:
            d[i] = None
    temp = set(d)
    temp.remove(None)
    d = deque(temp)
    

r = range(100, 10001, 100)
#print('starting')
#index_runs = [timeit.timeit('iter_index(d.copy())', 'from __main__ import build_deque, iter_index, iter_it,new; d = build_deque({})'.format(n), number=1000) for n in r]
#print('it_runs')
it_runs = [timeit.timeit('iter_it(d.copy())', 'from __main__ import build_deque, iter_index, iter_it,new; d = build_deque({})'.format(n), number=1000) for n in r]
print('last')
new = [timeit.timeit('new(d.copy())', 'from __main__ import build_deque, iter_index, iter_it,new; d = build_deque({})'.format(n), number=1000) for n in r]

df = pd.DataFrame({'index':it_runs,'set':new}, index=r)
df.plot()
plt.show()