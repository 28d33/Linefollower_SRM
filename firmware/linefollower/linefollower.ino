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
 *    RB (D10) — Start/Stop
 *
 *  LED feedback:
 *    LED1 slow blink           → waiting for calibration
 *    LED1 fast blink           → calibrating
 *    LED1 + LED2 on            → calibrated, ready
 *    LED1 solid                → tracking line (PID)
 *    LED1 solid + LED2 blink   → recovery: searching for line
 *    Both fast blink           → LOOP DETECTED — breaking out
 *    Both off                  → stopped
 *
 *  Serial: 115200 baud
 *  Git tags: v0.1 skeleton | v0.2 auto-cal | v0.3 right-first + loop guard
 * ============================================================
 */

#include <ARC16.h>
#include <RCBoard.h>

// ─── USER CONFIGURATION ─────────────────────────────────────

// Line polarity
//   true  → black line on white surface (standard)
//   false → white line on black surface (inverted)
#define BLACK_LINE_ON_WHITE  true

// Super-High Speed Competition Mode (BASE_SPEED = 450)
#define BASE_SPEED    450
#define CORNER_SPEED  210   // Reduced corner speed for extreme <30 deg acute turns

// Aggressive Instant-Response PD gains for BASE_SPEED = 450:
//   KP = 0.35  (instant aggressive steering response at small error deviations)
//   KD = 1.25  (strong derivative damping to eliminate high-speed oscillation)
//   KI = 0.00  (no integral delay)
#define KP  0.35
#define KI  0.0
#define KD  1.25

// ── Lost-line recovery timings (ms) ──────────────────────────
//   [0 .. COAST_MS)          coast — keep last error, don't overcorrect
//   [COAST_MS .. +SEARCH_R)  hard RIGHT turn (right-first priority)
//   [+SEARCH_R .. +SEARCH_L) hard LEFT turn  (second attempt)
#define COAST_MS    150   // ms to coast at high speed before searching
#define SEARCH_R_MS 500   // ms to search right
#define SEARCH_L_MS 500   // ms to search left

// ── Loop / spin detection ─────────────────────────────────────
// If |error| > LOOP_ERR_THRESH AND sign doesn't change for LOOP_TIME_MS
// → robot is going in circles → execute a loop-break maneuver.
#define LOOP_ERR_THRESH  5.5f   // near-max error (range is ±7.5)
#define LOOP_TIME_MS     2000   // ms of sustained high-magnitude same-sign error
#define LOOP_BREAK_MS    500    // how long to spin opposite during break

// Calibration duration
#define CAL_DURATION_MS  5000

// ─── OBJECTS ────────────────────────────────────────────────
ARC16   sensors;
RCBoard robot;

int select[4] = {A0, A1, A2, A3};
int rawValues[16];

// Calibration
int  calMin[16], calMax[16], calMid[16];
bool calibrated = false;

// ─── STATE MACHINE ───────────────────────────────────────────
enum State { IDLE, CALIBRATING, READY, RUNNING, STOPPED };
State robotState = IDLE;

// ─── PID STATE ───────────────────────────────────────────────
float errorPrev     = 0.0f;
float errorIntegral = 0.0f;

// ─── LOST-LINE RECOVERY STATE ────────────────────────────────
bool          lineVisible  = false;
unsigned long lostSince    = 0;

// ─── LOOP DETECTION STATE ────────────────────────────────────
int           loopErrorSign  = 0;    // +1 / -1
unsigned long loopSignSince  = 0;    // when that sign started

// ─── LED HELPERS ─────────────────────────────────────────────
void ledSet(bool l1, bool l2) {
  digitalWrite(LED1, l1 ? HIGH : LOW);
  digitalWrite(LED2, l2 ? HIGH : LOW);
}

void blinkLED1(unsigned long period) {
  static unsigned long last = 0;
  static bool on = false;
  if (millis() - last >= period) { last = millis(); on = !on; digitalWrite(LED1, on); }
}

void blinkBoth(unsigned long period) {
  static unsigned long last = 0;
  static bool on = false;
  if (millis() - last >= period) { last = millis(); on = !on; ledSet(on, on); }
}

void blinkLED2(unsigned long period) {
  static unsigned long last = 0;
  static bool on = false;
  if (millis() - last >= period) { last = millis(); on = !on; digitalWrite(LED2, on); }
}

// ─── BUTTON HELPER ───────────────────────────────────────────
bool buttonPressed(uint8_t pin) {
  if (digitalRead(pin) == LOW) {
    delay(40);
    if (digitalRead(pin) == LOW) {
      while (digitalRead(pin) == LOW);
      return true;
    }
  }
  return false;
}

// ─── CALIBRATION ─────────────────────────────────────────────
void startCalibration() {
  Serial.println(F("\n=== AUTO-CALIBRATION ==="));
  Serial.print(F("Sweep sensor across full track for "));
  Serial.print(CAL_DURATION_MS / 1000); Serial.println(F("s. Go!"));

  sensors.read(rawValues);
  for (int i = 0; i < 16; i++) { calMin[i] = rawValues[i]; calMax[i] = rawValues[i]; }

  robotState = CALIBRATING;
  unsigned long start = millis();
  unsigned long lastPrint = 0;

  while (millis() - start < CAL_DURATION_MS) {
    blinkLED1(100);
    sensors.read(rawValues);
    for (int i = 0; i < 16; i++) {
      if (rawValues[i] < calMin[i]) calMin[i] = rawValues[i];
      if (rawValues[i] > calMax[i]) calMax[i] = rawValues[i];
    }
    if (millis() - lastPrint > 500) {
      lastPrint = millis();
      Serial.print((millis() - start) * 100 / CAL_DURATION_MS);
      Serial.println(F("%..."));
    }
  }

  Serial.println(F("\n Idx | min | max | threshold"));
  Serial.println(F("-----|-----|-----|----------"));
  for (int i = 0; i < 16; i++) {
    calMid[i] = (calMin[i] + calMax[i]) / 2;
    Serial.print(F("  S")); if (i < 10) Serial.print(' ');
    Serial.print(i);
    Serial.print(F(" | ")); Serial.print(calMin[i]);
    Serial.print(F(" | ")); Serial.print(calMax[i]);
    Serial.print(F(" | ")); Serial.println(calMid[i]);
  }

  calibrated = true;
  robotState = READY;
  ledSet(true, true);
  Serial.println(F("\nReady! Press RB to start."));
}

// ─── RESET PID & RECOVERY STATE ──────────────────────────────
void resetDriveState() {
  errorPrev      = 0.0f;
  errorIntegral  = 0.0f;
  lineVisible    = false;
  lostSince      = 0;
  loopErrorSign  = 0;
  loopSignSince  = millis();
}

// ─── SENSOR WEIGHT FOR ONE CHANNEL ───────────────────────────
// Returns how strongly this sensor sees the line (0 if not on line).
float sensorWeight(int idx) {
  int v = rawValues[idx];
#if !BLACK_LINE_ON_WHITE
  v = 1023 - v;
#endif
  int threshold = calibrated ? calMid[idx] : 500;
  return (v > threshold) ? (float)(v - threshold) : 0.0f;
}

// ─── LINE ERROR + RECOVERY LOGIC ─────────────────────────────
/*
 *  Returns error in [-7.5 .. +7.5]:
 *    > 0  → line is RIGHT of centre → turn right
 *    < 0  → line is LEFT  of centre → turn left
 *
 *  When line is lost:
 *    0 .. COAST_MS       : coast with last error
 *    COAST_MS .. +SEARCH_R_MS : hard RIGHT (+7.5)  ← right-first priority
 *    +SEARCH_R_MS .. +SEARCH_L_MS : hard LEFT (-7.5)
 *    alternates R/L after that
 */
float computeError() {
  float weightedSum = 0.0f;
  float totalWeight = 0.0f;

  for (int i = 0; i < 16; i++) {
    float w = sensorWeight(i);
    // Sensor 0 = rightmost (+7.5), sensor 15 = leftmost (-7.5)
    float position = 7.5f - (float)i;
    weightedSum += w * position;
    totalWeight += w;
  }

  if (totalWeight < 1.0f) {
    // ── LINE LOST ──────────────────────────────────────────
    if (lineVisible) {
      // Just lost it
      lostSince   = millis();
      lineVisible = false;
      Serial.println(F("[LOST] Line lost — searching..."));
    }

    unsigned long lost = millis() - lostSince;

    // ACUTE TURN ZERO-COAST: If line was lost near edge (|errorPrev| >= 4.0),
    // skip coasting entirely (0ms delay) and tank-spin immediately!
    unsigned long effectiveCoast = (fabs(errorPrev) >= 4.0f) ? 0 : COAST_MS;

    if (lost < effectiveCoast) {
      // Stage 1: coast — preserve momentum with last known error
      return errorPrev;
    }

    // Stage 2+: active search, alternating R → L → R → L
    unsigned long searchPhase = (lost - effectiveCoast) % (SEARCH_R_MS + SEARCH_L_MS);
    if (searchPhase < SEARCH_R_MS) {
      // RIGHT FIRST
      return 7.5f;
    } else {
      // then LEFT
      return -7.5f;
    }

  } else {
    // ── LINE FOUND ─────────────────────────────────────────
    if (!lineVisible) {
      lineVisible = true;
      Serial.println(F("[FOUND] Line re-acquired."));
    }

    return weightedSum / totalWeight;
  }
}

// ─── PID CORRECTION + EXTREME ACUTE (<30 DEG) TANK-SPIN ─────────
int computeCorrection(float error, int baseSpd) {
  float derivative  = error - errorPrev;
  errorIntegral    += error;
  errorIntegral     = constrain(errorIntegral, -5000.0f, 5000.0f);
  errorPrev         = error;

  // EXTREME ACUTE HAIRPIN (<30 DEG) TRIGGER:
  // When error is extreme (|error| >= 5.0), force 100% MAXIMUM TANK SPIN (+255 / -255)
  // Outer motor = +255 Full Forward, Inner motor = -255 Full Reverse!
  if (fabs(error) >= 5.0f) {
    int maxTankCorrection = 500;  // Forces left = +255, right = -255
    return (error > 0.0f) ? maxTankCorrection : -maxTankCorrection;
  }

  float c = (KP * error) + (KI * errorIntegral) + (KD * derivative);
  return (int)constrain(c * (float)baseSpd, -255.0f, 255.0f);
}

// ─── OVERRUN TIMING (0.75 SECONDS BEFORE STOP) ────────────────
// When no track is found, continue driving for 750 ms (0.75 s).
// If track is still not found after 750 ms → IMMEDIATE HARD STOP.
// If track is re-found within 750 ms → resume line following seamlessly.
#define OVERRUN_STOP_MS  750   // 0.75 seconds (750 ms)

// ─── SAME / SIMILAR POLARITY DETECTION & STOP ────────────────
/*
 *  Checks if all (or nearly all) 16 sensors detect the SAME surface/polarity:
 *   1. All-Black (Stop bar / Finish line): >= 13 sensors active
 *   2. All-White / Off-Track             : <= 1 sensor active for > 1000 ms (1 full second)
 *   3. Low Contrast / Uniform Surface    : max - min < 120 ADC units for > 1000 ms
 *
 *  If no track is found for 1 full second (1000ms), the robot STOPS immediately.
 */
void checkPolarityAndLoop(float error) {
  int activeCount = 0;
  int minVal = 1023;
  int maxVal = 0;

  for (int i = 0; i < 16; i++) {
    int v = rawValues[i];
    if (v < minVal) minVal = v;
    if (v > maxVal) maxVal = v;

    float w = sensorWeight(i);
    if (w > 0.0f) activeCount++;
  }

  int contrast = maxVal - minVal;

  // 1. ALL BLACK (Stop bar / Finish line) — continue 1s, then stop
  static unsigned long allBlackStart = 0;
  if (activeCount >= 13) {
    if (allBlackStart == 0) allBlackStart = millis();
    else if (millis() - allBlackStart >= OVERRUN_STOP_MS) {
      Serial.print(F("[STOP] Finish line / All-Black (1s elapsed) — STOPPED!"));
      robot.stop();
      ledSet(false, false);
      robotState = STOPPED;
      allBlackStart = 0;
      return;
    }
  } else {
    allBlackStart = 0;
  }

  // 2. ALL WHITE / NO TRACK (Line lost for 1 full second)
  static unsigned long noTrackStart = 0;
  if (activeCount <= 1 || !lineVisible) {
    if (noTrackStart == 0) noTrackStart = millis();
    else if (millis() - noTrackStart >= OVERRUN_STOP_MS) {
      Serial.println(F("[STOP] No track found for 1 full second — IMMEDIATE STOP!"));
      robot.stop();
      ledSet(false, false);
      robotState = STOPPED;
      noTrackStart = 0;
      return;
    }
  } else {
    noTrackStart = 0;
  }

  // 3. LOW CONTRAST / UNIFORM SURFACE (Same/Similar reading across all sensors for 1s)
  static unsigned long lowContrastStart = 0;
  if (contrast < 120) {
    if (lowContrastStart == 0) lowContrastStart = millis();
    else if (millis() - lowContrastStart >= OVERRUN_STOP_MS) {
      Serial.print(F("[STOP] Uniform surface / Low contrast for 1s — STOPPED!"));
      robot.stop();
      ledSet(false, false);
      robotState = STOPPED;
      lowContrastStart = 0;
      return;
    }
  } else {
    lowContrastStart = 0;
  }

  // 4. CONTINUOUS SAME-SIDE ERROR (Circling / Looping)
  int sign = 0;
  if      (error >  LOOP_ERR_THRESH) sign = +1;
  else if (error < -LOOP_ERR_THRESH) sign = -1;

  if (sign == 0 || sign != loopErrorSign) {
    loopErrorSign = sign;
    loopSignSince = millis();
    return;
  }

  if (millis() - loopSignSince > LOOP_TIME_MS) {
    Serial.print(F("[LOOP STOP] Sustained same-side turn detected (Error="));
    Serial.print(error, 2);
    Serial.println(F(") — STOPPED!"));
    robot.stop();
    ledSet(false, false);
    robotState = STOPPED;
  }
}

// ─── SETUP ───────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial.println(F("TechGeeks Line Follower — v0.3"));
  Serial.println(F("  LB = Calibrate  |  RB = Start/Stop"));
  Serial.println(F("  Right-first recovery + loop guard active."));
  Serial.println(F("Press LB to calibrate."));

  robot.begin();
  robot.setPID(KP, KI, KD);
  robot.stop();
  sensors.begin(select, A4, A5);
  ledSet(false, false);
}

// ─── MAIN LOOP ────────────────────────────────────────────────
void loop() {

  // ── LB → Calibrate ────────────────────────────────────────
  if (robotState != CALIBRATING && buttonPressed(LB)) {
    robot.stop();
    ledSet(false, false);
    resetDriveState();
    startCalibration();
    return;
  }

  // ── RB → Start / Stop ─────────────────────────────────────
  if (buttonPressed(RB)) {
    if (robotState == RUNNING) {
      robot.stop();
      ledSet(false, false);
      robotState = STOPPED;
      Serial.println(F(">>> Stopped. RB to resume, LB to recalibrate."));
    } else if (robotState == READY || robotState == STOPPED) {
      if (!calibrated) { Serial.println(F("Calibrate first (LB)!")); return; }
      resetDriveState();
      ledSet(true, false);
      robotState = RUNNING;
      Serial.println(F(">>> Running!"));
    } else {
      Serial.println(F("Press LB to calibrate first."));
    }
    return;
  }

  // ── State actions ─────────────────────────────────────────
  switch (robotState) {

    case IDLE:
      blinkLED1(600);
      break;

    case CALIBRATING:
      break;

    case READY:
    case STOPPED:
      ledSet(true, true);
      break;

    case RUNNING: {

      // ── Normal PID tracking with Corner Speed Scaling ──
      sensors.read(rawValues);

      float error = computeError();

      // Corner Speed Scaling: 250 on straights, 130 on sharp turns (|error| >= 3.0)
      int baseSpd = (fabs(error) >= 3.0f) ? CORNER_SPEED : BASE_SPEED;

      int correction = computeCorrection(error, baseSpd);

      int leftSpeed  = baseSpd + correction;
      int rightSpeed = baseSpd - correction;
      robot.drive(leftSpeed, rightSpeed);

      // LED: solid LED1 while tracking, LED2 blinks during recovery
      digitalWrite(LED1, HIGH);
      if (lineVisible) {
        digitalWrite(LED2, LOW);
      } else {
        blinkLED2(120);
      }

      // Check for same/similar polarity surface or sustained looping
      checkPolarityAndLoop(error);

      // Debug — uncomment during tuning:
      /*
      Serial.print(F("e=")); Serial.print(error, 2);
      Serial.print(F(" c=")); Serial.print(correction);
      Serial.print(F(" L=")); Serial.print(leftSpeed);
      Serial.print(F(" R=")); Serial.println(rightSpeed);
      */
      break;
    }
  }
}
