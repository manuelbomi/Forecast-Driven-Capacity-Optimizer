from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.model import PlanInput,solve
app=FastAPI(title='Forecast Driven Capacity Optimizer')
class Req(BaseModel): date:str='2026-01-05'; solver:str='highs'; demand_multiplier:float=1.0
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/optimize')
def optimize(q:Req):
 d=pd.read_csv('data/capacity_scenarios.csv'); d=d[d.date==q.date]
 x=PlanInput(demand={r.facility:int(r.forecast_pieces*q.demand_multiplier) for _,r in d.iterrows()},worker_capacity={r.facility:r.pieces_per_worker_shift for _,r in d.iterrows()},max_workers={r.facility:r.max_workers for _,r in d.iterrows()},trailers_available={r.facility:r.available_trailers for _,r in d.iterrows()},trailer_capacity={r.facility:r.trailer_capacity for _,r in d.iterrows()}); return {'solver':q.solver,'plan':solve(x,q.solver)}
