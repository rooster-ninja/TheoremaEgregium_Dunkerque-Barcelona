import sys,math; sys.path.insert(0,'.')
import chain
P=chain.run('printed'); R0=57020*180/math.pi; M=10**0.2898199927; RAD=math.pi/180/3600
obs={}
for l in open('../data/obs.txt'):
    if l[0]=='#' or not l.strip(): continue
    n,e,err=l.split('|'); obs[int(n)]=(float(e),float(err))
rows=[]; bad=[]
for n,(e,err) in sorted(obs.items()):
    tr=chain.T[n]; exc=sum(r['exc'] for r in tr)
    if abs(e-exc-err)>0.02: bad.append((n,e,exc,err))
    L={st:Lg for st,Lg,_ in P[n]}
    a=[R0*math.asin(10**L[r['st']]/R0)*M for r in tr]
    A=0.5*a[1]*a[2]*math.sin(math.radians(tr[0]['ang']/3600))
    rows.append((n,A,e*RAD))
print('consistency issues',bad)
def fit(rows):
    K=sum(A*e for _,A,e in rows)/sum(A*A for _,A,e in rows)
    s=math.sqrt(sum((e-K*A)**2 for _,A,e in rows)/(len(rows)-1)); sK=s/math.sqrt(sum(A*A for _,A,e in rows))
    return K,sK,s
K,sK,s=fit(rows); R=1/math.sqrt(K)
print(len(rows),'triangles, total area %.0f km2, mean %.0f km2'%(sum(r[1] for r in rows)/1e6,sum(r[1] for r in rows)/len(rows)/1e6))
print('R = %.0f km  (1-sigma %.0f-%.0f km)'%(R/1e3,1/math.sqrt(K+sK)/1e3,1/math.sqrt(K-sK)/1e3))
print('closure scatter %.2f arcsec'%(s/RAD))
print('mean obs excess %.2f, expected@6371 %.2f'%(sum(e for *_,e in rows)/len(rows)/RAD, sum(A for _,A,_ in rows)/len(rows)/6371e3**2/RAD))
# robust: drop |resid|>3 sigma
r2=[r for r in rows if abs(r[2]-K*r[1])<3*s]; K2,sK2,s2=fit(r2); print('3-sigma clip',len(r2),'R=%.0f km'%(1/math.sqrt(K2)/1e3))
# north vs south halves
for lab,sel in (('north 1-43',lambda n:n<=43),('centre 44-89',lambda n:44<=n<=89),('south 90-115',lambda n:n>=90)):
    rr=[r for r in rows if sel(r[0])]; k,sk,_=fit(rr); print(lab,len(rr),'R=%.0f km +- %.0f'%(1/math.sqrt(k)/1e3, 1/math.sqrt(k)*sk/(2*k)/1e3))
# two-parameter fit: excess = bias + A/R^2  (bias = systematic error per triangle)
n=len(rows); Sx=sum(A for _,A,_ in rows); Sy=sum(e for *_,e in rows); Sxx=sum(A*A for _,A,_ in rows); Sxy=sum(A*e for _,A,e in rows)
d=n*Sxx-Sx*Sx; k=(n*Sxy-Sx*Sy)/d; b=(Sy-k*Sx)/n
res=[e-b-k*A for _,A,e in rows]; s=math.sqrt(sum(x*x for x in res)/(n-2)); sk=s*math.sqrt(n/d)
print('with bias term: bias %.2f arcsec/triangle, R = %.0f km (1-sigma %.0f-%.0f)'%(b/RAD,1/math.sqrt(k)/1e3,1/math.sqrt(k+sk)/1e3,1/math.sqrt(max(k-sk,1e-30))/1e3))
print('area range km2',min(A for _,A,_ in rows)/1e6,max(A for _,A,_ in rows)/1e6)
