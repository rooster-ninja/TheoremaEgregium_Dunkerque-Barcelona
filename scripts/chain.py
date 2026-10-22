import math, collections, json
LN10 = math.log(10)
def load():
    T = collections.OrderedDict()
    for line in open('../data/tab.txt', encoding='utf-8'):
        line=line.strip()
        if not line or line.startswith('#'): continue
        f=line.split('|'); n=int(f[0])
        d,m,s=f[2].split()
        T.setdefault(n,[]).append(dict(st=f[1], ang=int(d)*3600+int(m)*60+float(s), exc=float(f[3]),
            ls=None if f[4]=='-' else float(f[4]), L=None if f[5]=='-' else float(f[5]),
            arc=None if f[6]=='-' else float(f[6])))
    return T
T = load()
# known misprints where the value Delambre actually used is recoverable
CORR={(61,'Sainte-Montaine'):9.9385400957}
for n,tr in T.items():
    for r in tr:
        if (n,r['st']) in CORR: r['ls_printed']=r['ls']; r['ls']=CORR[(n,r['st'])]

# Tome I (commission) angles differ from Tome II for chain triangles 44-100.
# 44-95: angle opposite the base -0.10", the other two +0.05" (Tome II = Tome I + delta)  [verified 44,52,53,93,94,95]
# 96-100: read directly from Tome I pp. 537-538 (delta = TII - TI)
EXPLICIT = {96:{'Montredon':0,'Saint-Pons':+0.05,'Nore':-0.05},
            97:{'Saint-Pons':+0.05,'Nore':-0.05,'Alaric':0},
            98:{'Nore':0,'Alaric':+0.01,'Carcassonne':-0.01},
            99:{'Alaric':-0.01,'Carcassonne':+0.01,'Bugarach':0},
            100:{'Alaric':+0.01,'Bugarach':0,'Tauch':-0.01}}
NOT_MODIFIED = {45,46,50,51,59,60,63,67,68}   # side / 'inutile' triangles, not on the chain

def base_index(tr):
    idx=[i for i,r in enumerate(tr) if r['L'] is None]
    return idx[0] if len(idx)==1 else None

def deltas(n,tr):
    """Tome II minus Tome I, arcseconds, per station"""
    if n in EXPLICIT: return [EXPLICIT[n][r['st']] for r in tr]
    if 44<=n<=95 and n not in NOT_MODIFIED:
        b=base_index(tr); return [-0.10 if i==b else +0.05 for i in range(3)]
    return [0,0,0]

SRC={}
def run(mode, start=1):
    """mode: 'printed' = Delambre's printed log-sines of the angles (Tome II);
             'angles'  = log-sines recomputed from the printed Tome II angles;
             'tome1'   = printed log-sines shifted to the original Tome I angles."""
    sides={}   # frozenset pair -> (logsin, triangle)
    out=collections.OrderedDict()
    for n,tr in T.items():
        if any(r['ls'] is None for r in tr): continue
        if mode=='printed': ls=[r['ls'] for r in tr]
        elif mode=='angles': ls=[10+math.log10(math.sin(math.radians(r['ang']/3600))) for r in tr]
        else:
            dl=deltas(n,tr)
            ls=[r['ls'] - math.cos(math.radians(r['ang']/3600))/math.sin(math.radians(r['ang']/3600))*math.radians(d/3600)/LN10 for r,d in zip(tr,dl)]
        b=base_index(tr)
        pair=lambda i: frozenset(tr[j]['st'] for j in range(3) if j!=i)
        if b is None:   # triangle 1: seed with Delambre's printed sides
            for i in range(3): sides.setdefault(pair(i),[]).append((tr[i]['L'],n))
            out[n]=[(tr[i]['st'],tr[i]['L'],'seed') for i in range(3)]; continue
        if pair(b) not in sides: out[n]=None; continue
        cands=sides[pair(b)]
        if mode=='printed':
            g=[i for i in range(3) if i!=b and tr[i]['L'] is not None][0]
            implied=tr[g]['L']-tr[g]['ls']+tr[b]['ls']
            Lb,src=min(cands,key=lambda c:abs(c[0]-implied)); SRC[n]=src
        else:
            Lb,src=[c for c in cands if c[1]==SRC[n]][0]
        res=[]
        for i in range(3):
            if i==b: res.append((tr[i]['st'],Lb,f'base from {src}')); continue
            Li=Lb+ls[i]-ls[b]
            sides.setdefault(pair(i),[]).append((Li,n)); res.append((tr[i]['st'],Li,''))
        out[n]=res
    return out

if __name__=='__main__':
    P=run('printed'); A=run('angles'); O=run('tome1')
    # reproduction check vs printed sides
    worst=[]
    for n,tr in T.items():
        if not P.get(n): continue
        for (st,L,_),r in zip(P[n],tr):
            if r['L'] is not None: worst.append((abs(L-r['L'])*1e10, n, st))
    worst.sort(reverse=True); print('largest reproduction diffs (1e-10 log units):',[(round(a),n,s) for a,n,s in worst[:8]])
    def vs(R): return [L for st,L,_ in R[104] if st=='Espira'][0]
    def melun(R): return [L for st,L,_ in R[43] if st=='Malvoisine'][0]
    for name,R in (('printed',P),('angles',A),('tome1',O)):
        print(name,'Lieursaint-Melun',round(melun(R),10),'Vernet-Salces',round(vs(R),10))
