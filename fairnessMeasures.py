# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:21:47 2016

@author: nicolas
"""

from problem import Problem
import numpy as np


def envyMatrix(p):
    '''
    returns the envy matrix of a mara problem
    '''
    m =np.zeros((p.n,p.n))
    for x in range(p.n):
        for y in p.visibility_graph[x]:
    #for (x,y) in p.visibility_graph:
            utility_bundle_other = 0
            for r in p.agent[y].hold: 
                utility_bundle_other +=p.agent[x].u[r]
            m[x][y] =  max(0,utility_bundle_other - p.agent[x].current_u)
    return m

def envied(m,i):
    '''
    @m: an envy matrix
    @i: an agent
    returns whether an agent is envied
    '''
    (n,n) = m.shape
    return sum([m[j][i] for j in range(n)])!=0
    
def nbEnviousAgents(m):
    (n,n) = m.shape
    nb =0
    for x in range(n):
        if sum([m[x][y] for y in range(n)])>0:
            nb +=1
    return nb
    
def isEnvyFree(m):
    return (nbEnviousAgents(m)==0)
    
def maxEnvy(m):
    return np.max(m)

    
def egalitarianSW(p):
    if p.centralized:
        return min([p.agent[i].current_u for i in range(1,p.n)])
    else:
        return min([p.agent[i].current_u for i in range(0,p.n)])

        
        
        
def buildEnvyGraph(m):
    '''
    given an envy matrix, build the envy graph (as a dictionary)
    '''
    # eg = p.visibility_graph
    (n,n) = m.shape
    #for x,envied in eg:
    #    if m[x]
        
    eg = dict([(x,[]) for x in range(n)]) # graph
     
    for x in range(n):
        for y in range(n):
            if m[x][y]>0:
                eg[x].append(y)  
     
    #eg = [(x,y) for x in range(n) for y in range(n) if m[x][y]>0]
    return eg
    

def checkCycle(g):
    '''
    check cycle in an envy graph via dfs
    returns a cycle or empty list if none
    '''
    visited = dict([(x,0) for x,envied in g.items()])
    #TODO: need to return a cycle if there is one
    path =[]
    cycle_found = [False] 


    def dfsSearch(x,cycle_found):
        # labelling: 0 not explored, 1 currently explored, 2 closed
        #print(visited)
        if cycle_found[0]:
            return
        visited[x] = 1
        for enviedAgent in g[x]:
            #print ("Reaching ", str(enviedAgent))
            if visited[enviedAgent] == 1:
                cycle_found[0]=True
                return
            if visited[enviedAgent] == 0:
                path.append(enviedAgent)
                dfsSearch(enviedAgent,cycle_found)
        visited[x] = 2
        return
    
    for x,enviedAgents in g.items(): 
        if visited[x] == 0:
            path = [x]
            cycle = []
            dfsSearch(x,cycle_found)
        if cycle_found[0]:
            #print (visited)
            #print(path)
            cycle = path
            #for x in path[:-1]:
            #    if (x not in cycle) :
            #        cycle.append(x)
            #print(cycle)
            break
            
    return cycle_found[0],cycle



    
def proportionality(p):
    '''
    returns the list of proportional fair share for each agent
    '''
    pfs = []
    if p.centralized:
        nb_agents=(p.n)-1
    else:
        nb_agents=p.n
    for x in p.agent:
        pfs.append(sum([x.u[r] for r in p.resources])/float(nb_agents))
    return pfs
    
def isProportional(p):
    '''
    returns whether proportional
    '''
    pfs=proportionality(p)
    deb=0
    if p.centralized:
        deb=1
    for i in range(deb,p.n):
        if p.agent[i].current_u<pfs[i]:
            return False
    return True
    
    
        
class fairnessDashboard(object):
    '''
    records different fairness metrics
    '''
    def __init__(self):
        self.sample_size = 0
        self.egalitarianSW=[]
        self.proportional=[]
        self.envyFree = []
        self.nbEnvious = []
        self.maxEnvy = []
        return
        
    def __str__(self):
        s="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        s += "= Number of experiments: "+str(self.sample_size).rjust(20)+"\n"
        s += "= Average egalitarian sw: "+str(np.mean(self.egalitarianSW)).rjust(21)+"\n"
        s += "= Ratio of proportional: "+str(np.mean(self.proportional)).rjust(20)+"\n"
        s += "= Ratio of envy free: "+str(np.mean(self.envyFree)).rjust(24)+"\n"
        s += "= Average number of envious: "+str(np.mean(self.nbEnvious)).rjust(17)+"\n"
        s += "= Average max envy: "+str(np.mean(self.maxEnvy)).rjust(26)+"\n"
        s +="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        return s
        
    def update(self,p):
        '''
        update the dashboard given a new problem
        '''
        self.sample_size += 1
        self.egalitarianSW.append(egalitarianSW(p))
        self.proportional.append(isProportional(p))
        m = envyMatrix(p)
        self.envyFree.append(isEnvyFree(m))
        self.nbEnvious.append(nbEnviousAgents(m))
        self.maxEnvy.append(maxEnvy(m))
        return
    
    



###############################################################################
# Testing
    
'''    
    
p1 = Problem(4,4,'borda','random','complete')
p2 = Problem(4,4,'uniform','random','complete')
m2 = envyMatrix(p2)
print (p2.visibility_graph)
print (m2)
print (proportionality(p2))
eg2 = buildEnvyGraph(m2)
print (eg2)

print (checkCycle(eg2))

#print (checkCycle({0: [], 1: [0, 3], 2: [1], 3: [0]}))
#print (checkCycle({0: [1, 2], 1: [2], 2: [], 3: [1, 2]}))
    
# does not return correct cycle
print (checkCycle({0: [1, 2], 1: [0], 2: [0, 1], 3: [0, 1, 2]}))
'''

#print (checkCycle({0: [1, 2], 1: [0], 2: [0, 1], 3: [0, 1, 2]}))

#print (checkCycle({0: [2], 1: [0, 3], 2: [1], 3: [0]}))

#print (checkCycle({0: [1, 2], 1: [2], 2: [], 3: [1, 2]}))

#print (checkCycle({0: [], 1: [0, 2, 3], 2: [0, 3], 3: [0, 1]}))

#print (checkCycle({0: [], 1: [2, 3], 2: [3], 3: [1]}))