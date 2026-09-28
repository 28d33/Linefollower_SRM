# ARC16 — 16-Channel 2D Analog IR Sensor Array Schematic

Official KiCad schematic and hardware netlist for the **ARC16 Sensor Array** by TECHGEEKS.

---

## Files

- [`arc16_sensor.kicad_sch`](file:///home/d33/linefollower_agy/hardware/arc16_sensor/arc16_sensor.kicad_sch) — KiCad 7/8 schematic file
- [`arc16_netlist.net`](file:///home/d33/linefollower_agy/hardware/arc16_sensor/arc16_netlist.net) — KiCad hardware netlist
- [`arc16_skidl.py`](file:///home/d33/linefollower_agy/hardware/arc16_sensor/arc16_skidl.py) — Python SKiDL circuit generator

---

## Schematic Architecture

```
         ┌─────────────────────────────────────────────────────────┐
         │       16 x IR Reflectance Channels (Curved 2D)         │
         │ (IR Emitters D0..D15 + Phototransistors Q0..Q15)        │
         └────────────────────────────┬────────────────────────────┘
                                      │ 16 Analog Signal Lines
                                      ▼
                      ┌──────────────────────────────┐
                      │ 74HC4067 / CD4067 16:1 MUX   │
                      └──────────────┬───────────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
            4 Select Lines        Enable Pin        1 Signal Line
            (S0, S1, S2, S3)         (~E)               (SIG)
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     ▼
                        8-Pin Controller Connector
```

---

## MUX Address Mapping (CD4067 / 74HC4067)

| Channel Index | Sensor Name | MUX Input Pin | Binary Select Lines (S3 S2 S1 S0) | Position |
|---|---|---|---|---|
| **0** | Sensor 0 | I0 (Pin 9) | `0 0 0 0` | Far Right (+7.5) |
| **1** | Sensor 1 | I1 (Pin 8) | `0 0 0 1` | Right Wing (+6.5) |
| **2** | Sensor 2 | I2 (Pin 7) | `0 0 1 0` | Right (+5.5) |
| **3** | Sensor 3 | I3 (Pin 6) | `0 0 1 1` | Right (+4.5) |
| **4** | Sensor 4 | I4 (Pin 5) | `0 1 0 0` | Right (+3.5) |
| **5** | Sensor 5 | I5 (Pin 4) | `0 1 0 1` | Mid-Right (+2.5) |
| **6** | Sensor 6 | I6 (Pin 3) | `0 1 1 0` | Inner-Right (+1.5) |
| **7** | Sensor 7 | I7 (Pin 2) | `0 1 1 1` | Center-Right (+0.5) |
| **8** | Sensor 8 | I8 (Pin 23) | `1 0 0 0` | Center-Left (-0.5) |
| **9** | Sensor 9 | I9 (Pin 22) | `1 0 0 1` | Inner-Left (-1.5) |
| **10** | Sensor 10 | I10 (Pin 21) | `1 0 1 0` | Mid-Left (-2.5) |
| **11** | Sensor 11 | I11 (Pin 20) | `1 0 1 1` | Left (-3.5) |
| **12** | Sensor 12 | I12 (Pin 19) | `1 1 0 0` | Left (-4.5) |
| **13** | Sensor 13 | I13 (Pin 18) | `1 1 0 1` | Left (-5.5) |
| **14** | Sensor 14 | I14 (Pin 17) | `1 1 1 0` | Left Wing (-6.5) |
| **15** | Sensor 15 | I15 (Pin 16) | `1 1 1 1` | Far Left (-7.5) |

---

## Bill of Materials (BOM)

| Reference | Qty | Component / Value | Footprint / Package |
|---|---|---|---|
| **U1** | 1 | 74HC4067 / CD4067 16:1 Analog MUX | SOIC-24W / DIP-24 |
| **D_E0 .. D_E15** | 16 | 3mm IR Emitter LEDs (940nm) | LED D3.0mm THT |
| **Q0 .. Q15** | 16 | 3mm NPN IR Phototransistors | LED D3.0mm THT |
| **R_E0 .. R_E15** | 16 | 100 Ω Emitter Resistors | 0805 SMD |
| **R_P0 .. R_P15** | 16 | 10 kΩ Phototransistor Pull-Downs| 0805 SMD |
| **C1** | 1 | 0.1 µF Decoupling Capacitor | 0805 SMD |
| **J1** | 1 | 8-pin Male Connector Header | 2.54mm Pitch Header |

---

## Connector Pinout (J1 $\rightarrow$ Controller)

1. **VCC:** +5V DC
2. **GND:** Ground
3. **S0:** Address Select 0 (A0)
4. **S1:** Address Select 1 (A1)
5. **S2:** Address Select 2 (A2)
6. **S3:** Address Select 3 (A3)
7. **E:** Enable (A4, Active LOW)
8. **SIG:** Analog Output Signal (A5)
