/*
 * ============================================================
 *  Line Follower Firmware — TechGeeks ARC16 + Blueprint 01
 * ============================================================
 *  Hardware:
 *    - Blueprint 01 Robot Controller Board (Arduino Nano + TB6612FNG)
 *    - ARC16 16-Channel IR Sensor Array (MUX architecture)
 *
 *  Libraries required (install before compiling):
 *    - ARC16   : https://github.com/Techgeeks-store/ARC16-Sensor-Library
 *    - RCBoard : https://github.com/Techgeeks-store/Blueprint01-Robot-Controller-Board
 *
 *  Wiring (ARC16 → Arduino Nano via Blueprint01 sensor rail):
 *    S0 → A0  |  S1 → A1  |  S2 → A2  |  S3 → A3
 *    E  → A4  |  SIG → A5
 *    VCC → 5V |  GND → GND
 *
 *  Usage:
 *    - Press LEFT button  (LB) to start the robot.
 *    - Press RIGHT button (RB) to stop / emergency brake.
 *    - LED1 blinks while idle, stays solid when running.
 *    - Open Serial Monitor at 115200 for live debug output.
 *
 *  Phase progression (commit a git tag after each phase works):
 *    v0.1 — calibration + raw sensor print
 *    v0.2 — P-only control, basic driving
 *    v0.3 — PD control, smoother corners
 *    v1.0 — full PID, tuned for competition speed
 *
 * ============================================================
 */

#include <ARC16.h>
#include <RCBoard.h>

// ─── USER CONFIGURATION ─────────────────────────────────────

// Line polarity
//   true  → black line on white surface (standard)
//   false → white line on black surface (inverted)
#define BLACK_LINE_ON_WHITE  true

// Base drive speed: 0–255
//   Start around 120 for Phase 1; raise to 200+ for competition.
#define BASE_SPEED  130

// PID gains — tune these!
//   Start with Kp only. Zero out Ki and Kd first.
//   Phase 2: Kp = 0.03,  Ki = 0.0, Kd = 0.0
//   Phase 3: Kp = 0.03,  Ki = 0.0, Kd = 0.8
//   Phase 4: Kp = 0.06,  Ki = 0.0001, Kd = 1.5  (tweak to suit your track)
#define KP  0.03
#define KI  0.0
#define KD  0.0

// Sensor thresholds: values above this are treated as "on the line".
// Calibrate using the CALIBRATE_MODE below, then update this.
// ARC16 reading: HIGH (≈900) = dark/black | LOW (≈100) = light/white
#define LINE_THRESHOLD  500

// Enable calibration mode (reads sensors for 5 s on startup, then saves min/max).
// Set to false for normal driving after first calibration run.
#define CALIBRATE_ON_BOOT  true

// ─── END USER CONFIGURATION ─────────────────────────────────


// ─── OBJECTS ────────────────────────────────────────────────

ARC16   sensors;
RCBoard robot;

int  select[4]   = {A0, A1, A2, A3};   // MUX select lines (S0..S3)
int  rawValues[16];                     // raw ADC readings per sensor
int  calMin[16];                        // calibration minimums
int  calMax[16];                        // calibration maximums
bool calibrated  = false;

// PID state
float errorPrev     = 0.0;
float errorIntegral = 0.0;

// Robot state machine
enum State { IDLE, RUNNING };
State robotState = IDLE;

// ─── HELPERS ────────────────────────────────────────────────

/** Blink LED1 non-blockingly (call every loop). */
void blinkIdle() {
  static unsigned long last = 0;
  static bool ledOn = false;
  if (millis() - last > 400) {
    last = millis();
    ledOn = !ledOn;
    digitalWrite(LED1, ledOn ? HIGH : LOW);
  }
}

/**
 * Compute a weighted centroid error from [-7.5 … +7.5].
 * Positive → line is to the right; negative → line is to the left.
 * Returns the last known error when no sensor sees the line
 * (robot went off-track), so it keeps trying to turn back.
 */
float computeError() {
  float weightedSum = 0.0;
  float totalWeight = 0.0;

  for (int i = 0; i < 16; i++) {
    // Normalise to 0–1023 regardless of polarity
    int v = rawValues[i];

#if BLACK_LINE_ON_WHITE
    // High ADC = dark = on the line → use as-is
#else
    // Low ADC = dark = on the line → invert
    v = 1023 - v;
#endif

    // Only count sensors above threshold
    float weight = (v > LINE_THRESHOLD) ? (float)v : 0.0f;

    // Sensor 0 is rightmost, sensor 15 is leftmost.
    // Map to position: 0 → +7.5, 15 → -7.5
    float position = 7.5f - (float)i;   // 7.5, 6.5, … -6.5, -7.5

    weightedSum += weight * position;
    totalWeight += weight;
  }

  if (totalWeight < 1.0f) {
    // No line detected — keep using last error (sign tells direction)
    return errorPrev;
  }

  return weightedSum / totalWeight;
}

/** PD/PID correction value. */
int computeCorrection(float error) {
  float derivative = error - errorPrev;
  errorIntegral   += error;
  errorPrev        = error;

  // Clamp integral to prevent wind-up
  errorIntegral = constrain(errorIntegral, -5000.0f, 5000.0f);

  float correction = (KP * error) + (KI * errorIntegral) + (KD * derivative);

  return (int)constrain(correction * BASE_SPEED, -255.0f, 255.0f);
}

/** Calibrate: swing robot left and right by hand for 5 seconds. */
void runCalibration() {
  Serial.println(F("=== CALIBRATION MODE ==="));
  Serial.println(F("Slowly sweep sensor over the track for 5 seconds..."));

  // Initialise min/max arrays
  sensors.read(rawValues);
  for (int i = 0; i < 16; i++) {
    calMin[i] = rawValues[i];
    calMax[i] = rawValues[i];
  }

  digitalWrite(LED1, HIGH);
  unsigned long start = millis();

  while (millis() - start < 5000) {
    sensors.read(rawValues);
    for (int i = 0; i < 16; i++) {
      if (rawValues[i] < calMin[i]) calMin[i] = rawValues[i];
      if (rawValues[i] > calMax[i]) calMax[i] = rawValues[i];
    }
    delay(10);
  }

  digitalWrite(LED1, LOW);
  Serial.println(F("Calibration done. Min/Max per sensor:"));
  for (int i = 0; i < 16; i++) {
    Serial.print(F("S")); Serial.print(i);
    Serial.print(F("  min=")); Serial.print(calMin[i]);
    Serial.print(F("  max=")); Serial.println(calMax[i]);
  }
  Serial.println(F("Update LINE_THRESHOLD based on these values."));
  Serial.println(F("Press LB to start driving."));

  calibrated = true;
}

// ─── SETUP ──────────────────────────────────────────────────

void setup() {
  Serial.begin(115200);
  Serial.println(F("TechGeeks Line Follower — starting up"));

  // Initialise controller board (sets up motor driver STDBY, pins, etc.)
  robot.begin();
  robot.stop();

  // Set PID gains
  robot.setPID(KP, KI, KD);

  // Initialise ARC16 sensor array
  sensors.begin(select, A4, A5);

  Serial.println(F("Hardware initialised."));

  if (CALIBRATE_ON_BOOT) {
    runCalibration();
  } else {
    Serial.println(F("Calibration skipped. Press LB to start."));
    calibrated = true;
  }
}

// ─── MAIN LOOP ──────────────────────────────────────────────

void loop() {

  // ── Button handling ──────────────────────────────────────
  if (digitalRead(LB) == LOW) {           // LB = start
    delay(50);                            // debounce
    if (digitalRead(LB) == LOW && calibrated) {
      robotState    = RUNNING;
      errorPrev     = 0.0;
      errorIntegral = 0.0;
      digitalWrite(LED1, HIGH);
      Serial.println(F(">>> Running <<<"));
      delay(200);
    }
  }

  if (digitalRead(RB) == LOW) {           // RB = stop
    delay(50);
    if (digitalRead(RB) == LOW) {
      robotState = IDLE;
      robot.stop();
      digitalWrite(LED1, LOW);
      Serial.println(F(">>> Stopped <<<"));
      delay(200);
    }
  }

  // ── Idle ─────────────────────────────────────────────────
  if (robotState == IDLE) {
    blinkIdle();
    return;
  }

  // ── Running ──────────────────────────────────────────────

  // 1. Read all 16 sensors (~1.7 ms)
  sensors.read(rawValues);

  // 2. Compute line error
  float error      = computeError();

  // 3. Compute PID correction
  int correction   = computeCorrection(error);

  // 4. Mix into left / right motor speeds
  //    Positive correction → line is to the right → turn right (reduce right, boost left)
  int leftSpeed    = BASE_SPEED + correction;
  int rightSpeed   = BASE_SPEED - correction;

  // 5. Drive
  robot.drive(leftSpeed, rightSpeed);

  // 6. Debug output (comment out for full speed — Serial.print takes time!)
  // Uncomment the block below during tuning:
  /*
  Serial.print(F("err=")); Serial.print(error, 2);
  Serial.print(F("  corr=")); Serial.print(correction);
  Serial.print(F("  L=")); Serial.print(leftSpeed);
  Serial.print(F("  R=")); Serial.println(rightSpeed);
  */
}
