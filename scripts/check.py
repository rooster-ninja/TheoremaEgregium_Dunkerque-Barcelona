import math, sys, collections
R = 57020*180/math.pi   # Delambre: mean degree 57020 toises
M = 1.949036591          # metres per toise (provisional; refined from data)
rows = collections.OrderedDict()
for line in open('../data/tab.txt', encoding='utf-8'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    f=line.split('|')
    n=int(f[0]); rows.setdefault(n,[]).append(f)
def num(s): return None if s in ('-','') else float(s)
sides = {}   # frozenset(pair) -> list of (n, logsin)
bad=[]
ratios=[]
for n,tr in rows.items():
    if len(tr)!=3: bad.append((n,'rows',len(tr))); continue
    st=[t[1] for t in tr]
    ang=[];
    for t in tr:
        d,m,s=t[2].split(); ang.append(int(d)*3600+int(m)*60+float(s))
    exc=[float(t[3]) for t in tr]
    tot=sum(ang)-180*3600
    if abs(tot-sum(exc))>0.015: bad.append((n,'anglesum',round(tot,3),round(sum(exc),3)))
    la=[num(t[4]) for t in tr]
    if None in la:
        continue
    ls=[num(t[5]) for t in tr]
    # log sin angle check vs computed
    for i in range(3):
        c=10+math.log10(math.sin(math.radians(ang[i]/3600)))
        if abs(c-la[i])>3e-9: bad.append((n,st[i],'logsinA',la[i],round(c,10)))
    ks=[ls[i]-la[i] for i in range(3) if ls[i] is not None]
    if len(ks)>=2 and max(ks)-min(ks)>3e-9: bad.append((n,'sinerule',[round(k,10) for k in ks]))
    k=ks[0] if ks else None
    for i in range(3):
        pair=frozenset([st[j] for j in range(3) if j!=i])
        if ls[i] is None:
            if k is None: continue
            # base side: implied logsin
            imp=k+la[i]
            prev=sides.get(pair)
            if not prev: bad.append((n,'base-notfound',sorted(pair),round(imp,10)))
            else:
                diffs=[(pn,round((imp-pl)*1e10)) for pn,pl in prev]
                if min(abs(d) for _,d in diffs)>4: bad.append((n,'base-mismatch',sorted(pair),diffs))
        else:
            sides.setdefault(pair,[]).append((n,ls[i]))
            arc=num(tr[i][6]); met=num(tr[i][7])
            if arc:
                S=10**ls[i]; a=R*math.asin(S/R)
                if abs(a-arc)>0.0015: bad.append((n,st[i],'arc',arc,round(a,4)))
                if met: ratios.append((met/arc,n,st[i]))
if ratios:
    rs=sorted(r for r,_,_ in ratios); med=rs[len(rs)//2]
    print('metre/toise median',med)
    for r,n,s in ratios:
        if abs(r-med)*20000>0.03: bad.append((n,s,'metres',round((r-med)*1e9)))
print('triangles',len(rows))
for b in bad: print(b)
