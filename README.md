# Line Follower Firmware

**Hardware:** TechGeeks ARC16 (16-ch IR sensor) + Blueprint 01 Robot Controller Board (Arduino Nano + TB6612FNG)

---

## Libraries Required

Install these before compiling:

| Library | Source |
|---|---|
| `ARC16` | https://github.com/Techgeeks-store/ARC16-Sensor-Library |
| `RCBoard` | https://github.com/Techgeeks-store/Blueprint01-Robot-Controller-Board |

**Install via Arduino IDE:** Sketch → Include Library → Add .ZIP Library…

---

## Wiring

| ARC16 Pin | Arduino Nano | Notes |
|---|---|---|
| S0 | A0 | MUX select 0 |
| S1 | A1 | MUX select 1 |
| S2 | A2 | MUX select 2 |
| S3 | A3 | MUX select 3 |
| E  | A4 | Enable (active LOW, library handles it) |
| SIG | A5 | Analog output signal |
| VCC | 5V | From Blueprint01 sensor rail |
| GND | GND | Common ground |

> All 6 pins sit on the Blueprint01's sensor rail — just plug in.

---

## Quick Start

1. Clone this repo and open `firmware/linefollower/linefollower.ino` in Arduino IDE.
2. Install both libraries above.
3. Upload to the Arduino Nano on your Blueprint 01 board.
4. Open Serial Monitor at **115200 baud**.
5. On first boot, `CALIBRATE_ON_BOOT = true` → slowly sweep the sensor over the track for 5 seconds.
6. Press **LB (Left Button)** to start.  Press **RB (Right Button)** to stop.

---

## Tuning Phases

Work through these phases. Commit and tag each milestone.

### Phase 1 — Calibration + raw sensor print (`v0.1`)
- Set `CALIBRATE_ON_BOOT = true`
- Set `BASE_SPEED = 0` (motors off)
- Uncomment the debug Serial block in the loop
- Run and observe raw values; adjust `LINE_THRESHOLD`

### Phase 2 — P-only control (`v0.2`)
```cpp
#define KP  0.03
#define KI  0.0
#define KD  0.0
#define BASE_SPEED  120
```
Robot should follow the line but wobble.

### Phase 3 — PD control (`v0.3`)
```cpp
#define KP  0.03
#define KI  0.0
#define KD  0.8
#define BASE_SPEED  150
```
Wobble should reduce significantly.

### Phase 4 — Competition PID (`v1.0`)
```cpp
#define KP  0.06
#define KI  0.0001
#define KD  1.5
#define BASE_SPEED  200
```
Raise speed gradually. Add integral only if the robot consistently drifts to one side.

---

## Configuration Reference

| Constant | Default | Description |
|---|---|---|
| `BLACK_LINE_ON_WHITE` | `true` | `false` = white line on black |
| `BASE_SPEED` | `130` | Base motor speed (0–255) |
| `KP` | `0.03` | Proportional gain |
| `KI` | `0.0` | Integral gain |
| `KD` | `0.0` | Derivative gain |
| `LINE_THRESHOLD` | `500` | ADC value above which sensor sees the line |
| `CALIBRATE_ON_BOOT` | `true` | Run 5s calibration on every startup |

---

## Button Map

| Button | Action |
|---|---|
| LB (D2) | Start robot |
| RB (D10) | Emergency stop |

---

## Git Tag History

| Tag | Description |
|---|---|
| `v0.1` | Initial firmware + calibration |
| `v0.2` | P-only line following |
| `v0.3` | PD control |
| `v1.0` | Full PID, competition speed |
