"""Equivalent direct Gurobi formulation. Requires a valid gurobipy installation/license."""
def solve_with_gurobi(data):
 import gurobipy as gp
 from gurobipy import GRB
 m=gp.Model('capacity'); F=list(data['demand']); workers=m.addVars(F,vtype=GRB.INTEGER,lb=0,name='workers'); trailers=m.addVars(F,vtype=GRB.INTEGER,lb=0,name='trailers'); unprocessed=m.addVars(F,lb=0,name='unprocessed')
 for f in F:
  m.addConstr(workers[f]<=data['max_workers'][f]); m.addConstr(trailers[f]<=data['trailers_available'][f]); m.addConstr(data['worker_capacity'][f]*workers[f]+data['trailer_capacity'][f]*trailers[f]+unprocessed[f]>=data['demand'][f])
 m.setObjective(gp.quicksum(520*workers[f]+310*trailers[f]+14*unprocessed[f] for f in F),GRB.MINIMIZE); m.optimize(); return m
