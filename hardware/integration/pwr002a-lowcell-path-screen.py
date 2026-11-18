"""PWR-002A low-cell power-path sensitivity, NOT hardware qualification."""
from math import sqrt
P_SYS=6.60084 # W, assumed integrated 205V/16mA, etaHV=.70, eta5=.85 and other loads
R_BQ=0.14 # ohm, BQ25185 BATFET max under SPECIFIED test conditions, extrapolated
for vb in (4.0,3.6,3.3,3.0):
 for r_external in (0,0.1,0.2):
  r=R_BQ+r_external
  disc=vb*vb-4*r*P_SYS
  if disc<0:
   print(vb,r_external,"NO REAL STEADY STATE (constant-power model)")
   continue
  i=(vb-sqrt(disc))/(2*r)
  sys=vb-r*i
  print(f"VBAT={vb:.1f} Rext={r_external:.2f} I={i:.3f} VSYS={sys:.3f} PBQ={i*i*R_BQ:.3f} Pext={i*i*r_external:.3f} OCPmin27C_margin={2.5666-i:.3f}")
