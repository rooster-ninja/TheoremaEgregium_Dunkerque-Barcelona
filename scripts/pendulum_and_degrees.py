"""Flattening from Tome IV pendulum lengths (pp. 573-575) and Tome III degree lengths (p. 548), raw printed values."""
import math
def fit(x,y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    b=sum((a-mx)*(c-my) for a,c in zip(x,y))/sum((a-mx)**2 for a in x); a0=my-b*mx
    s=math.sqrt(sum((c-a0-b*a)**2 for a,c in zip(x,y))/(n-2)); return a0,b,s/math.sqrt(sum((a-mx)**2 for a in x))
dms=lambda d,m,s:d+m/60+s/3600
pend=[(dms(60,45,25),742.723136),(dms(55,58,37),742.413435),(dms(51,2,10),742.077030),(dms(48,50,14),741.917490),
      (dms(45,46,48),741.705180),(dms(44,50,26),741.608720),(dms(44,36,45),741.612280),(dms(38,39,56),741.252000)]
A,B,sB=fit([math.sin(math.radians(a))**2 for a,_ in pend],[l for _,l in pend])
f=0.00865-B/A; print('Pendulum: A=%.4f mm B=%.4f+-%.4f mm  flattening 1/%.0f (1-sigma 1/%.0f to 1/%.0f)'%(A,B,sB,1/f,1/(f+sB/A),1/(f-sB/A)))
deg=[(dms(51,15,25),57097.22),(dms(49,56,29),57087.66),(dms(47,30,46),57069.31),(dms(44,41,48),56977.80),(dms(42,17,20),56946.68),(dms(40,0,50),56999.84)]
a0,b,sb=fit([math.cos(2*math.radians(a)) for a,_ in deg],[m for _,m in deg])
f=-b/(1.5*a0); sf=sb/(1.5*a0)
print('Degrees: mean degree %.1f t, mean R %.0f km, flattening 1/%.0f (1-sigma 1/%.0f to 1/%.0f)'%(a0,a0*180/math.pi*1.949036592/1e3,1/f,1/(f+sf),1/(f-sf)))
