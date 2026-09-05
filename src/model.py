from dataclasses import dataclass
import pyomo.environ as pyo
@dataclass
class PlanInput:
    demand:dict; worker_capacity:dict; max_workers:dict; trailers_available:dict; trailer_capacity:dict

def build_model(x:PlanInput):
    F=list(x.demand)
    m=pyo.ConcreteModel(); m.F=pyo.Set(initialize=F)
    m.workers=pyo.Var(m.F,domain=pyo.NonNegativeIntegers); m.trailers=pyo.Var(m.F,domain=pyo.NonNegativeIntegers); m.unprocessed=pyo.Var(m.F,domain=pyo.NonNegativeReals)
    m.worker_limit=pyo.Constraint(m.F,rule=lambda m,f:m.workers[f]<=x.max_workers[f])
    m.trailer_limit=pyo.Constraint(m.F,rule=lambda m,f:m.trailers[f]<=x.trailers_available[f])
    m.cover=pyo.Constraint(m.F,rule=lambda m,f:x.worker_capacity[f]*m.workers[f]+x.trailer_capacity[f]*m.trailers[f]+m.unprocessed[f]>=x.demand[f])
    m.obj=pyo.Objective(expr=sum(520*m.workers[f]+310*m.trailers[f]+14*m.unprocessed[f] for f in m.F),sense=pyo.minimize)
    return m

def solve(x:PlanInput,solver='highs'):
    m=build_model(x); chosen={'gurobi':'gurobi','cplex':'cplex','highs':'appsi_highs'}.get(solver,solver)
    opt=pyo.SolverFactory(chosen); res=opt.solve(m)
    return [{'facility':f,'workers':round(pyo.value(m.workers[f])),'trailers':round(pyo.value(m.trailers[f])),'unprocessed':round(pyo.value(m.unprocessed[f]),1)} for f in m.F]
