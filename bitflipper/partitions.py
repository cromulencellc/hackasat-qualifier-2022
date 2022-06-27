#!/usr/bin/env pypy3

import json

BITS = 8
MAXNUMB = (2** BITS) - 1
elems = list()
partions = [0]
members =  [0]  * (MAXNUMB+1) 

def rotate(k):
    tmp = 2 * k
    if(tmp > MAXNUMB):
        tmp -= MAXNUMB
    return tmp
    
for ind in range (1,MAXNUMB+1):
    elems.append(ind)

elemInd = 0
members[0] = elemInd

while len(elems)> 0 :
    
    elemInd += 1
    z = elems[0]
    partions.append(z)
    x = z
    
    while x in elems:
        members[x] = elemInd
        elems.remove(x)
        x = rotate(x)

poss = dict()
for i in range(len(partions)):
    for j in range(len(partions)):
        rots = set()
        a = partions[i]
        b = partions[j]
        for ind in range(BITS):
            n = a^b
            rots.add(members[n])
            b = rotate(b)
        poss[(i,j)] = rots

        
scores = [2*len(partions)] * len(partions)
scores[0] = 0
prevscores  = 2 * sum(scores)

while (sum(scores) < prevscores):
    prevscores = sum(scores)
    for i in range(1,len(partions)):
        rankscore = 2 * len(partions)
        for j in range(1,len(partions)):
            opscore = 0
            x = poss[(i,j)]
            for k in x:
                opscore = max(opscore, scores[k])
            rankscore = min(rankscore, opscore)
        scores[i] = min(scores[i],(rankscore + 1))
        
rank = [0]* (MAXNUMB+1)
for ind in range(len(rank)):
    rank[ind] = scores[members[ind]]

with open("save.json", "w") as f:
    json.dump(rank, f)

print(rank)

x = [0, 4, 4, 3, 4, 2, 3, 4, 4, 3, 2, 4, 3, 4, 4, 1]