# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 22:43:45 2016

@author: nicolas
"""

from problem import Problem
import mipsolving
import protocols
import fairnessMeasures
from fairnessMeasures import fairnessDashboard
import numpy as np


def simulation(sample_size,int_agents,int_resources,culture,centralized=True):
    '''
    @sample_size: number of xps for each parameter configuration
    @int_agents: list of values to be considered
    @int_resources: list of values to be considered
    '''
    envies = np.zeros((len(int_agents),len(int_resources)))
    ef_ratios = np.zeros((len(int_agents),len(int_resources)))
    for idx_agent,n in enumerate(int_agents):
        for idx_res,m in enumerate(int_resources): 
            total_envy = 0
            nb_ef = 0
            for xp in range(sample_size):
                p = Problem(n,m,culture,centralized=True)
                # collecting statistics
                envy = mipsolving.envyminimizingLP(p)
                total_envy += envy
                if envy==0:
                    nb_ef += 1
            mean_envy = total_envy/sample_size
            ef_ratio = nb_ef / sample_size
            envies[idx_agent][idx_res] = mean_envy
            ef_ratios[idx_agent][idx_res]=ef_ratio
    return envies,ef_ratios
   
         
def simulationPickingSequences(sample_size,n,m,sequence,culture,verbose=False):
    '''
    for a given sequence, runs several simulations
    @sample_size: number of xps for each parameter configuration
    @n: nb of agents
    @m: nb of resources
    '''
    d = fairnessDashboard()    
    
    for xp in range(sample_size):
        p = Problem(n,m,culture,centralized=True)
        protocols.pickingSequence(p,sequence,verbose)
        if verbose:
            print(p)
            print (p.printAllocation())
        d.update(p)
    print(d)
    return
                
                
def simulationLipton(sample_size,n,m,culture,verbose=False):  
    d = fairnessDashboard()    
        
    for xp in range(sample_size):
        p = Problem(n,m,culture,centralized=True)
        protocols.lipton(p,verbose)
        if verbose:
            print(p)
            print (p.printAllocation()) # print the final allocation
        d.update(p)
    print(d)
    return
            
    
            
###############################################################################
# Testing
###############################################################################    

'''
tested_resources = list(range(6,12))
print(simulation(20,[6],tested_resources,'normalized',centralized=True))
'''

#print(simulationPickingSequences(1000,4,7,[3,1,2,1,2,1,3],'borda',verbose=False))

simulationLipton(1,4,6,'borda',verbose=True)
