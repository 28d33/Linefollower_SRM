# Blueprint 01 — Robot Controller Board Schematic

Official KiCad schematic and hardware netlist for the **Blueprint 01 Robot Controller Board** by TECHGEEKS.

---

## Files

- [`blueprint01.kicad_sch`](file:///home/d33/linefollower_agy/hardware/blueprint01/blueprint01.kicad_sch) — KiCad 7/8 schematic file
- [`blueprint01_netlist.net`](file:///home/d33/linefollower_agy/hardware/blueprint01/blueprint01_netlist.net) — KiCad hardware netlist
- [`blueprint01_skidl.py`](file:///home/d33/linefollower_agy/hardware/blueprint01/blueprint01_skidl.py) — Python SKiDL circuit generator

---

## Schematic Architecture

```
                       ┌─────────────────────────┐
                       │  Power Input (6V - 14V) │
                       └───────────┬─────────────┘
                                   │
                           [Reverse Diode SS14]
                                   │
                 ┌─────────────────┴──────────────────┐
                 │                                    │
                 ▼                                    ▼
       ┌──────────────────┐                 ┌──────────────────┐
       │ LM7805 Regulator │                 │  TB6612FNG VM    │
       └─────────┬────────┘                 └─────────┬────────┘
                 │ 5V Rail                            │ Motor Power
                 ▼                                    ▼
       ┌──────────────────┐                 ┌──────────────────┐
       │   Arduino Nano   │◄──Controls─────┤ TB6612FNG Driver │
       └─────────┬────────┘ (PWM & Dir)     └─────────┬────────┘
                 │                                    │
        Sensor Rail (A0..A7)                 Motor A & B Terminals
```

---

## Pin Allocation Table

| Arduino Nano Pin | Signal Name | Connected Hardware | Function |
|---|---|---|---|
| **D2** | `BTN_LB` | Push Button LB | Left User Button (Calibrate) |
| **D3** | `PWMA` | TB6612FNG `PWMA` | Motor A Speed Control (PWM) |
| **D4** | `AIN2` | TB6612FNG `AIN2` | Motor A Direction 2 |
| **D5** | `AIN1` | TB6612FNG `AIN1` | Motor A Direction 1 |
| **D6** | `STDBY` | TB6612FNG `STDBY` | Motor Driver Master Enable (High = On) |
| **D7** | `BIN1` | TB6612FNG `BIN1` | Motor B Direction 1 |
| **D8** | `BIN2` | TB6612FNG `BIN2` | Motor B Direction 2 |
| **D9** | `PWMB` | TB6612FNG `PWMB` | Motor B Speed Control (PWM) |
| **D10** | `BTN_RB` | Push Button RB | Right User Button (Start/Stop) |
| **D11** | `LED1` | LED1 (Red/Green) | Status LED 1 (330Ω resistor) |
| **D12** | `LED2` | LED2 (Blue/Green) | Status LED 2 (330Ω resistor) |
| **A0** | `S0` | Sensor Rail Pin 3 | MUX Select Line 0 |
| **A1** | `S1` | Sensor Rail Pin 4 | MUX Select Line 1 |
| **A2** | `S2` | Sensor Rail Pin 5 | MUX Select Line 2 |
| **A3** | `S3` | Sensor Rail Pin 6 | MUX Select Line 3 |
| **A4** | `E` | Sensor Rail Pin 7 | MUX Enable Line (Active LOW) |
| **A5** | `SIG` | Sensor Rail Pin 8 | MUX Analog Output Signal |
| **A6** | `SPARE_A6` | Sensor Rail Pin 9 | Spare Analog Input |
| **A7** | `SPARE_A7` | Sensor Rail Pin 10 | Spare Analog Input |

---

## Bill of Materials (BOM)

| Reference | Qty | Component / Value | Footprint / Package |
|---|---|---|---|
| **A1** | 1 | Arduino Nano (ATmega328P) | Socket 30-pin DIP Header |
| **U1** | 1 | TB6612FNG Dual H-Bridge Driver | SSOP-24 SMD / Breakout |
| **U2** | 1 | LM7805 5V 1A Voltage Regulator | TO-220-3 Vertical |
| **D1** | 1 | 1N4007 / SS14 Schottky Diode | SMA SMD |
| **C1** | 1 | 100 µF 25V Electrolytic Cap | Radial D6.3mm P2.5mm |
| **C2** | 1 | 0.1 µF Ceramic Decoupling Cap | 0805 SMD |
| **SW1, SW2** | 2 | 6mm Tactile Push Buttons | SW_PUSH_6mm THT |
| **LED1, LED2**| 2 | 3mm Status LEDs | LED D3.0mm THT |
| **R1, R2** | 2 | 330 Ω 0805 Resistors | 0805 SMD |
| **J1** | 1 | 2-pin Screw Terminal (Power In) | 5.08mm Pitch Terminal Block |
| **J2, J3** | 2 | 2-pin Screw Terminals (Motor A/B)| 5.08mm Pitch Terminal Block |
| **J4** | 1 | 10-pin Female Header (Sensor Rail)| 2.54mm Pitch Header |

---

## Opening in KiCad

1. Open **KiCad Schematic Editor**.
2. Select **File → Open** and choose `blueprint01.kicad_sch`.
3. To import the netlist: **File → Import → Netlist...** and select `blueprint01_netlist.net`.
