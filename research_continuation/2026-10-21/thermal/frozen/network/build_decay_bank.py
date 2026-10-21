"""Generate a decay/inverse-absorption conductance bank on scattering eta nodes."""
import argparse
import json
from pathlib import Path
import numpy as np
from decay_graph import decay_conductance

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-bank',type=Path,default=HERE.parent/'solver'/'bank_q40.npz')
    parser.add_argument('--output',type=Path,default=HERE/'decay_bank.npz')
    parser.add_argument('--parent-order',type=int,default=8)
    parser.add_argument('--spectral-order',type=int,default=64)
    parser.add_argument('--tail-order',type=int,default=64)
    args=parser.parse_args()
    data=np.load(args.source_bank)
    edges=data['edges']; eta=data['eta']
    matrices=[];metadata=[]
    for value in eta:
        T=.5*np.exp(-float(value))
        W,meta=decay_conductance(T,edges,parent_order=args.parent_order,
                               spectral_order=args.spectral_order,tail_order=args.tail_order)
        matrices.append(W); metadata.append(meta)
        print('T',T,'event relative error',meta['thermal_event_relative_difference'],flush=True)
    np.savez_compressed(args.output,edges=edges,eta=eta,conductances=np.array(matrices),
                        conductance_units=np.array('GeV; normalized by N_eq(T); not divided by H'))
    args.output.with_suffix('.json').write_text(json.dumps(dict(
        conductance_units='GeV; normalized by N_eq(T); not divided by H',
        source_scattering_bank=args.source_bank.name,eta=eta.tolist(),metadata=metadata),indent=2)+'\n')

if __name__=='__main__':main()
