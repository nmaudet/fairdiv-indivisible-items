# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 19:34:47 2016

@author: nicolas
"""
import random
import fairnessmeasures
from problem import Problem


###############################################################################
# Adjusted Winner Procedure
###############################################################################

def adujstedwinner():
    pass
    return


###############################################################################
# Picking Sequences
###############################################################################


def generateSequence(n,m,type_sequence):
    '''
    @n: number of agents
    @m: number of resources
    @t: type of sequence (balanced, alternate; etc.)
    '''
    if (m%n)!=0:
        print("Warning: number of resources not divisible by number of agents")
    sequence = []
    if type_sequence == "repeated":
        pass
    if type_sequence == "balanced":
        s = list(range(1,n+1))
        s_inv = s[::-1]
        
        for i in range(int(m/(2*n))):
            sequence += s + s_inv         
        
    return sequence

def pickingSequence(p,sequence,verbose=False):
    '''
    given a problem p and a sequence s (of integers)
    simulates agents picking at their turn from agent 0
    (supposed to be used with auctionneer problem)
    '''
    if len(sequence)!=p.m:
        print("The sequence length is different from the number of resources!")
    for i in sequence:
        best_utility = -1
        for r in p.agent[0].hold:
            if p.agent[i].u[r]>best_utility:
                best_utility = p.agent[i].u[r]
                best_resource_to_pick = r
        if verbose==True:
            print ("agent ", i, " picks ", best_resource_to_pick)
        p.agent[i].getItem(best_resource_to_pick)
        p.agent[0].giveItem(best_resource_to_pick)
    return
   

###############################################################################
# Lipton et al.
###############################################################################

def lipton(p,verbose=True):
    '''
    runs the Lipton et al. protocol
    '''
    m = fairnessMeasures.envyMatrix(p)
    for j,r in enumerate(p.resources): # we allocate all resources one by one
        g = fairnessMeasures.buildEnvyGraph(m)
        if verbose:
            print(p.printAllocation())
            print("envy graph:", g)
            print ("allocating resource ", r)
        
        m = fairnessMeasures.envyMatrix(p)
        #g = fairnessMeasures.buildEnvyGraph(m)
        _,c = fairnessMeasures.checkCycle(g) # a cycle must exist
        while (c!=[]): # stop when acyclic graph
            if verbose:
                print("solving the cycle:",c)
            p.cycleReallocation(c)
            m = fairnessMeasures.envyMatrix(p)
            g = fairnessMeasures.buildEnvyGraph(m)
            _,c = fairnessMeasures.checkCycle(g) 
        
        for i in range(1,p.n):
            if not(fairnessMeasures.envied(m,i)):
                p.agent[i].getItem(r)
                p.agent[0].giveItem(r)
                break        
         
            #print(p.printAllocation())
        m = fairnessMeasures.envyMatrix(p)
    if verbose:
        g = fairnessMeasures.buildEnvyGraph(m)
        print("envy graph:", g)
    return


###############################################################################
# Local Exchanges
###############################################################################

def rationalSwapDeal(p,x,y,verbose=True):
    '''
    checks if there are rational 1-deal between agents x and y
    and performs all of them if possible (no further heuristic for choice)
    '''
    deal = False
    for rx in p.agent[x].hold: 
        for ry in p.agent[y].hold:
            if p.agent[x].u[rx]<p.agent[x].u[ry] and p.agent[y].u[rx]>p.agent[y].u[ry]:
                if verbose == True:                 
                    print ("deal between ", x, " and ", y, "for ", rx, " and ", ry)
                p.agent[x].getItem(ry)
                p.agent[x].giveItem(rx)
                p.agent[y].getItem(rx)
                p.agent[y].giveItem(ry)
                deal = True
                break
    return deal
                
                
def randomDynamics(p):
    testedPairs = []
    allPairs = [(x,y) for x in range(p.n) for y in range(p.n)]
    #random.shuffle(allPairs)
    
    while len(testedPairs) != len(allPairs): 
        candidatePairs = [(x,y) for (x,y) in allPairs if (x,y) not in testedPairs]   
        #print (candidatePairs)
        # choice in all pairs - tested
        (x,y) = random.choice(candidatePairs)    
    
        if not(rationalSwapDeal(p,x,y)):
            testedPairs += (x,y)
        else:
            testedPairs = []
            print (p.printAllocation())
    return

     




