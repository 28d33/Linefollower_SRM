#!/usr/bin/env python3
"""
SKiDL Netlist & Circuit Generator for ARC16 16-Channel IR Sensor Array
Hardware: 16x IR Emitters + 16x IR Phototransistors + CD4067 16:1 MUX IC
"""

from skidl import *

# Initialize Circuit
reset()

# MUX IC
mux = Part('74xx', '74HC4067', footprint='Package_SO:SOIC-24W_7.5x15.4mm_P1.27mm')

# Decoupling Cap
c_dec = Part('Device', 'C', value='0.1uF', footprint='Capacitor_SMD:C_0805_2012Metric')

# Connector to Main Controller
conn = Part('Connector', 'Conn_01x08_Pin', footprint='Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical')

# Power Nets
vcc = Net('VCC_5V')
gnd = Net('GND')

conn[1] += vcc
conn[2] += gnd
mux['VCC'] += vcc
mux['GND'] += gnd
c_dec[1] += vcc
c_dec[2] += gnd

# Control Lines (S0..S3, E, SIG)
conn[3] += mux['S0']
conn[4] += mux['S1']
conn[5] += mux['S2']
conn[6] += mux['S3']
conn[7] += mux['E']
conn[8] += mux['SIG']

# 16 Channel IR Reflectance Sensor Array (Emitters + Phototransistors + Resistors)
emitters = [Part('Device', 'LED_IR', value=f'IR_LED_{i}', footprint='LED_THT:LED_D3.0mm') for i in range(16)]
r_emit   = [Part('Device', 'R', value='100', footprint='Resistor_SMD:R_0805_2012Metric') for i in range(16)]

sensors  = [Part('Device', 'Q_Phototransistor_NPN', value=f'IR_PT_{i}', footprint='LED_THT:LED_D3.0mm') for i in range(16)]
r_pull   = [Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_0805_2012Metric') for i in range(16)]

mux_inputs = [mux[f'I{i}'] for i in range(16)]

for i in range(16):
    # Emitter LED circuit (VCC -> Resistor -> LED -> GND)
    vcc += r_emit[i][1]
    r_emit[i][2] += emitters[i]['A']
    emitters[i]['K'] += gnd

    # Phototransistor Circuit (VCC -> Collector, Emitter -> 10k -> GND, Node -> MUX input)
    vcc += sensors[i]['C']
    sig_node = Net(f'IR_SIG_{i}')
    sensors[i]['E'] += sig_node
    r_pull[i][1]    += sig_node
    r_pull[i][2]    += gnd
    sig_node        += mux_inputs[i]

# Generate SKiDL Netlist
generate_netlist(filename='/home/d33/linefollower_agy/hardware/arc16_sensor/arc16_netlist.net')
print("Generated SKiDL Netlist: /home/d33/linefollower_agy/hardware/arc16_sensor/arc16_netlist.net")
