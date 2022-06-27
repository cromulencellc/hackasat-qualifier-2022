#!/usr/bin/env pypy3

import json
import os

class Gen():
    BITS = 16
    MAXNUM = (2** BITS) - 1
    LOOKUP_PATH = "lookup.json"
    OPTMOVES_PATH = "OptMoves.json"

    def __init__(self, bits=BITS):
        if bits != Gen.BITS:
            if bits % 2:
                raise ValueError("Bits must be divisible by 2")
            
            Gen.BITS = bits
            Gen.MAXNUM = (2** Gen.BITS) - 1

        self.elems = list()
        self.partitions = [0]
        self.members = [0] * (Gen.MAXNUM+1)
        self.poss = dict()
        self.scores = None
    
        if os.path.exists(Gen.OPTMOVES_PATH) and os.path.isfile(Gen.OPTMOVES_PATH):
            with open(Gen.OPTMOVES_PATH, "r") as f:
                self.best_moves = json.load(f)
            
            if len(self.best_moves) != Gen.BITS+1:
                self.generate()
        else:
            self.generate()

        self.lookup_by_diff = dict(enumerate(self.best_moves))
    
    @staticmethod
    def rotate(k):
        k *= 2
        return (k - Gen.MAXNUM) if k > Gen.MAXNUM else k

    def generate(self):
        print(f"Generating for the first time for {Gen.BITS}. This may take a minute...")

        self.find_unique_rot_nums()
        self.best_moves = self.find_moves_overlap()

        # Store results in jsons
        self.store_ranks()
        self.store_optimal_moves()

    def find_unique_rot_nums(self):
        '''
        Find unique elements based off rotations and put into partitions
        '''
        for ind in range (1,Gen.MAXNUM+1):
            self.elems.append(ind)

        elemInd = 0
        self.members[0] = elemInd

        while len(self.elems)> 0 :
            
            elemInd += 1
            z = self.elems[0]
            self.partitions.append(z)
            x = z
            
            while x in self.elems:
                self.members[x] = elemInd
                self.elems.remove(x)
                x = Gen.rotate(x)
    
    def find_all_vals_rot(self):
        '''
        For every pair non zero elements find all possible values after rotation  
        '''
        self.poss = dict()

        # calc upper triangle of matrix
        for i in range(len(self.partitions)):
            for j in range(i,len(self.partitions)):
                rots = set()
                a = self.partitions[i]
                b = self.partitions[j]
                for ind in range(Gen.BITS):
                    n = a^b  
                    rots.add(self.members[n])
                    b = Gen.rotate(b)
                self.poss[(i,j)] = rots
        
        # copy upper triangle into lower triangle
        for i in range(1,len(self.partitions)):
            for j in range(i):
                self.poss[(i,j)] = self.poss[(j,i)]

    def calc_scores(self):
        '''
        Calculate scores of every non zero unique element
        '''
        self.find_all_vals_rot()

        maxscore = len(self.partitions)+1
        scores = [maxscore] * len(self.partitions)
        scores[0] = 0
        prevscores  = sum(scores) + 10

        while (sum(scores) < prevscores):
            prevscores = sum(scores)
            for i in range(1,len(self.partitions)):
                if scores[i] == maxscore:
                    rankscore = maxscore
                    for j in range(1,len(self.partitions)):
                        opscore = 0
                        x = self.poss[(i,j)]
                        for k in x:
                            opscore = max(opscore, scores[k])
                        rankscore = min(rankscore, opscore)
                    scores[i] = min(scores[i],(rankscore + 1))

        self.scores = scores
    
    def calc_good_moves(self):
        '''
        For each non zero element find the list of guesses that produce good results
        good meaning resulting in a lower score
        '''
        if not self.scores:
            self.calc_scores()

        goodMoves = dict()
        for i in range(1,len(self.partitions)):
            for j in range(1,len(self.partitions)):
                opscore = 0
                x = self.poss[(i,j)]
                for k in x:
                    opscore = max(opscore, self.scores[k])
                if opscore < self.scores[i]:
                    if i not in goodMoves:
                        goodMoves[i] = []
                    goodMoves[i].append(j)

        return goodMoves

    def find_moves_overlap(self):
        '''
        Finds overlap of the goodmoves for  all elements of a given score
        '''

        goodMoves = self.calc_good_moves()

        if not goodMoves:
            return

        optMove = dict()

        for i in range(1, len(self.partitions)):
            if self.scores[i] not in optMove:
                optMove[self.scores[i]] = set(goodMoves[i])
            else:
                optMove[self.scores[i]] = optMove[self.scores[i]].intersection(set(goodMoves[i]))
        #  ends here

        # picks an arbitrary optimal move for each level and stores in a json file
        bestMove = [0]
        for i in range(1,max(self.scores) + 1):
            bestMove.append(self.partitions[optMove[i].pop()])
    
        return bestMove
    
    def calc_ranks(self):
        '''
        Use element score to calculate the score for each register value
        '''
        if not self.scores:
            self.calc_scores()
        
        ranks = [0] * (Gen.MAXNUM+1)
        for ind in range(len(ranks)):
            ranks[ind] = self.scores[self.members[ind]]

        return ranks
        
    def store_ranks(self):
        ranks = self.calc_ranks()

        with open("lookup.json", "w") as f:
            json.dump(ranks, f)

    def store_optimal_moves(self):
        bestMove = self.find_moves_overlap()

        if bestMove:
            with open("OptMoves.json", "w") as f:
                json.dump(bestMove, f)
            return True
        
        return False

def test():
    g = Gen(2)
    assert(g.best_moves == [0, 3, 1])

    g = Gen(4)
    assert(g.best_moves == [0, 15, 5, 3, 7])
    
    g = Gen(8)
    assert(g.best_moves == [0, 255, 85, 51, 119, 45, 95, 111, 127])
    
    g = Gen(16)
    assert(g.best_moves == [0, 65535, 21845, 13107, 30583,
                            11565, 24415, 28527, 32639, 11475, 
                            24055, 28407, 30719, 28095, 32255, 
                            32511, 32767])

if __name__ == "__main__":
    test()