from pathlib import Path
import pandas as pd, numpy as np

def generate(seed=7):
 rng=np.random.default_rng(seed); facilities=['HUB-A','HUB-B','HUB-C','HUB-D']; rows=[]
 for d in pd.date_range('2026-01-05',periods=28):
  for i,f in enumerate(facilities):
   forecast=int(52000+i*8500+9000*(d.dayofweek in [0,1])+rng.normal(0,3200)); rows.append([d.date(),f,forecast,9000+i*700,38+i*4,11+i,420+20*i])
 return pd.DataFrame(rows,columns=['date','facility','forecast_pieces','pieces_per_worker_shift','max_workers','available_trailers','trailer_capacity'])
if __name__=='__main__':
 out=Path(__file__).resolve().parents[1]/'data'; out.mkdir(exist_ok=True); generate().to_csv(out/'capacity_scenarios.csv',index=False)
