# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 09:38:54 2016

@author: nicolas
"""

'''
Fair Division of Indivisible Goods
Companion code for the chapter 12 of the Handbook of CSC 
'''

import random

def generateUtilities(n,resources,culture):
        '''
        @n: number of agents
        @resources: resources
        @culture: type of culture (uniform,borda,normalized,gauss)
        '''
        u_min=1
        u_max=99
        utilities = {r:0 for r in resources}
        intrinsic_utilities = {r:0 for r in resources}
        all_utilities = []
        if culture=='gauss':
            for r in resources:
                    intrinsic_utilities[r]=random.randrange(u_min,u_max)
    
        for i in range(n): 
            if culture == 'uniform': # 
                for r in resources:
                    u = random.randrange(u_min,u_max)
                    utilities[r]=u
            elif culture == 'borda': # utilities = rank
                random.shuffle(resources)
                for r in resources:
                    utilities[r]=resources.index(r)+1
            elif culture == 'normalized': # quick-and-dirty normalisation via rounding
                for r in resources:
                    u = random.randrange(u_min,u_max)
                    utilities[r]=u
                sum_of_utilities = sum([utilities[r] for r in resources])
                for r in resources:
                    utilities[r]=round(utilities[r]/sum_of_utilities,3)
            elif culture == 'gauss': # picks an intrinsic value for resources
                for r in resources:
                    pass
                    #TODO: draw with gauss from intrinsic
            elif culture == 'empty':
                pass
            all_utilities += utilities
        return utilities
        #TODO: adapt when calling since now all agents utilities are produced
        
def generateAllocation(n,resources,alloc):
    '''
    returns a dictionary resource:agent
    '''
    if alloc == 'random':        
    #allocates each resource uniformly at random
        allocation = {r:random.randint(0,n-1) for r in resources}
    elif alloc == 'auctioneer':
    #allocates all resources to agent 0    
        allocation = {r:0 for r in resources}
    return allocation
    
def generateTopology(n,topo):
    # complete, centralised, circle
    visibility_graph = {i:[] for i in range(n)}
    exchange_graph = {i:[] for i in range(n)}
    if topo == 'complete': 
        for i in range(n):
            for j in range(n):
                if i!=j: 
                    visibility_graph[i].append(j)
                    exchange_graph[i].append(j)
    elif topo =='centralized':
        for i in range(1,n):
            exchange_graph[0].append(i)
            for j in range(1,n):
                if j!=i: 
                    visibility_graph[i].append(j)
    return visibility_graph, exchange_graph

###############################################################################

class Problem(object):
    ''' a fair division problem is defined by: 
        - a set of m resources
        - a set of n agents, 
        - utilities over the resources
        - an initial allocation of resources
        - a visibility topology (symmetric)
        - an exchange topology (directed)
    '''
    
    def __init__(self,n,m,culture,centralized=True):
        '''
        @n: number of agents
        @m: number of resources
        @culture: generation of utilities
        @predef_model: 
        we provide the following pre-defined MARA models: 
        - centralized: agent 0 gets all resources, 
        - complete topology, random initial allocation
        - ...
        
        '''
        
        self.n=n
        self.m=m
        self.agent = []

        # creating the resources
        resources = []
        for i in range(m):
            resources.append("r"+str(i))
            
        self.resources= resources
        
        self.centralized = centralized
        
        if centralized:
            
            # calling the function generating initial allocation
            allocation = generateAllocation(n,resources,'auctioneer')
            #print (allocation)
        
            # calling the function generating topologies
            visibility, exchange = generateTopology(n,'centralized')
            
        else: # decentrlized
            # calling the function generating initial allocation
            allocation = generateAllocation(n,resources,'random')
            #print (allocation)
        
            # calling the function generating topologies
            visibility, exchange = generateTopology(n,'complete')
            
        self.visibility_graph = visibility
        self.exchange_graph = exchange
        
        # calling the function generating the utilities
        utilities = {}
        
        
        # TODO: if centralized, enforce agent 0 gets 0 utility
        # should be ok via the topology
        for i in range(n):  # creating the agents
            utilities = generateUtilities(n,resources,culture)
            self.agent.append(Agent(utilities,[r for (r,j) in allocation.items() if j==i]))

            
            
        return
        
        
    def setUtilities(self,utilities):
        '''
        sets utilities of a problem,
        @utilities: list of dictionary
        '''
        for i in range(self.n):
            utility = utilities[i]
            self.agent[i].u= utility
        return
        
    def setAllocation(self,alloc):
        '''
        sets the allocation of a problem, 
        @alloc: a boolean array nxm specifying who gets which resource
        '''
        return
        
    def cycleReallocation(self,agents):
        '''
        @agents: list (cycle) of agents [x_1,x_2, ... xn]
        reallocate bundle by giving bundle x_2 to x_1, etc.
        '''
        items_of_first_agent = self.agent[agents[0]].hold
        self.agent[agents[0]].dropItems()
        for idx,i in enumerate(agents[:-1]): # solving the cycle
            items_of_next_agent = self.agent[agents[(idx+1)%(len(agents))]].hold
            self.agent[agents[(idx+1)%(len(agents))]].dropItems()
            self.agent[i].getItems(items_of_next_agent)
        self.agent[agents[(idx+1)%(len(agents))]].getItems(items_of_first_agent)
        return
        
    def __str__(self):
        s=""
        for i in range(self.n):
            s += "agent " + str(i) + str(self.agent[i]) + "\n"
        return s
        
    def printAllocation(self):
        s="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        for i in range(self.n):
            s += "agent " + str(i).rjust(2) + str(self.agent[i].hold).rjust(35) + "\t" + str(self.agent[i].current_u).rjust(2)+ "\n"
        return (s)
    
    
    
#TODO: create with agents and ressoures instead, then infer n/m?    
    
    
###############################################################################

#TODO: we may define at least ordinal agents, who ranks simply resources, cardinal agents who assign utilities 
#TODO: stick to the preflib representation of profiles (for ordinal profiles)
#NOTE: not really suited, as the dico representation vote : number of voters is anonymous

class Agent(object): 
    
    def __init__(self,utility,resources):
        '''
        '''
        self.u= utility # dictionary of utility for resources
        self.hold = resources # list of resources held by agent
        self.current_u = sum([self.u[r] for r in resources]) # current utility enjoyed by agent
        
    def __str__(self):
        return str(self.u)
        
    def getItem(self,r):
        '''
        @r: a single item
        '''
        self.hold.append(r)
        self.current_u += self.u[r]
        return
        
    def getItems(self,lr):
        '''
        @lr: a list of items
        '''
        for r in lr:
            self.getItem(r)
        return
        
    def giveItem(self,r):
        if r not in self.hold:
            print ("agent ", self, " does not hold ", r, "!!!")
        self.hold.remove(r)
        self.current_u -= self.u[r]
        return
        
    def giveItems(self,lr):
        for r in lr:
            self.giveItem(r)
        return
        
    def dropItems(self):
        self.hold=[]
        self.current_u = 0
        
    #TODO: replace by dropItems        
    

        
    
###############################################################################

#p1 = Problem(4,6,'empty','random','complete')
#print(p1)
#print(p1.printAllocation())
#p1.setUtilities(
#[{'r0':0,'r1':0,'r2':0,'r3':0,'r4':0,'r5':0},\
#{'r0':1,'r1':2,'r2':5,'r3':3,'r4':7,'r5':2},\
#{'r0':2,'r1':6,'r2':8,'r3':1,'r4':1,'r5':2},\
#{'r0':5,'r1':4,'r2':4,'r3':3,'r4':2,'r5':2}]
#)
#print(p1)
    