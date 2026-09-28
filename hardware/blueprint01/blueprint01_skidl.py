#!/usr/bin/env python3
"""
SKiDL Netlist & Circuit Generator for Blueprint 01 Robot Controller Board
Hardware: Arduino Nano + TB6612FNG Dual Motor Driver + LM7805 + Rail Headers
"""

from skidl import *

# Initialize Circuit
reset()

# Components Definition
nano     = Part('MCU_Module', 'Arduino_Nano', footprint='Module:Arduino_Nano')
tb6612   = Part('Driver_Motor', 'TB6612FNG', footprint='Package_SO:SSOP-24_5.3x8.2mm_P0.65mm')
lm7805   = Part('Regulator_Linear', 'LM7805_TO220', footprint='Package_TO_SOT_THT:TO-220-3_Vertical')
diode    = Part('Device', 'D_Schottky', value='SS14', footprint='Diode_SMD:D_SMA')
c_in     = Part('Device', 'C_Polarized', value='100uF', footprint='Capacitor_THT:CP_Radial_D6.3mm_P2.50mm')
c_out    = Part('Device', 'C', value='0.1uF', footprint='Capacitor_SMD:C_0805_2012Metric')

# Buttons & LEDs
btn_lb   = Part('Switch', 'SW_Push', value='LB_Button', footprint='Button_Switch_THT:SW_PUSH_6mm')
btn_rb   = Part('Switch', 'SW_Push', value='RB_Button', footprint='Button_Switch_THT:SW_PUSH_6mm')
led1     = Part('Device', 'LED', value='LED1_Ind', footprint='LED_THT:LED_D3.0mm')
led2     = Part('Device', 'LED', value='LED2_Ind', footprint='LED_THT:LED_D3.0mm')
r_led1   = Part('Device', 'R', value='330', footprint='Resistor_SMD:R_0805_2012Metric')
r_led2   = Part('Device', 'R', value='330', footprint='Resistor_SMD:R_0805_2012Metric')

# Connectors & Terminals
term_pwr = Part('Connector', 'Screw_Terminal_01x02', footprint='TerminalBlock:TerminalBlock_bornier-2_P5.08mm')
term_motA= Part('Connector', 'Screw_Terminal_01x02', footprint='TerminalBlock:TerminalBlock_bornier-2_P5.08mm')
term_motB= Part('Connector', 'Screw_Terminal_01x02', footprint='TerminalBlock:TerminalBlock_bornier-2_P5.08mm')
rail_hdr = Part('Connector', 'Conn_01x10_Pin', footprint='Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical')

# Nets
vin  = Net('VIN')
vcc5 = Net('5V')
gnd  = Net('GND')

# Power Connections
term_pwr[1] += diode['A']
diode['K']  += vin, lm7805['VI'], c_in[1], tb6612['VM'], nano['VIN']
term_pwr[2] += gnd
lm7805['GND'] += gnd
c_in[2]     += gnd
c_out[2]    += gnd
lm7805['VO']+= vcc5, c_out[1], nano['5V'], tb6612['VCC'], rail_hdr[1]
nano['GND'] += gnd
tb6612['GND'] += gnd
rail_hdr[2] += gnd

# Motor Driver Connections (Control lines from Arduino Nano)
nano['D3']  += tb6612['PWMA']
nano['D4']  += tb6612['AIN2']
nano['D5']  += tb6612['AIN1']
nano['D6']  += tb6612['STDBY']
nano['D7']  += tb6612['BIN1']
nano['D8']  += tb6612['BIN2']
nano['D9']  += tb6612['PWMB']

# Motor Outputs to Screw Terminals
tb6612['AO1'] += term_motA[1]
tb6612['AO2'] += term_motA[2]
tb6612['BO1'] += term_motB[1]
tb6612['BO2'] += term_motB[2]

# Button Connections (Pullup to GND)
nano['D2']  += btn_lb[1]
btn_lb[2]   += gnd
nano['D10'] += btn_rb[1]
btn_rb[2]   += gnd

# LED Connections
nano['D11'] += r_led1[1]
r_led1[2]   += led1['A']
led1['K']   += gnd

nano['D12'] += r_led2[1]
r_led2[2]   += led2['A']
led2['K']   += gnd

# Sensor Rail Header (A0 to A7)
nano['A0']  += rail_hdr[3]   # S0
nano['A1']  += rail_hdr[4]   # S1
nano['A2']  += rail_hdr[5]   # S2
nano['A3']  += rail_hdr[6]   # S3
nano['A4']  += rail_hdr[7]   # E
nano['A5']  += rail_hdr[8]   # SIG
nano['A6']  += rail_hdr[9]
nano['A7']  += rail_hdr[10]

# Generate SKiDL Netlist
generate_netlist(filename='/home/d33/linefollower_agy/hardware/blueprint01/blueprint01_netlist.net')
print("Generated SKiDL Netlist: /home/d33/linefollower_agy/hardware/blueprint01/blueprint01_netlist.net")
