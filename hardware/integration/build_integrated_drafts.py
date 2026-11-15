"""Build intentionally incomplete Rev.A HV and CTRL KiCad schematic drafts.

Only manufacturer-verified pins are numbered. Missing power-stage and lamp
mechanical data remain explicit nets and TODOs, never fabricated parts.
"""
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
q = lambda s: json.dumps(str(s), ensure_ascii=False)
uid = lambda: str(uuid.uuid4())

class Draft:
    def __init__(self, name, title):
        self.name, self.title = name, title
        self.root = uid()
        self.defs, self.symbols, self.items = {}, [], []

    def define(self, name, pins, width=25.4, height=None):
        counts = {'L': 0, 'R': 0}
        if height is None:
            height = (max(sum(p[2]=='L' for p in pins), sum(p[2]=='R' for p in pins))+2)*2.54
        pinout=[]
        for num,pname,side,ptype in pins:
            i=counts[side]; counts[side]+=1
            xx=-width/2 if side=='L' else width/2
            yy=height/2-2.54*(i+1)
            pinout.append((num,pname,side,ptype,xx,yy,0 if side=='L' else 180))
        body=f'(rectangle (start {-width/2} {height/2}) (end {width/2} {-height/2}) (stroke (width 0.254) (type default)) (fill (type background)))'
        pinexpr=' '.join(f'(pin {typ} line (at {x} {y} {a}) (length 0) (name {q(pname)} (effects (font (size 0.9 0.9)))) (number {q(num)} (effects (font (size 0.9 0.9)))))' for num,pname,side,typ,x,y,a in pinout)
        self.symbols.append(f'(symbol "Project:{name}" (pin_names (offset 0.508)) (in_bom yes) (on_board yes) (property "Reference" "U" (at 0 {height/2+2} 0) (effects (font (size 1.27 1.27)))) (property "Value" {q(name)} (at 0 {-height/2-2} 0) (effects (font (size 1.27 1.27)))) (symbol "{name}_1_1" {body} {pinexpr}))')
        self.defs[name]=(pinout,width,height)

    def place(self, kind, ref, value, x, y, nets, footprint='', datasheet=''):
        x=round(x/1.27)*1.27; y=round(y/1.27)*1.27
        pins,w,h=self.defs[kind]
        props=f'(property "Reference" {q(ref)} (at {x} {y-h/2-3} 0) (effects (font (size 1.1 1.1)))) (property "Value" {q(value)} (at {x} {y+h/2+3} 0) (effects (font (size 1.0 1.0)))) (property "Footprint" {q(footprint)} (at {x} {y} 0) (effects (font (size 1 1)) (hide yes))) (property "Datasheet" {q(datasheet)} (at {x} {y} 0) (effects (font (size 1 1)) (hide yes)))'
        pinids=' '.join(f'(pin {q(num)} (uuid {q(uid())}))' for num,*_ in pins)
        virtual = kind in ('SUPPLY_MARK', 'DISPLAY_PATH')
        assembly = 'no' if virtual else 'yes'
        self.items.append(f'(symbol (lib_id "Project:{kind}") (at {x} {y} 0) (unit 1) (in_bom {assembly}) (on_board {assembly}) (dnp no) (uuid {q(uid())}) {props} {pinids} (instances (project {q(self.name)} (path {q("/"+self.root)} (reference {q(ref)}) (unit 1)))))')
        for num,pname,side,typ,px,py,a in pins:
            atx,aty=round(x+px,4),round(y-py,4)
            if num in nets:
                self.items.append(f'(label {q(nets[num])} (at {atx} {aty} 0) (effects (font (size 0.8 0.8)) (justify left bottom)) (uuid {q(uid())}))')
            else:
                self.items.append(f'(no_connect (at {atx} {aty}) (uuid {q(uid())}))')

    def note(self, content, x, y):
        self.items.append(f'(text {q(content)} (at {x} {y} 0) (effects (font (size 1.0 1.0)) (justify left)) (uuid {q(uid())}))')

    def write(self, path):
        path.mkdir(parents=True,exist_ok=True)
        sch=f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(self.root)}) (paper "A2") (title_block (title {q(self.title)}) (rev "UNVERIFIED DRAFT") (date "2026-11-15")) (lib_symbols {" ".join(self.symbols)}) {" ".join(self.items)} (embedded_fonts no))'
        (path/f'{self.name}.kicad_sch').write_text(sch,encoding='utf-8')
        (path/f'{self.name}.kicad_pro').write_text('{}\n',encoding='utf-8')
        lib='(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor") '+' '.join(s.replace('Project:','') for s in self.symbols)+')'
        (path/'Project.kicad_sym').write_text(lib,encoding='utf-8')
        (path/'sym-lib-table').write_text('(sym_lib_table (lib (name "Project") (type "KiCad") (uri "${KIPRJMOD}/Project.kicad_sym") (options "") (descr "Manufacturer pin verified draft symbols")))\n',encoding='utf-8')

P=[('1','1','L','passive'),('2','2','R','passive')]

def build_hv(path):
    d=Draft('HV_RevA','PROJECT-NIXIDORO HV control interface - transformer unverified')
    d.define('MAX668',[(str(i),name,'L' if i<=5 else 'R',typ) for i,name,typ in [
        (1,'LDO','power_out'),(2,'FREQ','input'),(3,'GND','power_in'),(4,'REF','power_out'),(5,'FB','input'),
        (6,'CS+','input'),(7,'PGND','power_in'),(8,'EXT','output'),(9,'VCC','power_in'),(10,'SYNC/SHDN','input')]],30.48,25.4)
    d.define('PASSIVE',P,10.16,10.16)
    d.define('SUPPLY_MARK', [('1','external supply','R','power_out')],10.16,10.16)
    d.place('SUPPLY_MARK','PWR1','PWR J1 +5V source',28,110,{'1':'+5V_HV'})
    d.place('SUPPLY_MARK','PWR2','PWR J1 GND return',28,125,{'1':'GND'})
    d.define('CONN4',[(str(i),str(i),'L','passive') for i in range(1,5)],17.78,17.78)
    d.define('CONN2',[(str(i),str(i),'L','passive') for i in range(1,3)],17.78,12.7)
    d.place('CONN4','J1','PWR-HV LV interface tentative',45,55,{'1':'+5V_HV','2':'GND','3':'HV_EN_REQ','4':'HV_FAULT_N'})
    d.place('MAX668','U1','MAX668EUB+T',125,60,{'1':'MAX_LDO','2':'MAX_FREQ','3':'GND','4':'MAX_REF','5':'HV_FB_TODO','6':'HV_CS_TODO','7':'GND','8':'MOS_GATE_TODO','9':'+5V_HV','10':'HV_RUN_TODO'},'Package_SO:MSOP-10_3x3mm_P0.5mm','https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf')
    for ref,val,x,y,n1,n2 in [('C1','1uF LDO bypass',55,105,'MAX_LDO','GND'),('C2','0.22uF REF bypass',85,105,'MAX_REF','GND'),('C3','0.1uF VCC bypass',115,105,'+5V_HV','GND'),('R1','200k 250kHz candidate',145,105,'MAX_FREQ','GND'),('R2','100k default OFF',175,105,'HV_RUN_TODO','GND')]:
        d.place('PASSIVE',ref,val,x,y,{'1':n1,'2':n2})
    d.place('CONN2','J2','HV output RESERVED no generator',215,55,{'1':'HV_OUT_TODO','2':'HV_RETURN_TODO'})
    for i,note in enumerate([
        'NO HV POWER STAGE: T1 ratio Lp saturation isolation and temperature unverified.',
        'HV_FB_TODO/CS_TODO/MOS_GATE_TODO are UNCONNECTED stage interfaces, not a working converter.',
        'HV_RUN_TODO is pulled low; HV_EN_REQ not yet connected. OVP and discharge absent.',
        'J2 is an interface reservation only. No 200V supply can be produced by this schematic.',
        'TTRN-060S-013-T JLC listing has no electrical transformer specification; no substitution assumed.',
        'Do not manufacture, energize, or populate until independent OVP/bleeder and stage are reviewed.'
    ]): d.note(note,25,145+i*5)
    d.write(path)

def build_ctrl(path):
    d=Draft('CTRL_RevA','PROJECT-NIXIDORO CTRL/DISP pin-level draft')
    d.define('PASSIVE',P,10.16,10.16)
    pico_names={1:'GP0',2:'GP1',3:'GND',4:'GP2',5:'GP3',6:'GP4',7:'GP5',8:'GND',9:'GP6',10:'GP7',11:'GP8',12:'GP9',13:'GND',14:'GP10',15:'GP11',16:'GP12',17:'GP13',18:'GND',19:'GP14',20:'GP15',21:'GP16',22:'GP17',23:'GND',24:'GP18',25:'GP19',26:'GP20',27:'GP21',28:'GND',29:'GP22',30:'RUN',31:'GP26_ADC0',32:'GP27_ADC1',33:'AGND',34:'GP28_ADC2',35:'ADC_VREF',36:'3V3_OUT',37:'3V3_EN',38:'GND',39:'VSYS',40:'VBUS'}
    pico_nets={1:'HV_DATA_3V3',2:'HV_CLK_3V3',4:'HV_LE_3V3',5:'HV_BL_3V3',6:'HV_EN_REQ',7:'HV_FAULT_N',9:'UI_NEXT_L_N',10:'UI_NEXT_R_N',11:'UI_ACTION_N',12:'ENC_A_N',14:'ENC_B_N',15:'ENC_SW_N',16:'AUDIO_PWM',17:'CHG_STAT1',19:'CHG_STAT2',21:'PWR_5V_EN',22:'ADC_SENSE_EN',25:'AUDIO_AMP_EN',26:'I2C_SDA',27:'I2C_SCL',31:'ADC_BAT',32:'ADC_SYS',34:'ADC_5V',33:'GND',36:'PICO_3V3',39:'PICO_VSYS'}
    pico_nets.update({i:'GND' for i in (3,8,13,18,23,28,38)})
    d.define('PICO2',[(str(i),pico_names[i],'L' if i<=20 else 'R','power_out' if i==36 else 'passive') for i in range(1,41)],40.64,58.42)
    d.place('PICO2','U1','Raspberry Pi Pico 2',65,75,{str(k):v for k,v in pico_nets.items()},'Module:RaspberryPi_Pico_Common_THT','https://pip-assets.raspberrypi.com/categories/1005-raspberry-pi-pico-2/documents/RP-008299-DS-2-pico-2-datasheet.pdf')
    d.define('SUPPLY_MARK', [('1','external supply','R','power_out')],10.16,10.16)
    d.place('SUPPLY_MARK','PWR1','PWR J2 5V source',28,115,{'1':'+5V_LOGIC'})
    d.place('SUPPLY_MARK','PWR2','PWR J2 GND return',28,130,{'1':'GND'})
    d.place('SUPPLY_MARK','PWR3','PWR J2 SYS amp source',28,145,{'1':'SYS_TO_AMP'})
    d.define('SN74LV4T125',[(str(i),name,'L' if i in (1,2,4,5,7,9,10,12,13,14) else 'R',typ) for i,name,typ in [
        (1,'1OE','input'),(2,'1A','input'),(3,'1Y','output'),(4,'2OE','input'),(5,'2A','input'),(6,'2Y','output'),(7,'GND','power_in'),(8,'3Y','output'),(9,'3A','input'),(10,'3OE','input'),(11,'4Y','output'),(12,'4A','input'),(13,'4OE','input'),(14,'VCC','power_in')]],27.94,35.56)
    d.place('SN74LV4T125','U2','SN74LV4T125PWR',150,75,{'1':'SHIFTER_OE_N_TODO','2':'HV_DATA_3V3','3':'HV_DATA_5V','4':'SHIFTER_OE_N_TODO','5':'HV_CLK_3V3','6':'HV_CLK_5V','7':'GND','8':'HV_LE_5V','9':'HV_LE_3V3','10':'SHIFTER_OE_N_TODO','11':'HV_BL_5V','12':'HV_BL_3V3','13':'SHIFTER_OE_N_TODO','14':'+5V_LOGIC'},'Package_SO:TSSOP-14_4.4x5mm_P0.65mm','https://www.ti.com/lit/ds/symlink/sn74lv4t125.pdf')
    hvpins=[]; hvnets={}
    for n in range(1,33):
        pin=34+n if n<=10 else n-10
        hvpins.append((str(pin),f'HV{n}','L' if n<=16 else 'R','open_collector'))
        if n<=10: net=f'TUBE_A_K{n-1}'
        elif n<=20: net=f'TUBE_B_K{n-11}'
        else: net=f'NEON_{n-20:02d}_K'
        hvnets[str(pin)]=net
    hvpins += [(str(i),name,'L' if i in (27,28,29,30,31,32,33) else 'R',typ) for i,name,typ in [(23,'DATA_OUT','output'),(24,'NC','passive'),(25,'NC','passive'),(26,'NC','passive'),(27,'POL','input'),(28,'CLK','input'),(29,'VSS','power_in'),(30,'VDD','power_in'),(31,'LE','input'),(32,'DATA_IN','input'),(33,'BL','input'),(34,'NC','passive'),(45,'EP','power_in')]]
    hvnets.update({'27':'+5V_LOGIC','28':'HV_CLK_5V','29':'GND','30':'+5V_LOGIC','31':'HV_LE_5V','32':'HV_DATA_5V','33':'HV_BL_5V','45':'GND'})
    d.define('HV5524',hvpins,40.64,58.42)
    d.place('HV5524','U3','HV5524K7-G',255,85,hvnets,'Package_DFN_QFN:QFN-44-1EP_7x7mm_P0.5mm_EP5.15x5.15mm','https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf')
    d.define('RV3028',[(str(i),name,'L' if i in (3,4,5,6,7) else 'R',typ) for i,name,typ in [(1,'CLKOUT','output'),(2,'INT','open_collector'),(3,'SCL','input'),(4,'SDA','bidirectional'),(5,'VSS','power_in'),(6,'VBACKUP','power_in'),(7,'VDD','power_in'),(8,'EVI','input')]],25.4,22.86)
    d.place('RV3028','U4','RV-3028-C7',340,67,{'3':'I2C_SCL','4':'I2C_SDA','5':'GND','6':'RTC_BACKUP_TODO','7':'PICO_3V3'},'', 'https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3028-C7.pdf')
    for ref,val,x,y,n1,n2 in [('R2','10k BL default LOW',160,135,'HV_BL_5V','GND'),('R3','10k OE disable HIGH',185,135,'+5V_LOGIC','SHIFTER_OE_N_TODO'),('C1','0.1uF HV5524 VDD',210,135,'+5V_LOGIC','GND'),('C2','0.1uF translator',235,135,'+5V_LOGIC','GND'),('R4','4.7k I2C SDA candidate',260,135,'PICO_3V3','I2C_SDA'),('R5','4.7k I2C SCL candidate',285,135,'PICO_3V3','I2C_SCL')]:
        d.place('PASSIVE',ref,val,x,y,{'1':n1,'2':n2})
    d.define('CONN5',[(str(i),str(i),'L','passive') for i in range(1,6)],17.78,20.32)
    d.define('CONN10',[(str(i),str(i),'L','passive') for i in range(1,11)],17.78,35.56)
    d.place('CONN5','J2','PWR-CTRL power provisional',55,190,{'1':'SYS_TO_MCU','2':'SYS_TO_AMP','3':'+5V_LOGIC','4':'GND','5':'GND'})
    d.place('CONN10','J3','PWR-CTRL signal provisional',110,190,{str(i):n for i,n in enumerate(['CHG_STAT1','CHG_STAT2','ADC_BAT','ADC_SYS','ADC_5V','PWR_5V_EN','HV_EN_REQ','HV_FAULT_N','GND','ADC_SENSE_EN'],1)})
    d.define('CONN2',[(str(i),str(i),'L','passive') for i in (1,2)],17.78,12.7)
    d.place('CONN2','J4','HV to DISP interface RESERVED',170,190,{'1':'HV_OUT_TODO','2':'HV_RETURN_TODO'})
    d.place('PASSIVE','D1','Schottky OR MPN TBD',215,190,{'1':'SYS_TO_MCU','2':'PICO_VSYS'})
    d.define('CONN4',[(str(i),str(i),'L','passive') for i in range(1,5)],17.78,17.78)
    d.place('CONN4','J5','OLED Adafruit 938 provisional',260,190,{'1':'PICO_3V3','2':'GND','3':'I2C_SDA','4':'I2C_SCL'})
    d.place('CONN4','J6','UI ACTION/NEXT provisional',310,190,{'1':'GND','2':'UI_ACTION_N','3':'UI_NEXT_L_N','4':'UI_NEXT_R_N'})
    d.place('CONN4','J7','Encoder provisional',355,190,{'1':'GND','2':'ENC_A_N','3':'ENC_B_N','4':'ENC_SW_N'})
    d.define('TPA2005D1',[(str(i),name,'L' if i in (1,2,3,4,7,9) else 'R',typ) for i,name,typ in [
        (1,'SHUTDOWN','input'),(2,'NC','passive'),(3,'IN+','input'),(4,'IN-','input'),
        (5,'VO+','output'),(6,'VDD','power_in'),(7,'GND','power_in'),(8,'VO-','output'),(9,'EP','power_in')]],27.94,25.4)
    d.place('TPA2005D1','U5','TPA2005D1DRBR optional',420,70,
            {'1':'AUDIO_AMP_EN','3':'AUDIO_INP_TODO','4':'AUDIO_INN_TODO',
             '5':'SPEAKER_P','6':'SYS_TO_AMP','7':'GND','8':'SPEAKER_N','9':'GND'},
            'Package_DFN_QFN:Texas_DRB0008A','https://www.ti.com/lit/ds/symlink/tpa2005d1.pdf')
    d.place('PASSIVE','R6','100k amp default OFF',370,130,{'1':'AUDIO_AMP_EN','2':'GND'})
    d.place('PASSIVE','C3','1uF amp bypass candidate',400,130,{'1':'SYS_TO_AMP','2':'GND'})
    d.place('CONN2','J8','8ohm speaker provisional',475,190,{'1':'SPEAKER_P','2':'SPEAKER_N'})
    # Electrical load abstractions only. Real tube/anode pin numbers are unknown.
    d.define('DISPLAY_PATH',P,10.16,10.16)
    d.place('PASSIVE','R100','IN12B A anode R TODO',400,185,{'1':'HV_OUT_TODO','2':'TUBE_A_ANODE'})
    d.place('PASSIVE','R101','IN12B B anode R TODO',430,185,{'1':'HV_OUT_TODO','2':'TUBE_B_ANODE'})
    for n in range(1,33):
        x=50+65*((n-1)%8); y=230+30*((n-1)//8)
        cathode=(f'TUBE_A_K{n-1}' if n<=10 else
                 f'TUBE_B_K{n-11}' if n<=20 else f'NEON_{n-20:02d}_K')
        anode=('TUBE_A_ANODE' if n<=10 else
               'TUBE_B_ANODE' if n<=20 else f'NEON_{n-20:02d}_ANODE')
        d.place('DISPLAY_PATH',f'L{n}',f'LOAD {n} NO FOOTPRINT',x,y,{'1':anode,'2':cathode})
        if n>20:
            d.place('PASSIVE',f'R{200+n-20}','Neon limit R TODO',x+22, y+12,
                    {'1':'HV_OUT_TODO','2':anode})
    for i,note in enumerate([
        '32 HV5524 outputs mapped: 1-10 IN12B A; 11-20 IN12B B; 21-32 neon 01-12.',
        'L1-L32 are load abstractions, not physical lamp pin numbers or orderable components.',
        'R100/R101/R201-212 values TBD from lamp data; no voltage ratings/footprints assigned.',
        'POL tied HIGH; BL pull-down R2; OE pull-up R3 disables translator.',
        'OE release and power-good interlock NOT BUILT. HV_EN_REQ must stay LOW during tests.',
        'RTC backup source and OLED module pullups unresolved. U5 single-ended input filter is TODO.',
        'Pico VBUS and ADC_VREF deliberately NC; J2 SYS reaches VSYS through unselected D1.',
        'J2/J3/J4/J5/J6/J7 are conceptual, no connector footprints. HV is not safe to energize.'
    ]): d.note(note,25,350+i*5)
    d.write(path)

if __name__=='__main__':
    build_hv(ROOT/'hardware'/'hv'/'RevA-draft')
    build_ctrl(ROOT/'hardware'/'ctrl'/'RevA-draft')
