#!/usr/bin/env python3
"""
Hardware Netlist & KiCad Schematic Generator
Generates KiCad 7/8 Schematic (.kicad_sch) and Netlist (.net) files for:
  1. Blueprint 01 Robot Controller Board
  2. ARC16 16-Channel IR Sensor Array
"""

import os

# ─────────────────────────────────────────────────────────────
# 1. Blueprint 01 Netlist Generator
# ─────────────────────────────────────────────────────────────

def generate_blueprint01_netlist(filepath):
    netlist = """(export (version D)
  (design
    (source "blueprint01.kicad_sch")
    (date "2026-09-28")
    (tool "TechGeeks Netlist Generator")
  )
  (components
    (comp (ref A1) (value "Arduino_Nano") (footprint "Module:Arduino_Nano"))
    (comp (ref U1) (value "TB6612FNG") (footprint "Package_SO:SSOP-24_5.3x8.2mm_P0.65mm"))
    (comp (ref U2) (value "LM7805") (footprint "Package_TO_SOT_THT:TO-220-3_Vertical"))
    (comp (ref D1) (value "1N4007 / SS14") (footprint "Diode_SMD:D_SMA"))
    (comp (ref C1) (value "100uF") (footprint "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"))
    (comp (ref C2) (value "0.1uF") (footprint "Capacitor_SMD:C_0805_2012Metric"))
    (comp (ref SW1) (value "LB_Button") (footprint "Button_Switch_THT:SW_PUSH_6mm"))
    (comp (ref SW2) (value "RB_Button") (footprint "Button_Switch_THT:SW_PUSH_6mm"))
    (comp (ref LED1) (value "LED1_Ind") (footprint "LED_THT:LED_D3.0mm"))
    (comp (ref LED2) (value "LED2_Ind") (footprint "LED_THT:LED_D3.0mm"))
    (comp (ref R1) (value "330") (footprint "Resistor_SMD:R_0805_2012Metric"))
    (comp (ref R2) (value "330") (footprint "Resistor_SMD:R_0805_2012Metric"))
    (comp (ref J1) (value "POWER_IN") (footprint "TerminalBlock:TerminalBlock_bornier-2_P5.08mm"))
    (comp (ref J2) (value "MOTOR_A") (footprint "TerminalBlock:TerminalBlock_bornier-2_P5.08mm"))
    (comp (ref J3) (value "MOTOR_B") (footprint "TerminalBlock:TerminalBlock_bornier-2_P5.08mm"))
    (comp (ref J4) (value "SENSOR_RAIL") (footprint "Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical"))
  )
  (nets
    (net (code 1) (name "VIN") (node (ref J1) (pin 1)) (node (ref D1) (pin 1)))
    (net (code 2) (name "VIN_PROT") (node (ref D1) (pin 2)) (node (ref U2) (pin 1)) (node (ref C1) (pin 1)) (node (ref U1) (pin 9)) (node (ref A1) (pin 29)))
    (net (code 3) (name "+5V") (node (ref U2) (pin 3)) (node (ref C2) (pin 1)) (node (ref A1) (pin 30)) (node (ref U1) (pin 8)) (node (ref J4) (pin 1)))
    (net (code 4) (name "GND") (node (ref J1) (pin 2)) (node (ref U2) (pin 2)) (node (ref C1) (pin 2)) (node (ref C2) (pin 2)) (node (ref A1) (pin 4)) (node (ref U1) (pin 10)) (node (ref SW1) (pin 2)) (node (ref SW2) (pin 2)) (node (ref LED1) (pin 2)) (node (ref LED2) (pin 2)) (node (ref J4) (pin 2)))

    (net (code 5) (name "PWMA") (node (ref A1) (pin 6)) (node (ref U1) (pin 1)))
    (net (code 6) (name "AIN2") (node (ref A1) (pin 7)) (node (ref U1) (pin 2)))
    (net (code 7) (name "AIN1") (node (ref A1) (pin 8)) (node (ref U1) (pin 3)))
    (net (code 8) (name "STDBY") (node (ref A1) (pin 9)) (node (ref U1) (pin 4)))
    (net (code 9) (name "BIN1") (node (ref A1) (pin 10)) (node (ref U1) (pin 5)))
    (net (code 10) (name "BIN2") (node (ref A1) (pin 11)) (node (ref U1) (pin 6)))
    (net (code 11) (name "PWMB") (node (ref A1) (pin 12)) (node (ref U1) (pin 7)))

    (net (code 12) (name "MOTOR_A1") (node (ref U1) (pin 11)) (node (ref J2) (pin 1)))
    (net (code 13) (name "MOTOR_A2") (node (ref U1) (pin 12)) (node (ref J2) (pin 2)))
    (net (code 14) (name "MOTOR_B2") (node (ref U1) (pin 13)) (node (ref J3) (pin 2)))
    (net (code 15) (name "MOTOR_B1") (node (ref U1) (pin 14)) (node (ref J3) (pin 1)))

    (net (code 16) (name "BTN_LB") (node (ref A1) (pin 5)) (node (ref SW1) (pin 1)))
    (net (code 17) (name "BTN_RB") (node (ref A1) (pin 13)) (node (ref SW2) (pin 1)))

    (net (code 18) (name "LED1") (node (ref A1) (pin 14)) (node (ref R1) (pin 1)))
    (net (code 19) (name "LED1_ANODE") (node (ref R1) (pin 2)) (node (ref LED1) (pin 1)))
    (net (code 20) (name "LED2") (node (ref A1) (pin 15)) (node (ref R2) (pin 1)))
    (net (code 21) (name "LED2_ANODE") (node (ref R2) (pin 2)) (node (ref LED2) (pin 1)))

    (net (code 22) (name "SENSOR_A0_S0") (node (ref A1) (pin 19)) (node (ref J4) (pin 3)))
    (net (code 23) (name "SENSOR_A1_S1") (node (ref A1) (pin 20)) (node (ref J4) (pin 4)))
    (net (code 24) (name "SENSOR_A2_S2") (node (ref A1) (pin 21)) (node (ref J4) (pin 5)))
    (net (code 25) (name "SENSOR_A3_S3") (node (ref A1) (pin 22)) (node (ref J4) (pin 6)))
    (net (code 26) (name "SENSOR_A4_E")  (node (ref A1) (pin 23)) (node (ref J4) (pin 7)))
    (net (code 27) (name "SENSOR_A5_SIG")(node (ref A1) (pin 24)) (node (ref J4) (pin 8)))
    (net (code 28) (name "SENSOR_A6")    (node (ref A1) (pin 25)) (node (ref J4) (pin 9)))
    (net (code 29) (name "SENSOR_A7")    (node (ref A1) (pin 26)) (node (ref J4) (pin 10)))
  )
)
"""
    with open(filepath, "w") as f:
        f.write(netlist.strip())
    print(f"Generated Blueprint01 Netlist: {filepath}")


# ─────────────────────────────────────────────────────────────
# 2. ARC16 Netlist Generator
# ─────────────────────────────────────────────────────────────

def generate_arc16_netlist(filepath):
    comp_str = ""
    net_str = ""

    # MUX IC
    comp_str += '    (comp (ref U1) (value "74HC4067 / CD4067") (footprint "Package_SO:SOIC-24W_7.5x15.4mm_P1.27mm"))\n'
    comp_str += '    (comp (ref C1) (value "0.1uF") (footprint "Capacitor_SMD:C_0805_2012Metric"))\n'
    comp_str += '    (comp (ref J1) (value "MAIN_CONNECTOR") (footprint "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical"))\n'

    # Power nets
    net_str += '    (net (code 1) (name "VCC_5V") (node (ref J1) (pin 1)) (node (ref U1) (pin 24)) (node (ref C1) (pin 1))'
    for i in range(16):
        net_str += f' (node (ref R_E{i}) (pin 1)) (node (ref Q{i}) (pin 1))'
    net_str += ')\n'

    net_str += '    (net (code 2) (name "GND") (node (ref J1) (pin 2)) (node (ref U1) (pin 12)) (node (ref C1) (pin 2))'
    for i in range(16):
        net_str += f' (node (ref D_E{i}) (pin 2)) (node (ref R_P{i}) (pin 2))'
    net_str += ')\n'

    # Control lines
    net_str += '    (net (code 3) (name "S0") (node (ref J1) (pin 3)) (node (ref U1) (pin 10)))\n'
    net_str += '    (net (code 4) (name "S1") (node (ref J1) (pin 4)) (node (ref U1) (pin 11)))\n'
    net_str += '    (net (code 5) (name "S2") (node (ref J1) (pin 5)) (node (ref U1) (pin 14)))\n'
    net_str += '    (net (code 6) (name "S3") (node (ref J1) (pin 6)) (node (ref U1) (pin 13)))\n'
    net_str += '    (net (code 7) (name "E")  (node (ref J1) (pin 7)) (node (ref U1) (pin 15)))\n'
    net_str += '    (net (code 8) (name "SIG")(node (ref J1) (pin 8)) (node (ref U1) (pin 1)))\n'

    net_code = 9
    mux_pins = [9, 8, 7, 6, 5, 4, 3, 2, 23, 22, 21, 20, 19, 18, 17, 16]

    for i in range(16):
        comp_str += f'    (comp (ref D_E{i}) (value "IR_LED_{i}") (footprint "LED_THT:LED_D3.0mm"))\n'
        comp_str += f'    (comp (ref R_E{i}) (value "100") (footprint "Resistor_SMD:R_0805_2012Metric"))\n'
        comp_str += f'    (comp (ref Q{i}) (value "IR_PT_{i}") (footprint "LED_THT:LED_D3.0mm"))\n'
        comp_str += f'    (comp (ref R_P{i}) (value "10k") (footprint "Resistor_SMD:R_0805_2012Metric"))\n'

        # Emitter connection
        net_str += f'    (net (code {net_code}) (name "IR_EMIT_{i}") (node (ref R_E{i}) (pin 2)) (node (ref D_E{i}) (pin 1)))\n'
        net_code += 1

        # Sensor Signal node
        net_str += f'    (net (code {net_code}) (name "IR_SIG_{i}") (node (ref Q{i}) (pin 2)) (node (ref R_P{i}) (pin 1)) (node (ref U1) (pin {mux_pins[i]})))\n'
        net_code += 1

    netlist = f"""(export (version D)
  (design
    (source "arc16_sensor.kicad_sch")
    (date "2026-09-28")
    (tool "TechGeeks Netlist Generator")
  )
  (components
{comp_str.rstrip()}
  )
  (nets
{net_str.rstrip()}
  )
)
"""
    with open(filepath, "w") as f:
        f.write(netlist.strip())
    print(f"Generated ARC16 Netlist: {filepath}")

if __name__ == "__main__":
    generate_blueprint01_netlist("/home/d33/linefollower_agy/hardware/blueprint01/blueprint01_netlist.net")
    generate_arc16_netlist("/home/d33/linefollower_agy/hardware/arc16_sensor/arc16_netlist.net")
