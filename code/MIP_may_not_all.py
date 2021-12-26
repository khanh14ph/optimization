import time
from ortools.linear_solver import pywraplp
import numpy as np

begin = time.time()


def input(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        c = [int(x) for x in f.readline().split()]

        d = [[int(x) for x in f.readline().split()] for i in range(2 * n + 1)]

    return n, k, c, d


import numpy as np

n, k, c, d = input('bus.txt')


print(c)
c1 = c.copy()
A = []
for i in range(2 * n + 1):
    for j in range(2 * n + 1):
        if (i != j) and not (i <= n and j == 0) and not (i == 0 and j >= n + 1) and not (i == j + n):
            A.append([i, j])

Ao = lambda x: (j for i, j in A if i == x)
Ai = lambda x: (i for i, j in A if j == x)
#
M = 10 * n
total_demand = max(c)
solver = pywraplp.Solver('testdata.txt', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
#
INF = solver.infinity()
#
# Decision variables
x = [[[solver.IntVar(0, 1, f'x[{q}][{i}][{j}]') for j in range(2 * n + 1)] for i in range(2 * n + 1)] for q in range(k)]
#
y = [solver.IntVar(0, total_demand, f'y[{i}]') for i in range(2 * n + 1)]
#
z = [solver.IntVar(0, k, f'z[{i}]') for i in range(2 * n)]
# Biến quyết định b xem i có dc visited trước j ko
b = [[solver.IntVar(0, 1, f'x[{i}][{j}]') for j in range(2 * n + 1)] for i in range(2 * n + 1)]
for i in range(1, 2 * n + 1):
    cstr = solver.Constraint(1, 1)
    for q in range(k):
        for j in Ao(i):
            cstr.SetCoefficient(x[q][i][j], 1)
###########################
for i in range(1, 2 * n + 1):
    cstr = solver.Constraint(1, 1)
    for q in range(k):
        for j in Ai(i):
            cstr.SetCoefficient(x[q][j][i], 1)
#############

###############
for i in range(0,2*n+1):
    for q in range(k):
        cstr = solver.Constraint(0, 0)
        for j in Ao(i):
            cstr.SetCoefficient(x[q][i][j], 1)
        for j in Ai(i):
            cstr.SetCoefficient(x[q][j][i], -1)

for q in range(k):
    cstr=solver.Constraint(0,1)
    for i in Ao(0):
        cstr.SetCoefficient(x[q][0][i],1)

    cstr = solver.Constraint(0, 1)
    for i in Ai(0):
        cstr.SetCoefficient(x[q][i][0],1)
for q in range(k):
    cstr=solver.Constraint(0,0)
    for i in Ao(0):
        cstr.SetCoefficient(x[q][0][i],1)
    for j in Ai(0):
        cstr.SetCoefficient(x[q][i][0],-1)
for q in range(k):
    for i, j in A:
        if i != 0:
            cstr = solver.Constraint(-M - c[q], INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(y[i], -1)
        if j != 0:
            cstr = solver.Constraint(-M - c[q], INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(y[j], -1)

for q in range(k):
    for i, j in A:
        if 0 < j <= n:
            cstr = solver.Constraint(-M + 1, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(y[j], 1)
            cstr.SetCoefficient(y[i], -1)

            cstr = solver.Constraint(-M - 1, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(y[j], -1)
            cstr.SetCoefficient(y[i], 1)
        if j > n:
            cstr = solver.Constraint(-M - 1, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(y[j], 1)
            cstr.SetCoefficient(y[i], -1)

            cstr = solver.Constraint(-M + 1, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(y[j], -1)
            cstr.SetCoefficient(y[i], 1)
    for i, j in A:
        if i != 0 and j != 0:
            cstr1 = solver.Constraint(-M, INF)
            cstr1.SetCoefficient(x[q][i][j], -M)
            cstr1.SetCoefficient(z[j - 1], 1)
            cstr1.SetCoefficient(z[i - 1], -1)

            cstr2 = solver.Constraint(-M, INF)
            cstr2.SetCoefficient(x[q][i][j], -M)
            cstr2.SetCoefficient(z[j - 1], -1)
            cstr2.SetCoefficient(z[i - 1], 1)
            #
            cstr3 = solver.Constraint(-M + q, INF)
            cstr3.SetCoefficient(x[q][i][j], -M)
            cstr3.SetCoefficient(z[i - 1], 1)

            cstr = solver.Constraint(-M - q, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(z[i - 1], -1)
for i in range(n):
    cstr = solver.Constraint(0, 0)
    cstr.SetCoefficient(z[i], 1)
    cstr.SetCoefficient(z[i + n], -1)
c = solver.Constraint(0, 0)
c.SetCoefficient(y[0], 1)
################
for q in range(k):
    for i in range(1, 2 * n + 1):
        for j in range(1, 2 * n + 1):
            cstr = solver.Constraint(-INF, 0)
            cstr.SetCoefficient(x[q][i][j], 1)
            cstr.SetCoefficient(b[i][j], -1)

for q in range(k):
    for i, j in A:
        if i != 0 and j != 0:
            cstr = solver.Constraint(-M + 1, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(b[i][j], 1)

            cstr = solver.Constraint(-M - 1, INF)
            cstr.SetCoefficient(x[q][i][j], -M)
            cstr.SetCoefficient(b[i][j], -1)

for q in range(k):
    for i, j in A:
        if i != 0 and j != 0:
            cstr = solver.Constraint(-M, INF)
            cstr.SetCoefficient(x[q][j][i], -M)
            cstr.SetCoefficient(b[i][j], 1)

            cstr = solver.Constraint(-M, INF)
            cstr.SetCoefficient(x[q][j][i], -M)
            cstr.SetCoefficient(b[i][j], -1)

for i in range(1, n + 1):
    cstr = solver.Constraint(1, 1)
    cstr.SetCoefficient(b[i][i + n], 1)
for q in range(k):
    for i in range(1, 2 * n + 1):
        cstr = solver.Constraint(0, 0)
        cstr.SetCoefficient(b[i][i], 1)
for i in range(1, n + 1):
    cstr = solver.Constraint(0, 0)
    cstr.SetCoefficient(b[n + i][i], 1)

for q in range(k):
    for i in range(1, 2 * n + 1):
        for j in range(1, 2 * n + 1):
            if j != i:
                for u in range(1, 2 * n + 1):
                    if u != i and u != j:
                        cstr = solver.Constraint(-M, INF)
                        cstr.SetCoefficient(x[q][i][j], -M)
                        cstr.SetCoefficient(b[u][i], 1)
                        cstr.SetCoefficient(b[u][j], -1)

                        cstr = solver.Constraint(-M, INF)
                        cstr.SetCoefficient(x[q][i][j], -M)
                        cstr.SetCoefficient(b[u][i], -1)
                        cstr.SetCoefficient(b[u][j], 1)

                        cstr = solver.Constraint(-M, INF)
                        cstr.SetCoefficient(x[q][i][j], -M)
                        cstr.SetCoefficient(b[i][u], 1)
                        cstr.SetCoefficient(b[j][u], -1)

                        cstr = solver.Constraint(-M, INF)
                        cstr.SetCoefficient(x[q][i][j], -M)
                        cstr.SetCoefficient(b[i][u], -1)
                        cstr.SetCoefficient(b[j][u], 1)

obj = solver.Objective()
for q in range(k):
    for i, j in A:
        obj.SetCoefficient(x[q][i][j], d[i][j])
obj.SetMinimization()

rs = solver.Solve()
#
print(f'Optimal objective value = {obj.Value()}')


#
def findNext(q, i):
    for j in Ao(i):
        if x[q][i][j].solution_value() > 0:
            return j


def route(q):
    s = '0 - '
    i = findNext(q, 0)

    while i != 0:
        s = s + str(i) + ' - '
        i = findNext(q, i)
    s = s + str(0)
    return s


for q in range(k):
    print('capacity : ', c1[q])
    print('route[', q, '] = ', route(q))
    for i, j in A:
        if x[q][i][j].solution_value() > 0:
            print('(', i, '-', j, ')')
import numpy as np

data = np.random.rand(k, 2 * n + 1, 2 * n + 1)
end = time.time()
print('time:', end - begin)

