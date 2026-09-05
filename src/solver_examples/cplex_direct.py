"""Equivalent DOcplex formulation. Requires docplex + a CPLEX runtime/license."""
def solve_with_cplex(data):
 from docplex.mp.model import Model
 m=Model('capacity'); F=list(data['demand']); workers=m.integer_var_dict(F,lb=0,name='workers'); trailers=m.integer_var_dict(F,lb=0,name='trailers'); unprocessed=m.continuous_var_dict(F,lb=0,name='unprocessed')
 for f in F:
  m.add_constraint(workers[f]<=data['max_workers'][f]); m.add_constraint(trailers[f]<=data['trailers_available'][f]); m.add_constraint(data['worker_capacity'][f]*workers[f]+data['trailer_capacity'][f]*trailers[f]+unprocessed[f]>=data['demand'][f])
 m.minimize(m.sum(520*workers[f]+310*trailers[f]+14*unprocessed[f] for f in F)); return m.solve(log_output=True)
