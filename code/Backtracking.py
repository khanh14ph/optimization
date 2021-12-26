
def input(filename):
    with open(filename) as f:
        N,K = [int(x) for x in f.readline().split()]
        q = [int(x) for x in f.readline().split()]
        d = [[int(x) for x in f.readline().split()] for i in range(2*N+1)]
    return N,K,q,d
N,K,q,d = input('K3-N5.txt')


answer=float('inf')
segments=0
visited=[0 for i in range(2*N+5)]
load=[0 for i in range(2*N+5)]

y=[0 for i in range(2*N+5)]
x=[0 for i in range(2*N+5)]
path=[[0]*(2*N+5) for i in range(2*N+5)]



def case():
    global answer
    res=0 # result of this case
    for i in range(1,K+1):
        if load[i]:
            return
    for i in range(1,K+1):
        h=y[i]
        res+=d[0][h]
        while(h>0):
            res+=d[h][x[h]]
            h=x[h]

    answer = min(answer, res)

def CheckY(v):
    if visited[v]:
        return False
    return True

def CheckX(v,k):
    if v==0:
        if load[k]==0:
            return 1
        return 0
    if visited[v]:
        return 0
    if(v<=N):
        if load[k]+1 > q[k-1]:
            return 0
        return 1
    else:
        if path[k][v-N]:
            return 1
        else:
            return 0


def TryX(u,k): # u is node, k is k's route
    global segments
    for v in range(0,2*N+1):
        if CheckX(v,k):
            x[u]=v
            visited[v] = 1
            segments += 1
            if v!=0:
                if (v <= N):
                    load[k] += 1
                    path[k][v] += 1
                else:
                    load[k] -= 1
                    path[k][v - N] -= 1
            if v==0:
                if(k==K):
                    if segments==2*N+K:
                        case()
                else:
                    TryX(y[k+1],k+1)
            else:
                TryX(v,k)
            visited[v]=0
            segments -= 1
            if v!=0:
                if (v <= N):
                    load[k] -= 1
                    path[k][v] -= 1
                else:
                    load[k] += 1
                    path[k][v-N] += 1

def TryY(k):
    global segments
    for v in range(1,N+1):

        if CheckY(v):
            path[k][v]+=1
            y[k]=v
            load[k]+=1
            visited[v]=1
            segments += 1
            if k==min(N,K):
                TryX(y[1],1)
            else:
                TryY(k+1)
            visited[v]=0
            load[k] -=1
            segments -=1
            path[k][v] -= 1


TryY(1)
print(answer)