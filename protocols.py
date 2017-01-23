# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 19:34:47 2016

@author: nicolas
"""
import heapq
import random
import fairnessMeasures
from problem import Problem


###############################################################################
# Adjusted Winner Procedure
###############################################################################

def adjustedWinner(p,verbose=True):
    '''
    runs the adjusted winner on problem p
    to be used with centralized problem
    and only two agents
    '''
    if p.n!=3:
        print("Warning: Adjusted Winner must be used with two agents.")
        print("Note: Only the two first agents will be considered.")
    # the allocation phase
    for r in p.agent[0].hold:
        if p.agent[1].u[r]>p.agent[2].u[r]:
            p.agent[1].getItem(r)
        else:
            p.agent[2].getItem(r)     
    if verbose:
        print ("Allocation phase:")
        print (p.printAllocation())
    # happiest / sadest agent
    if p.agent[1].current_u>p.agent[2].current_u:
        high, low = 1,2
    else:
        high, low = 2,1
    # ranking the resources (of the rich)
    h = [] # using a heapqueue with u_h/u_l as comparison value
    for r in p.agent[high].hold:  
        ratio = p.agent[high].u[r] / p.agent[low].u[r]
        ratio = round(ratio,3) # to use the float as a dict key
        heapq.heappush(h,(ratio,r))
    print (h)
    # now inspect resources by priority oder
    while p.agent[high].current_u>p.agent[low].current_u:
        _,r = heapq.heappop(h)
        p.agent[low].getItem(r)
        p.agent[high].giveItem(r)
        if verbose:
            print ("Resource ",r , " moves from ", high, " to ", low)
    if p.agent[1].current_u != p.agent[2].current_u:
        part_of_low = (p.agent[low].current_u - p.agent[high].current_u) / \
        (p.agent[high].u[r]+p.agent[low].u[r])
        if verbose:
            print ("Resource ", r, " will be splitted!")
            print ("Agent ", low, " gets ", round(part_of_low,3), " of resource ", r)
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
        best_resource_to_pick=""
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

     




