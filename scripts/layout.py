"""Lay the chain out on a plane (for display only) and compute k = excess/area per triangle."""
import math, json, sys
sys.path.insert(0,'.')
import chain
P=chain.run('printed'); R0=57020*180/math.pi; M=10**0.2898199927; RAD=math.pi/180/3600
obs={int(l.split('|')[0]):float(l.split('|')[1]) for l in open('../data/obs.txt') if l[0]!='#' and l.strip()}
side={}
for n,res in P.items():
    if not res: continue
    tr=chain.T[n]; L={st:Lg for st,Lg,_ in res}
    for i,r in enumerate(tr):
        pair=frozenset(tr[j]['st'] for j in range(3) if j!=i)
        side.setdefault(pair, R0*math.asin(10**L[r['st']]/R0)*M)
pos={}; tris=[]
def d(a,b): return side.get(frozenset((a,b)))
first=True
for n,res in P.items():
    if not res: continue
    st=[r['st'] for r in chain.T[n]]
    if first:
        a,b,c=st; pos[a]=(0.0,0.0); pos[b]=(d(a,b),0.0); first=False
    known=[s for s in st if s in pos]; new=[s for s in st if s not in pos]
    if len(known)==3: pass
    elif len(known)==2:
        a,b=known; c=new[0]; ab,ac,bc=d(a,b),d(a,c),d(b,c)
        ax,ay=pos[a]; bx,by=pos[b]; ux,uy=(bx-ax)/ab,(by-ay)/ab
        x=(ac*ac-bc*bc+ab*ab)/(2*ab); h=math.sqrt(max(ac*ac-x*x,0))
        # choose side away from centroid of previously placed points near the base
        cands=[(ax+ux*x-uy*h, ay+uy*x+ux*h),(ax+ux*x+uy*h, ay+uy*x-ux*h)]
        src=chain.SRC.get(n); opp=[r['st'] for r in chain.T[src] if r['st'] not in (a,b)] if src else []
        if opp and opp[0] in pos:
            ox,oy=pos[opp[0]]; sgn=lambda p:(bx-ax)*(p[1]-ay)-(by-ay)*(p[0]-ax)
            pos[c]=[p for p in cands if sgn(p)*sgn((ox,oy))<0][0]
        else: pos[c]=cands[0]
    else: continue
    tris.append(n)
# orient: Dunkerque at top, Montjouy at bottom
s0,s1=pos['Dunkerque'],pos['Montjouy']; ang=math.atan2(s1[1]-s0[1],s1[0]-s0[0]); rot=-math.pi/2-ang
P2={k:((x-s0[0])*math.cos(rot)-(y-s0[1])*math.sin(rot),(x-s0[0])*math.sin(rot)+(y-s0[1])*math.cos(rot)) for k,(x,y) in pos.items()}
out=[]
for n in tris:
    st=[r['st'] for r in chain.T[n]]; a=[d(st[1],st[2]),d(st[0],st[2]),d(st[0],st[1])]
    A=0.5*a[1]*a[2]*math.sin(math.radians(chain.T[n][0]['ang']/3600))
    e=obs.get(n); k=(e*RAD/A) if e is not None else None
    out.append(dict(n=n,st=st,xy=[[round(P2[s][0]/1000,3),round(P2[s][1]/1000,3)] for s in st],area_km2=round(A/1e6,2),excess=e,k=(None if k is None else float('%.4g'%(k*1e6)))))
json.dump(out,open('../data/triangles_layout.json','w'),ensure_ascii=False)
span=max(p[1] for p in P2.values())-min(p[1] for p in P2.values())
print(len(out),'triangles laid out; N-S span km',span/1000, 'Dunkerque->Montjouy km', math.hypot(s1[0]-s0[0],s1[1]-s0[1])/1000)
ks=[t['k'] for t in out if t['k'] is not None]; print(len(ks),'with k; min/max k (1/km^2)',min(ks),max(ks))
