#!/usr/bin/env python3
"""
Clean KiCad 7/8/9 Schematic Generator
For TechGeeks Hardware:
  1. Blueprint 01 Robot Controller Board
  2. ARC16 16-Channel IR Sensor Array (Clean Net-Label Architecture)
"""

import os
import sys

# ─────────────────────────────────────────────────────────────
# 1. Blueprint 01 Robot Controller Board Schematic Generator
# ─────────────────────────────────────────────────────────────

def create_blueprint01_kicad_sch(filepath):
    sch_content = """(kicad_sch (version 20230121) (generator "TechGeeks KiCad Generator")
  (uuid "d0a1b2c3-4e5f-6a7b-8c9d-0e1f2a3b4c5d")
  (paper "A3")

  (title_block
    (title "Blueprint 01 - Robot Controller Board")
    (date "2026-09-28")
    (rev "1.0")
    (company "TechGeeks Robotics")
    (comment 1 "Arduino Nano + TB6612FNG + LM7805 + Sensor Rail")
    (comment 2 "Designed for Line Follower Robots")
  )

  (lib_symbols
    (symbol "MCU_Module:Arduino_Nano" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
      (property "Reference" "A" (at 0 22.86 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Arduino_Nano" (at 0 -22.86 0) (effects (font (size 1.27 1.27))))
      (symbol "Arduino_Nano_0_1"
        (rectangle (start -10.16 20.32) (end 10.16 -20.32) (stroke (width 0.254) (type default)))
      )
      (symbol "Arduino_Nano_1_1"
        (pin passive line (at -12.7 17.78 0) (length 2.54) (name "D1/TX" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 15.24 0) (length 2.54) (name "D0/RX" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 12.7 0) (length 2.54) (name "RESET" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -12.7 10.16 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 7.62 0) (length 2.54) (name "D2/LB" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 5.08 0) (length 2.54) (name "D3/PWMA" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 2.54 0) (length 2.54) (name "D4/AIN2" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 0 0) (length 2.54) (name "D5/AIN1" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -2.54 0) (length 2.54) (name "D6/STDBY" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -5.08 0) (length 2.54) (name "D7/BIN1" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -7.62 0) (length 2.54) (name "D8/BIN2" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -10.16 0) (length 2.54) (name "D9/PWMB" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -12.7 0) (length 2.54) (name "D10/RB" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -15.24 0) (length 2.54) (name "D11/LED1" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -12.7 -17.78 0) (length 2.54) (name "D12/LED2" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))

        (pin power_out line (at 12.7 17.78 180) (length 2.54) (name "5V" (effects (font (size 1.27 1.27)))) (number "30" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 12.7 15.24 180) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27)))) (number "29" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 12.7 180) (length 2.54) (name "A7" (effects (font (size 1.27 1.27)))) (number "26" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 10.16 180) (length 2.54) (name "A6" (effects (font (size 1.27 1.27)))) (number "25" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 7.62 180) (length 2.54) (name "A5/SIG" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 5.08 180) (length 2.54) (name "A4/E" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 2.54 180) (length 2.54) (name "A3/S3" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 0 180) (length 2.54) (name "A2/S2" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 -2.54 180) (length 2.54) (name "A1/S1" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 -5.08 180) (length 2.54) (name "A0/S0" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 -7.62 180) (length 2.54) (name "REF" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
        (pin power_out line (at 12.7 -10.16 180) (length 2.54) (name "3V3" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 -12.7 180) (length 2.54) (name "D13" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
      )
    )

    (symbol "Driver_Motor:TB6612FNG" (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 17.78 0) (effects (font (size 1.27 1.27))))
      (property "Value" "TB6612FNG" (at 0 -17.78 0) (effects (font (size 1.27 1.27))))
      (symbol "TB6612FNG_0_1"
        (rectangle (start -10.16 15.24) (end 10.16 -15.24) (stroke (width 0.254) (type default)))
      )
      (symbol "TB6612FNG_1_1"
        (pin input line (at -12.7 12.7 0) (length 2.54) (name "PWMA" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin input line (at -12.7 10.16 0) (length 2.54) (name "AIN2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin input line (at -12.7 7.62 0) (length 2.54) (name "AIN1" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin input line (at -12.7 5.08 0) (length 2.54) (name "STDBY" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
        (pin input line (at -12.7 2.54 0) (length 2.54) (name "BIN1" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
        (pin input line (at -12.7 0 0) (length 2.54) (name "BIN2" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
        (pin input line (at -12.7 -2.54 0) (length 2.54) (name "PWMB" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -12.7 -7.62 0) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -12.7 -10.16 0) (length 2.54) (name "VM" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -12.7 -12.7 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))

        (pin output line (at 12.7 10.16 180) (length 2.54) (name "AO1" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
        (pin output line (at 12.7 7.62 180) (length 2.54) (name "AO2" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
        (pin output line (at 12.7 -2.54 180) (length 2.54) (name "BO2" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
        (pin output line (at 12.7 -5.08 180) (length 2.54) (name "BO1" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
      )
    )

    (symbol "Regulator_Linear:LM7805" (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 7.62 0) (effects (font (size 1.27 1.27))))
      (property "Value" "LM7805" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
      (symbol "LM7805_0_1"
        (rectangle (start -7.62 5.08) (end 7.62 -5.08) (stroke (width 0.254) (type default)))
      )
      (symbol "LM7805_1_1"
        (pin input line (at -10.16 0 0) (length 2.54) (name "VI" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 -7.62 90) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin power_out line (at 10.16 0 180) (length 2.54) (name "VO" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
      )
    )
  )

  (symbol (lib_id "MCU_Module:Arduino_Nano") (at 150 120 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "00000000-0000-0000-0000-000060010001")
    (property "Reference" "A1" (at 150 95 0) (effects (font (size 1.27 1.27))))
    (property "Value" "Arduino_Nano" (at 150 145 0) (effects (font (size 1.27 1.27))))
  )

  (symbol (lib_id "Driver_Motor:TB6612FNG") (at 240 120 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "00000000-0000-0000-0000-000060010002")
    (property "Reference" "U1" (at 240 95 0) (effects (font (size 1.27 1.27))))
    (property "Value" "TB6612FNG" (at 240 145 0) (effects (font (size 1.27 1.27))))
  )

  (symbol (lib_id "Regulator_Linear:LM7805") (at 60 60 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "00000000-0000-0000-0000-000060010003")
    (property "Reference" "U2" (at 60 50 0) (effects (font (size 1.27 1.27))))
    (property "Value" "LM7805" (at 60 70 0) (effects (font (size 1.27 1.27))))
  )

  (sheet_instances
    (path "/" (page "1"))
  )
)
"""
    with open(filepath, "w") as f:
        f.write(sch_content.strip())
    print(f"Created Blueprint01 KiCad Schematic: {filepath}")


# ─────────────────────────────────────────────────────────────
# 2. ARC16 16-Channel IR Sensor Array Generator (Clean Net Labels)
# ─────────────────────────────────────────────────────────────

def create_arc16_kicad_sch(filepath):
    symbols_def = """  (lib_symbols
    (symbol "74xx:74HC4067" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 25.4 0) (effects (font (size 1.27 1.27))))
      (property "Value" "74HC4067" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))
      (symbol "74HC4067_0_1"
        (rectangle (start -12.7 22.86) (end 12.7 -22.86) (stroke (width 0.254) (type default)))
      )
      (symbol "74HC4067_1_1"
        (pin input line (at -15.24 20.32 0) (length 2.54) (name "I0" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 17.78 0) (length 2.54) (name "I1" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 15.24 0) (length 2.54) (name "I2" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 12.7 0) (length 2.54) (name "I3" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 10.16 0) (length 2.54) (name "I4" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 7.62 0) (length 2.54) (name "I5" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 5.08 0) (length 2.54) (name "I6" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 2.54 0) (length 2.54) (name "I7" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 0 0) (length 2.54) (name "I8" (effects (font (size 1.27 1.27)))) (number "23" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -2.54 0) (length 2.54) (name "I9" (effects (font (size 1.27 1.27)))) (number "22" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -5.08 0) (length 2.54) (name "I10" (effects (font (size 1.27 1.27)))) (number "21" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -7.62 0) (length 2.54) (name "I11" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -10.16 0) (length 2.54) (name "I12" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -12.7 0) (length 2.54) (name "I13" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -15.24 0) (length 2.54) (name "I14" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
        (pin input line (at -15.24 -17.78 0) (length 2.54) (name "I15" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))

        (pin input line (at 15.24 20.32 180) (length 2.54) (name "S0" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
        (pin input line (at 15.24 17.78 180) (length 2.54) (name "S1" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
        (pin input line (at 15.24 15.24 180) (length 2.54) (name "S2" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
        (pin input line (at 15.24 12.7 180) (length 2.54) (name "S3" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
        (pin input line (at 15.24 7.62 180) (length 2.54) (name "~{E}" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 15.24 0 180) (length 2.54) (name "SIG" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 15.24 -15.24 180) (length 2.54) (name "VCC" (effects (font (size 1.27 1.27)))) (number "24" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 15.24 -17.78 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
      )
    )

    (symbol "Device:LED_IR" (in_bom yes) (on_board yes)
      (property "Reference" "D" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (property "Value" "LED_IR" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (symbol "LED_IR_0_1"
        (polyline (pts (xy -1.27 2.54) (xy 1.27 0) (xy -1.27 -2.54) (xy -1.27 2.54)) (stroke (width 0.254) (type default)))
        (polyline (pts (xy 1.27 2.54) (xy 1.27 -2.54)) (stroke (width 0.254) (type default)))
      )
      (symbol "LED_IR_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 3.81 0 180) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )

    (symbol "Device:Q_Phototransistor_NPN" (in_bom yes) (on_board yes)
      (property "Reference" "Q" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
      (property "Value" "IR_PT" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
      (symbol "Q_Phototransistor_NPN_0_1"
        (circle (center 0 0) (radius 3.81) (stroke (width 0.254) (type default)))
        (polyline (pts (xy 0 2.54) (xy 0 -2.54)) (stroke (width 0.381) (type default)))
        (polyline (pts (xy 0 1.27) (xy 2.54 2.54)) (stroke (width 0.254) (type default)))
        (polyline (pts (xy 0 -1.27) (xy 2.54 -2.54)) (stroke (width 0.254) (type default)))
      )
      (symbol "Q_Phototransistor_NPN_1_1"
        (pin passive line (at 2.54 6.35 270) (length 3.81) (name "C" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 2.54 -6.35 90) (length 3.81) (name "E" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )

    (symbol "Device:R" (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (symbol "R_0_1"
        (rectangle (start -1.016 2.54) (end 1.016 -2.54) (stroke (width 0.254) (type default)))
      )
      (symbol "R_1_1"
        (pin passive line (at 0 5.08 270) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -5.08 90) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )

    (symbol "Connector:Conn_01x08_Pin" (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_01x08_Pin" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
      (symbol "Conn_01x08_Pin_0_1"
        (rectangle (start -5.08 11.43) (end 5.08 -11.43) (stroke (width 0.254) (type default)))
      )
      (symbol "Conn_01x08_Pin_1_1"
        (pin passive line (at -7.62 8.89 0) (length 2.54) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 6.35 0) (length 2.54) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 3.81 0) (length 2.54) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 1.27 0) (length 2.54) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 -1.27 0) (length 2.54) (name "Pin_5" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 -3.81 0) (length 2.54) (name "Pin_6" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 -6.35 0) (length 2.54) (name "Pin_7" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 -8.89 0) (length 2.54) (name "Pin_8" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
      )
    )
  )
"""

    placed_symbols = ""
    wires_and_labels = ""

    # Place CD4067 MUX IC on right side
    placed_symbols += """  (symbol (lib_id "74xx:74HC4067") (at 300 120 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "00000000-0000-0000-0000-000070010001")
    (property "Reference" "U1" (at 300 90 0) (effects (font (size 1.27 1.27))))
    (property "Value" "74HC4067" (at 300 150 0) (effects (font (size 1.27 1.27))))
  )\n"""

    # Place Interface Header J1 on far right
    placed_symbols += """  (symbol (lib_id "Connector:Conn_01x08_Pin") (at 380 120 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "00000000-0000-0000-0000-000070010002")
    (property "Reference" "J1" (at 380 100 0) (effects (font (size 1.27 1.27))))
    (property "Value" "INTERFACE_HEADER" (at 380 140 0) (effects (font (size 1.27 1.27))))
  )\n"""

    # 16 Channels Clean Matrix Layout (X = 30 to 255, Step = 15mm)
    for i in range(16):
        x = 30 + (i * 15)
        uid_base = f"00000000-0000-0000-0000-{i:012x}"

        # Emitter LED
        placed_symbols += f"""  (symbol (lib_id "Device:LED_IR") (at {x} 50 90) (unit 1)
    (in_bom yes) (on_board yes) (uuid "{uid_base}1")
    (property "Reference" "DE{i}" (at {x} 42 0) (effects (font (size 0.8 0.8))))
    (property "Value" "IR_LED" (at {x} 58 0) (effects (font (size 0.7 0.7))))
  )\n"""

        # Emitter Resistor (100 ohm)
        placed_symbols += f"""  (symbol (lib_id "Device:R") (at {x} 25 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "{uid_base}2")
    (property "Reference" "RE{i}" (at {x-2.5} 25 0) (effects (font (size 0.7 0.7))))
    (property "Value" "100" (at {x+2.5} 25 0) (effects (font (size 0.7 0.7))))
  )\n"""

        # Phototransistor
        placed_symbols += f"""  (symbol (lib_id "Device:Q_Phototransistor_NPN") (at {x} 110 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "{uid_base}3")
    (property "Reference" "Q{i}" (at {x-2.5} 110 0) (effects (font (size 0.8 0.8))))
    (property "Value" "IR_PT" (at {x+2.5} 110 0) (effects (font (size 0.7 0.7))))
  )\n"""

        # Phototransistor Pull-Down Resistor (10k)
        placed_symbols += f"""  (symbol (lib_id "Device:R") (at {x} 140 0) (unit 1)
    (in_bom yes) (on_board yes) (uuid "{uid_base}4")
    (property "Reference" "RP{i}" (at {x-2.5} 140 0) (effects (font (size 0.7 0.7))))
    (property "Value" "10k" (at {x+2.5} 140 0) (effects (font (size 0.7 0.7))))
  )\n"""

        # Wires & Net Labels for Channel i
        # VCC Rail -> Resistor -> LED -> GND
        wires_and_labels += f"  (wire (pts (xy {x} 10) (xy {x} 20)) (stroke (width 0) (type default)))\n"
        wires_and_labels += f"  (wire (pts (xy {x} 30) (xy {x} 50)) (stroke (width 0) (type default)))\n"
        wires_and_labels += f"  (wire (pts (xy {x} 54) (xy {x} 70)) (stroke (width 0) (type default)))\n"

        # VCC Rail -> PT Collector, PT Emitter -> Signal Node -> Pull-down -> GND
        wires_and_labels += f"  (wire (pts (xy {x} 10) (xy {x} 103.65)) (stroke (width 0) (type default)))\n"
        wires_and_labels += f"  (wire (pts (xy {x+2.54} 116.35) (xy {x+2.54} 135)) (stroke (width 0) (type default)))\n"
        wires_and_labels += f"  (wire (pts (xy {x+2.54} 145) (xy {x+2.54} 160)) (stroke (width 0) (type default)))\n"

        # Net Label for SIG_i at signal node
        wires_and_labels += f'  (label "SIG_{i}" (at {x+2.54} 125 0) (fields_autoplaced yes) (effects (font (size 1.0 1.0))))\n'

        # Net Label for MUX input pin I_i
        y_mux_pin = 140.32 - (i * 2.54)
        wires_and_labels += f'  (label "SIG_{i}" (at 284.76 {y_mux_pin} 180) (fields_autoplaced yes) (effects (font (size 1.0 1.0))))\n'

    sch_header = """(kicad_sch (version 20230121) (generator "TechGeeks KiCad Generator")
  (uuid "e1b2c3d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e")
  (paper "A2")

  (title_block
    (title "ARC16 - 16-Channel 2D Analog IR Reflectance Sensor Array")
    (date "2026-09-28")
    (rev "1.0")
    (company "TechGeeks Robotics")
    (comment 1 "Clean 16-Channel Matrix Layout with Net Labels & CD4067 MUX")
    (comment 2 "Designed for Line Follower Competition Robots")
  )
"""

    sch_footer = """  (sheet_instances
    (path "/" (page "1"))
  )
)
"""

    full_sch = sch_header + symbols_def + placed_symbols + wires_and_labels + sch_footer
    with open(filepath, "w") as f:
        f.write(full_sch.strip())
    print(f"Created Clean ARC16 KiCad Schematic: {filepath}")


if __name__ == "__main__":
    bp_path = "/home/d33/linefollower_agy/hardware/blueprint01/blueprint01.kicad_sch"
    arc_path = "/home/d33/linefollower_agy/hardware/arc16_sensor/arc16_sensor.kicad_sch"
    create_blueprint01_kicad_sch(bp_path)
    create_arc16_kicad_sch(arc_path)
