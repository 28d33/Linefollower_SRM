# TechGeeks Hardware Schematics & Netlists

This directory contains the complete hardware schematics, netlists, SKiDL code, and BOM specifications for:

1. **[Blueprint 01 Robot Controller Board](file:///home/d33/linefollower_agy/hardware/blueprint01/README.md)** (Arduino Nano + TB6612FNG + LM7805 + Sensor Rail)
2. **[ARC16 16-Channel IR Sensor Array](file:///home/d33/linefollower_agy/hardware/arc16_sensor/README.md)** (16x IR Reflectance Sensors + CD4067 16:1 MUX)

---

## Directory Layout

```
hardware/
├── blueprint01/
│   ├── blueprint01.kicad_sch       <- KiCad 7/8 Schematic File
│   ├── blueprint01_netlist.net     <- Hardware Netlist
│   ├── blueprint01_skidl.py        <- SKiDL Generator
│   └── README.md                   <- Documentation & BOM
│
├── arc16_sensor/
│   ├── arc16_sensor.kicad_sch      <- KiCad 7/8 Schematic File
│   ├── arc16_netlist.net           <- Hardware Netlist
│   ├── arc16_skidl.py              <- SKiDL Generator
│   └── README.md                   <- Documentation & BOM
│
└── generate_hardware_files.py      <- Automated Generator Script
```

---

## Hardware Interconnect

```
 ┌──────────────────────────────────────┐       8-Pin Ribbon Cable       ┌──────────────────────────────────────┐
 │   ARC16 16-Channel IR Array          ├───────────────────────────────►│ Blueprint 01 Controller Board        │
 │                                      │  5V, GND, S0-S3, E, SIG        │                                      │
 │ - 16x IR LEDs + Phototransistors     │                                │ - Arduino Nano (ATmega328P)          │
 │ - CD4067 16:1 Multiplexer            │                                │ - TB6612FNG Motor Driver             │
 └──────────────────────────────────────┘                                │ - LM7805 5V Regulator                │
                                                                         │ - Motor Screw Terminals (A & B)       │
                                                                         └──────────────────────────────────────┘
```
