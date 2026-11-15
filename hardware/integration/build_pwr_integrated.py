import json, uuid
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'hardware/pwr/RevA-integrated-draft'
OUT.mkdir(parents=True, exist_ok=True)
uid=lambda: str(uuid.uuid4())
q=lambda s: json.dumps(str(s), ensure_ascii=False)
symbols=[]; items=[]; defs={}

def define(name, pins, width=18, height=None):
    height=height or max(12, (max(len([p for p in pins if p[2]=='L']),len([p for p in pins if p[2]=='R']))+1)*2.54)
    pinout=[]
    counts={'L':0,'R':0}
    for num,pname,side,ptype in pins:
        idx=counts[side]; counts[side]+=1
        yy=height/2-2.54*(idx+1)
        xx=-width/2 if side=='L' else width/2
        angle=0 if side=='L' else 180
        pinout.append((num,pname,side,ptype,xx,yy,angle))
    body=f'(rectangle (start {-width/2} {height/2}) (end {width/2} {-height/2}) (stroke (width 0.254) (type default)) (fill (type background)))'
    parts=[]
    for num,pname,side,ptype,xx,yy,angle in pinout:
        parts.append(f'(pin {ptype} line (at {xx} {yy} {angle}) (length 0) (name {q(pname)} (effects (font (size 1.0 1.0)))) (number {q(num)} (effects (font (size 1.0 1.0)))))')
    sym=f'''(symbol "Project:{name}" (pin_names (offset 0.508)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 {height/2+2} 0) (effects (font (size 1.27 1.27))))
      (property "Value" {q(name)} (at 0 {-height/2-2} 0) (effects (font (size 1.27 1.27))))
      (symbol "{name}_1_1" {body} {' '.join(parts)}))'''
    defs[name]=(pinout,width,height)
    symbols.append(sym)

define('BQ25185', [('10','IN','L','power_in'),('2','BAT','L','passive'),('6','TS/MR','L','input'),('7','ILIM/VSET','L','input'),('8','ISET','L','input'),('4','CE','L','input'),('5','GND','L','power_in'),('11','EP','L','power_in'),('1','SYS','R','power_out'),('9','STAT1','R','open_collector'),('3','STAT2','R','open_collector')],35.56,25.4)
define('TPS61023',[('3','VIN','L','power_in'),('2','EN','L','input'),('4','GND','L','power_in'),('1','FB','L','input'),('5','SW','R','passive'),('6','VOUT','R','power_out')],30.48,20.32)
define('USB4105',[
 ('A1','GND','R','power_out'),('A4','VBUS','R','power_out'),('A5','CC1','R','passive'),
 ('A6','D+','R','passive'),('A7','D-','R','passive'),('A8','SBU1','R','passive'),
 ('A9','VBUS','R','passive'),('A12','GND','R','passive'),('B1','GND','R','passive'),
 ('B4','VBUS','R','passive'),('B5','CC2','R','passive'),('B6','D+','R','passive'),
 ('B7','D-','R','passive'),('B8','SBU2','R','passive'),('B9','VBUS','R','passive'),
 ('B12','GND','R','passive'),('SH','SHIELD','R','passive')],27.94,48.26)
define('PASSIVE',[('1','1','L','passive'),('2','2','R','passive')],10.16,10.16)
define('TPS259533',[('3','IN','L','power_in'),('4','IN','L','power_in'),('2','EN/OVLO','L','input'),('7','ILM','L','input'),('1','dVdt','L','input'),('8','GND','L','power_in'),('9','EP','L','power_in'),('5','OUT','R','power_out'),('6','FLT','R','open_collector')],33.02,22.86)
define('TPD2E2U06DCK',[('1','IO1','L','passive'),('2','IO2','L','passive'),('3','GND','L','power_in')],22.86,12.7)
define('TVS_BI',[('1','IO','L','passive'),('2','IO','R','passive')],15.24,10.16)
define('PMOS_BSS84AK',[('2','S','L','passive'),('1','G','L','input'),('3','D','R','passive')],17.78,12.7)
define('NMOS_2N7002',[('1','G','L','input'),('2','S','L','passive'),('3','D','R','passive')],17.78,12.7)
define('CONN_1x2',[('1','1','L','passive'),('2','2','L','passive')],17.78,10.16)
define('CONN_1x3',[(str(i),str(i),'L','passive') for i in range(1,4)],17.78,15.24)
define('CONN_1x4',[(str(i),str(i),'L','passive') for i in range(1,5)],17.78,17.78)
define('CONN_1x5',[(str(i),str(i),'L','passive') for i in range(1,6)],17.78,20.32)
define('CONN_1x9',[(str(i),str(i),'L','passive') for i in range(1,10)],17.78,30.48)
define('CONN_1x10',[(str(i),str(i),'L','passive') for i in range(1,11)],17.78,33.02)

root=uid()
def place(kind,ref,value,x,y,nets,footprint='',datasheet=''):
    x=round(x/1.27)*1.27; y=round(y/1.27)*1.27
    pins,w,h=defs[kind]; su=uid()
    props=f'''(property "Reference" {q(ref)} (at {x} {y-h/2-3} 0) (effects (font (size 1.27 1.27))))
    (property "Value" {q(value)} (at {x} {y+h/2+3} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" {q(footprint)} (at {x} {y} 0) (effects (font (size 1.0 1.0)) (hide yes)))
    (property "Datasheet" {q(datasheet)} (at {x} {y} 0) (effects (font (size 1.0 1.0)) (hide yes)))'''
    pinids=' '.join(f'(pin {q(num)} (uuid {q(uid())}))' for num,*_ in pins)
    items.append(f'''(symbol (lib_id "Project:{kind}") (at {x} {y} 0) (unit 1) (in_bom {'no' if ref=='RT1' else 'yes'}) (on_board {'no' if ref=='RT1' else 'yes'}) (dnp {'yes' if ref=='JP1' else 'no'}) (uuid {q(su)}) {props} {pinids}
      (instances (project "PWR_RevA" (path {q('/'+root)} (reference {q(ref)}) (unit 1)))))''')
    for num,pname,side,ptype,px,py,a in pins:
        net=nets.get(num)
        if net:
            lx,ly=round(x+px,4),round(y-py,4)
            items.append(f'(label {q(net)} (at {lx} {ly} 0) (effects (font (size 0.9 0.9)) (justify left bottom)) (uuid {q(uid())}))')
        else:
            lx,ly=round(x+px,4),round(y-py,4)
            items.append(f'(no_connect (at {lx} {ly}) (uuid {q(uid())}))')

def passive(ref,value,x,y,a,b,footprint=''):
    place('PASSIVE',ref,value,x,y,{'1':a,'2':b},footprint)

place('USB4105','J4','GCT USB4105-GF-A',40,70,{
 'A1':'GND','A4':'USB_VBUS_RAW','A5':'CC1','A9':'USB_VBUS_RAW','A12':'GND',
 'B1':'GND','B4':'USB_VBUS_RAW','B5':'CC2','B9':'USB_VBUS_RAW','B12':'GND','SH':'GND'},
 'Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal','https://gct.co/files/drawings/usb4105.pdf')
passive('R6','5.1k 1% CC1 Rd',92,44,'CC1','GND')
passive('R7','5.1k 1% CC2 Rd',92,59,'CC2','GND')
place('TPD2E2U06DCK','U4','CC ESD TPD2E2U06DCK',96,82,{'1':'CC1','2':'CC2','3':'GND'},
 'Package_TO_SOT_SMD:SOT-323_SC-70','https://www.ti.com/lit/ds/symlink/tpd2e2u06.pdf')
place('TVS_BI','D1','VBUS TVS TPD1E10B06DPY',93,108,{'1':'USB_VBUS_RAW','2':'GND'},
 'Package_SON:Texas_DPY0002A_0.6x1mm_P0.65mm','https://www.ti.com/lit/ds/symlink/tpd1e10b06.pdf')
place('TPS259533','U3','TPS259533DSGR',169,75,{
 '3':'USB_VBUS_RAW','4':'USB_VBUS_RAW','2':'EFUSE_OVLO','7':'EFUSE_ILM',
 '1':'EFUSE_DVDT','8':'GND','9':'GND','5':'USB_VBUS_PROTECTED'},
 'Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm','https://www.ti.com/lit/ds/symlink/tps2595.pdf')
passive('R16','442k 1% OVLO top',135,111,'USB_VBUS_RAW','EFUSE_OVLO')
passive('R17','100k 1% OVLO bottom',158,111,'EFUSE_OVLO','GND')
passive('R18','1.78k 1% ILM',181,111,'EFUSE_ILM','GND')
passive('C7','3.3nF dVdt',204,111,'EFUSE_DVDT','GND')
passive('C8','0.1uF input bypass',227,111,'USB_VBUS_RAW','GND')
passive('C9','1uF protected input',250,111,'USB_VBUS_PROTECTED','GND')
place('BQ25185','U1','BQ25185',290,75,{'10':'USB_VBUS_PROTECTED','2':'CELL_BAT','6':'CELL_NTC','7':'ILIM_SET','8':'ISET_SET','4':'GND','5':'GND','11':'GND','1':'SYS_BUS','9':'CHG_STAT1','3':'CHG_STAT2'},
 'Package_DFN_QFN:Texas_DLH0010A_WSON-10-1EP_2.2x2mm_P0.4mm_EP0.9x1.5mm','https://www.ti.com/lit/ds/symlink/bq25185.pdf')
passive('C1','1uF min effective; 25V candidate',110,145,'USB_VBUS_PROTECTED','GND')
passive('C2','10uF nominal; >=1uF effective',133,145,'SYS_BUS','GND')
passive('C3','1uF min effective',156,145,'CELL_BAT','GND')
passive('R1','18k 1%',181,145,'ILIM_SET','GND')
passive('R2','1.2k 1% / 250mA target',209,145,'ISET_SET','GND')
passive('RT1','EXTERNAL cell NTC 10k B3435 provisional',242,145,'CELL_NTC','GND')
place('CONN_1x3','J5','3-wire protected cell + in-pack NTC',40,155,{'1':'CELL_BAT','2':'GND','3':'CELL_NTC'})
place('TPS61023','U2','TPS61023',169,190,{'3':'SYS_BUS','2':'PWR_5V_EN','4':'GND','1':'BOOST_FB','5':'BOOST_SW','6':'+5V_PWR'},
 'Package_TO_SOT_SMD:SOT-563','https://www.ti.com/lit/ds/symlink/tps61023.pdf')
passive('L1','1uH; Isat/Irms TODO',73,190,'SYS_BUS','BOOST_SW')
passive('C4','10uF nominal; effective >=1uF',101,190,'SYS_BUS','GND')
passive('C5','22uF nominal',226,179,'+5V_PWR','GND')
passive('C6','22uF nominal',252,179,'+5V_PWR','GND')
passive('R3','732k 1%',226,199,'+5V_PWR','BOOST_FB')
passive('R4','100k 1%',252,199,'BOOST_FB','GND')
passive('R5','100k candidate; EN default LOW',280,199,'PWR_5V_EN','GND')
place('CONN_1x4','J1','PWR-HV pin order provisional',47,231,{'1':'+5V_PWR','2':'GND','3':'HV_EN_REQ','4':'HV_FAULT_N'})
place('CONN_1x5','J2','PWR-CTRL power provisional',125,231,{'1':'SYS_BUS','2':'SYS_BUS','3':'+5V_PWR','4':'GND','5':'GND'})
place('CONN_1x10','J3','PWR-CTRL signal provisional',237,231,{
 '1':'CHG_STAT1','2':'CHG_STAT2','3':'ADC_BAT','4':'ADC_SYS','5':'ADC_5V',
 '6':'PWR_5V_EN','7':'HV_EN_REQ','8':'HV_FAULT_N','9':'GND','10':'ADC_SENSE_EN'})

for x,pm,nm,idx,src,sense,adc,top,bot,cap,pull in [
 (58,'Q1','Q4',1,'CELL_BAT','SENSE_BAT','ADC_BAT','R10','R11','C10','R21'),
 (171,'Q2','Q5',2,'SYS_BUS','SENSE_SYS','ADC_SYS','R12','R13','C11','R22'),
 (284,'Q3','Q6',3,'+5V_PWR','SENSE_5V','ADC_5V','R14','R15','C12','R23')]:
    gate='ADC_GATE_'+str(idx)
    place('PMOS_BSS84AK',pm,'BSS84AK',x,282,{'2':src,'1':gate,'3':sense},
          'Package_TO_SOT_SMD:SOT-23','https://assets.nexperia.com/documents/data-sheet/BSS84AK.pdf')
    place('NMOS_2N7002',nm,'2N7002',x,307,{'1':'ADC_SENSE_EN','2':'GND','3':gate},
          'Package_TO_SOT_SMD:SOT-23','https://assets.nexperia.com/documents/data-sheet/2N7002.pdf')
    passive(pull,'1M PMOS gate pull-up',x+29,282,src,gate)
    passive(top,'100k 1% ADC upper',x-14,333,sense,adc)
    passive(bot,'47k 1% ADC lower',x+12,333,adc,'GND')
    passive(cap,'1nF ADC filter',x+37,333,adc,'GND')
passive('R24','100k ADC_EN default LOW',330,307,'ADC_SENSE_EN','GND')

notes=[
 'Rev.A integrated PWR DRAFT - NOT PCB / ORDER READY. Original v3 preserved.',
 'BQ25185 CE=GND: USB present causes automatic charging independent of MCU; battery absent behavior requires test.',
 'J4=GCT USB4105; CC1/CC2 each 5.1k Rd; D+/D-/SBU unused. J4 shield ties to GND; EMI review pending.',
 'U3=eFuse current limit is NOT USB source-current detection; USB source policy remains a blocker.',
 'J1/J2/J3 pin numbers are DRAFT ONLY. J3 adds ADC_SENSE_EN (GP17 candidate).',
 'J5 pin3 is cell-mounted NTC; RT1 is OFF-BOARD representation only. Cell MPN/polarity TODO.',
 'ADC PMOS switches default OFF. Wait >=1ms after EN and >=0.3ms after mux change; leakage test.',
 'No HV generation on this PCB. HV board must independently implement OVP, discharge and fail-safe EN.',
 'Cell pack protection, NTC placement, thermal and connector current ratings are unresolved.'
]
for i,n in enumerate(notes):
    items.append(f'(text {q(n)} (at 24 {390+i*4} 0) (effects (font (size 1.1 1.1)) (justify left)) (uuid {q(uid())}))')

sch=f'''(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(root)}) (paper "A2")
 (title_block (title "PROJECT-NIXIDORO PWR Rev.A integrated draft") (rev "INTEGRATION DRAFT") (date "2026-11-15"))
 (lib_symbols {' '.join(symbols)})
 {' '.join(items)}
 (embedded_fonts no))'''
(OUT/'PWR_RevA.kicad_sch').write_text(sch,encoding='utf-8')
(OUT/'PWR_RevA.kicad_pro').write_text('{}\n',encoding='utf-8')
lib='(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor") '+ ' '.join(s.replace('Project:','') for s in symbols)+')'
(OUT/'Project.kicad_sym').write_text(lib,encoding='utf-8')
(OUT/'sym-lib-table').write_text('(sym_lib_table (lib (name "Project") (type "KiCad") (uri "${KIPRJMOD}/Project.kicad_sym") (options "") (descr "Project draft symbols")))\n',encoding='utf-8')
print(OUT/'PWR_RevA.kicad_sch')
