from src.model import *
def test_build():
 x=PlanInput({'A':100},{'A':20},{'A':10},{'A':1},{'A':50}); m=build_model(x); assert len(list(m.F))==1
