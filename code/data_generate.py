import numpy as np

def gen(filename,K,N):
#K : number of trucks
#N : number of customers
    c=[np.random.randint(1,2) for i in range(K)]
    M = 2*N+1
    d = [[abs(int(np.random.normal(15,30))) for i in range(M)] for j in range(M)]
    for i in range (len(d)):
        d[i][i]=0
    for i in range(len(d)):
        for j in range(len(d)):
            if d[i][j]==0 and i!=j:
                d[i][j]+=1
    f = open(filename,'w')
    f.write(str(N) + ' ' + str(K) + '\n')
    line = ''
    for ci in c:
        line = line + str(ci) + ' '
    f.write(line + '\n')
    for i in range(M):
        line = ''
        for j in range(M):
            line = line + str(d[i][j]) + ' '
        f.write(line + '\n')

gen('K30-N100.txt',30,100)