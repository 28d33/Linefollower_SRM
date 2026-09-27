/*
 * ============================================================
 *  Line Follower Firmware — TechGeeks ARC16 + Blueprint 01
 * ============================================================
 *  Hardware:
 *    - Blueprint 01 Robot Controller Board (Arduino Nano + TB6612FNG)
 *    - ARC16 16-Channel IR Sensor Array (MUX architecture)
 *
 *  Libraries required:
 *    - ARC16   : https://github.com/Techgeeks-store/ARC16-Sensor-Library
 *    - RCBoard : https://github.com/Techgeeks-store/Blueprint01-Robot-Controller-Board
 *
 *  Wiring (ARC16 → Blueprint01 sensor rail):
 *    S0→A0  S1→A1  S2→A2  S3→A3  E→A4  SIG→A5
 *    VCC→5V  GND→GND
 *
 *  Button Map:
 *    LB (D2)  — Calibrate  : sweep sensor over track for 5 s
 *    RB (D10) — Start/Stop : begin or stop driving
 *
 *  LED feedback:
 *    LED1 slow blink  → waiting for calibration
 *    LED1 fast blink  → calibrating (keep sweeping)
 *    LED1 + LED2 on   → calibrated, ready to drive
 *    LED1 solid       → driving
 *    Both off         → stopped after driving
 *
 *  Serial Monitor: 115200 baud
 *
 *  Phase tags (git tag after each works):
 *    v0.1  initial skeleton
 *    v0.2  auto-calibration + button remap
 *    v0.3  PD tuning
 *    v1.0  competition speed
 * ============================================================
 */

#include <ARC16.h>
#include <RCBoard.h>

// ─── USER CONFIGURATION ─────────────────────────────────────

// Line polarity
//   true  → black line on white surface (standard)
//   false → white line on black surface (inverted)
#define BLACK_LINE_ON_WHITE  true

// Base drive speed: 0–255. Start at 130, raise once PID is tuned.
#define BASE_SPEED  130

// PID gains — tune in phases:
//   Phase 2 (P only): Kp=0.03  Ki=0.0  Kd=0.0
//   Phase 3 (PD)    : Kp=0.03  Ki=0.0  Kd=0.8
//   Phase 4 (full)  : Kp=0.06  Ki=0.0001 Kd=1.5
#define KP  0.03
#define KI  0.0
#define KD  0.0

// Calibration duration in milliseconds
#define CAL_DURATION_MS  5000

// ─── END USER CONFIGURATION ─────────────────────────────────


// ─── OBJECTS ────────────────────────────────────────────────

ARC16   sensors;
RCBoard robot;

int  select[4] = {A0, A1, A2, A3};

// Sensor readings & auto-calibration
int  rawValues[16];
int  calMin[16];
int  calMax[16];
int  calMid[16];           // per-sensor threshold = (min+max)/2
bool calibrated = false;

// PID state
float errorPrev     = 0.0f;
float errorIntegral = 0.0f;

// ─── STATE MACHINE ──────────────────────────────────────────

enum State {
  IDLE,           // waiting for LB (calibrate)
  CALIBRATING,    // sweeping for CAL_DURATION_MS
  READY,          // calibrated, waiting for RB (start)
  RUNNING,        // following the line
  STOPPED         // RB pressed while running
};

State robotState = IDLE;

// ─── LED HELPERS ─────────────────────────────────────────────

void ledAll(bool on) {
  digitalWrite(LED1, on ? HIGH : LOW);
  digitalWrite(LED2, on ? HIGH : LOW);
}

// Non-blocking blink on LED1. Call every loop().
void blinkLED1(unsigned long period) {
  static unsigned long last = 0;
  static bool on = false;
  if (millis() - last >= period) {
    last = millis();
    on = !on;
    digitalWrite(LED1, on ? HIGH : LOW);
  }
}

// ─── BUTTON HELPERS ──────────────────────────────────────────

// Returns true once per press (debounced).
bool buttonPressed(uint8_t pin) {
  if (digitalRead(pin) == LOW) {
    delay(40);
    if (digitalRead(pin) == LOW) {
      while (digitalRead(pin) == LOW);  // wait for release
      return true;
    }
  }
  return false;
}

// ─── CALIBRATION ─────────────────────────────────────────────

void startCalibration() {
  Serial.println(F(""));
  Serial.println(F("=== AUTO-CALIBRATION ==="));
  Serial.println(F("Slowly sweep the sensor over the FULL track width..."));
  Serial.print(F("You have ")); Serial.print(CAL_DURATION_MS / 1000);
  Serial.println(F(" seconds. Go!"));

  // Seed min/max with first real reading
  sensors.read(rawValues);
  for (int i = 0; i < 16; i++) {
    calMin[i] = rawValues[i];
    calMax[i] = rawValues[i];
  }

  robotState = CALIBRATING;
  unsigned long start = millis();

  while (millis() - start < CAL_DURATION_MS) {
    // Fast-blink LED1 during calibration
    blinkLED1(100);

    sensors.read(rawValues);
    for (int i = 0; i < 16; i++) {
      if (rawValues[i] < calMin[i]) calMin[i] = rawValues[i];
      if (rawValues[i] > calMax[i]) calMax[i] = rawValues[i];
    }

    // Print progress bar every 500 ms
    static unsigned long lastPrint = 0;
    if (millis() - lastPrint > 500) {
      lastPrint = millis();
      unsigned long elapsed = millis() - start;
      int pct = (int)(elapsed * 100UL / CAL_DURATION_MS);
      Serial.print(pct); Serial.println(F("%..."));
    }
  }

  // Compute per-sensor midpoint thresholds
  Serial.println(F(""));
  Serial.println(F("Calibration done. Per-sensor thresholds:"));
  Serial.println(F(" Idx | min | max | threshold"));
  Serial.println(F("-----|-----|-----|----------"));
  for (int i = 0; i < 16; i++) {
    calMid[i] = (calMin[i] + calMax[i]) / 2;
    Serial.print(F("  S")); Serial.print(i);
    if (i < 10) Serial.print(F(" "));
    Serial.print(F(" | ")); Serial.print(calMin[i]);
    Serial.print(F(" | ")); Serial.print(calMax[i]);
    Serial.print(F(" | ")); Serial.println(calMid[i]);
  }

  calibrated = true;
  robotState = READY;

  // Both LEDs on = ready
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);

  Serial.println(F(""));
  Serial.println(F("Ready! Press RB to start driving."));
}

// ─── LINE ERROR COMPUTATION ───────────────────────────────────

/*
 * Weighted centroid error on range [-7.5 … +7.5].
 *  > 0 → line is to the right of centre → turn right
 *  < 0 → line is to the left  of centre → turn left
 *
 * Uses per-sensor threshold from calibration.
 * Falls back to last error if no sensor sees the line.
 */
float computeError() {
  float weightedSum = 0.0f;
  float totalWeight = 0.0f;

  for (int i = 0; i < 16; i++) {
    int v = rawValues[i];

#if !BLACK_LINE_ON_WHITE
    v = 1023 - v;          // invert for white-on-black tracks
#endif

    // Weight = how far above threshold (0 if not on line)
    int threshold = calibrated ? calMid[i] : 500;
    float weight  = (v > threshold) ? (float)(v - threshold) : 0.0f;

    // Sensor 0 = rightmost (+7.5), sensor 15 = leftmost (-7.5)
    float position = 7.5f - (float)i;

    weightedSum += weight * position;
    totalWeight += weight;
  }

  if (totalWeight < 1.0f) {
    return errorPrev;      // lost line → keep last direction
  }

  return weightedSum / totalWeight;
}

// ─── PID CORRECTION ──────────────────────────────────────────

int computeCorrection(float error) {
  float derivative  = error - errorPrev;
  errorIntegral    += error;
  errorIntegral     = constrain(errorIntegral, -5000.0f, 5000.0f);
  errorPrev         = error;

  float c = (KP * error) + (KI * errorIntegral) + (KD * derivative);
  return (int)constrain(c * (float)BASE_SPEED, -255.0f, 255.0f);
}

// ─── SETUP ───────────────────────────────────────────────────

void setup() {
  Serial.begin(115200);
  Serial.println(F("TechGeeks Line Follower — v0.2"));
  Serial.println(F("-------------------------------"));
  Serial.println(F("LB = Calibrate   |   RB = Start / Stop"));
  Serial.println(F("Press LB to begin calibration."));

  robot.begin();
  robot.setPID(KP, KI, KD);
  robot.stop();

  sensors.begin(select, A4, A5);

  ledAll(false);
  robotState = IDLE;
}

// ─── MAIN LOOP ────────────────────────────────────────────────

void loop() {

  // ── LB — Calibrate (any state except mid-calibration) ─────
  if (robotState != CALIBRATING && buttonPressed(LB)) {
    robot.stop();
    ledAll(false);
    errorPrev     = 0.0f;
    errorIntegral = 0.0f;
    startCalibration();          // blocks for CAL_DURATION_MS, then returns READY
    return;
  }

  // ── RB — Start / Stop ──────────────────────────────────────
  if (buttonPressed(RB)) {
    if (robotState == RUNNING) {
      robot.stop();
      ledAll(false);
      robotState = STOPPED;
      Serial.println(F(">>> Stopped. Press LB to recalibrate, RB to resume."));
    } else if (robotState == READY || robotState == STOPPED) {
      if (!calibrated) {
        Serial.println(F("Not calibrated yet! Press LB first."));
        return;
      }
      errorPrev     = 0.0f;
      errorIntegral = 0.0f;
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
      robotState = RUNNING;
      Serial.println(F(">>> Running! Press RB to stop."));
    } else {
      // IDLE — nudge user
      Serial.println(F("Calibrate first! Press LB."));
    }
    return;
  }

  // ── State actions ──────────────────────────────────────────

  switch (robotState) {

    case IDLE:
      blinkLED1(600);              // slow blink = waiting for calibration
      break;

    case CALIBRATING:
      break;                       // handled inside startCalibration()

    case READY:
    case STOPPED:
      // Both LEDs on = ready / stopped
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, HIGH);
      break;

    case RUNNING: {
      // 1. Read sensors
      sensors.read(rawValues);

      // 2. Compute error & correction
      float error      = computeError();
      int   correction = computeCorrection(error);

      // 3. Drive
      int leftSpeed  = BASE_SPEED + correction;
      int rightSpeed = BASE_SPEED - correction;
      robot.drive(leftSpeed, rightSpeed);

      // 4. Debug (uncomment during tuning)
      /*
      Serial.print(F("err=")); Serial.print(error, 2);
      Serial.print(F("  corr=")); Serial.print(correction);
      Serial.print(F("  L=")); Serial.print(leftSpeed);
      Serial.print(F("  R=")); Serial.println(rightSpeed);
      */
      break;
    }
  }
}
