"""Assert board connector and critical device pins in KiCad-exported netlists."""
import re
from pathlib import Path

root=Path(__file__).resolve().parents[2]
paths={
    'PWR':root/'hardware/pwr/RevA-integrated-draft/PWR_RevA.net',
    'HV':root/'hardware/hv/RevA-draft/HV_RevA.net',
    'CTRL':root/'hardware/ctrl/RevA-draft/CTRL_RevA.net',
}

def nets(path):
    text=path.read_text(encoding='utf-8')
    result={}
    for block in re.split(r'\n\t\t\(net\s*',text)[1:]:
        m=re.search(r'\(name "([^"]+)"\)',block)
        if not m: continue
        name=m.group(1).lstrip('/')
        nodes=re.findall(r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)',block)
        result[name]=set(nodes)
    return result

allnets={k:nets(p) for k,p in paths.items()}
def net_of(board, ref, pin):
    hit=[name for name,nodes in allnets[board].items() if (ref,str(pin)) in nodes]
    if len(hit)!=1: raise SystemExit(f'{board} {ref} pin {pin}: expected one net, found {hit}')
    return hit[0]

signal=['CHG_STAT1','CHG_STAT2','ADC_BAT','ADC_SYS','ADC_5V',
        'PWR_5V_EN','HV_EN_REQ','HV_FAULT_N','GND','ADC_SENSE_EN']
for pin,name in enumerate(signal,1):
    for board in ('PWR','CTRL'):
        actual=net_of(board,'J3',pin)
        if actual!=name: raise SystemExit(f'{board} J3 pin {pin}: {actual} != {name}')
assert net_of('CTRL','U1',22)=='ADC_SENSE_EN'
assert net_of('PWR','J5',3)=='CELL_NTC'
assert net_of('PWR','U1',6)=='CELL_NTC'
assert net_of('PWR','J1',3)==net_of('HV','J1',3)=='HV_EN_REQ'
assert net_of('PWR','J1',4)==net_of('HV','J1',4)=='HV_FAULT_N'
assert net_of('PWR','J1',1)=='+5V_PWR'
assert net_of('HV','J1',1)=='+5V_HV'
for ch in range(1,33):
    pin=34+ch if ch<=10 else ch-10
    expect=(f'TUBE_A_K{ch-1}' if ch<=10 else
            f'TUBE_B_K{ch-11}' if ch<=20 else f'NEON_{ch-20:02d}_K')
    if net_of('CTRL','U3',pin)!=expect:
        raise SystemExit(f'HV5524 channel {ch} pin {pin} mismatch')
assert net_of('CTRL','U3',27)=='+5V_LOGIC'  # POL high
assert net_of('CTRL','U3',33)=='HV_BL_5V'
assert net_of('CTRL','U3',45)=='GND'
assert net_of('HV','U1',10)=='HV_RUN_TODO'
assert net_of('HV','J1',3)!='HV_RUN_TODO'  # deliberate inhibit until safety gate exists
print('PASS: J3 10 pins; PWR J5 NTC; J1 control; Pico GP17; HV5524 32 channels and inhibit')
