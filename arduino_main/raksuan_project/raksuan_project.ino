#define BUZZER 9
#define FLAME_SENSOR A0
#define GAS_SENSOR A1
#define ULTRA_SONIC_TRIG 11
#define ULTRA_SONIC_ECHO 10
#define WATER_LED_MID 13
#define WATER_LED_HIGH 12
#define VIBRATION_SENSOR A2

void setup() {
  pinMode(BUZZER, OUTPUT);
  pinMode(FLAME_SENSOR, INPUT);
  pinMode(GAS_SENSOR, INPUT);
  pinMode(WATER_LED_MID, OUTPUT);
  pinMode(WATER_LED_HIGH, OUTPUT);
  pinMode(VIBRATION_SENSOR, INPUT);
  
  pinMode(ULTRA_SONIC_TRIG, OUTPUT);
  pinMode(ULTRA_SONIC_ECHO, INPUT);
  Serial.begin(9600); // For debugging purposes
}

void loop() {
  long duration;
  int distance;

  // Send a 10 microsecond pulse to the trigger pin
  digitalWrite(ULTRA_SONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRA_SONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRA_SONIC_TRIG, LOW);

  // Read the echo pin and calculate the distance
  duration = pulseIn(ULTRA_SONIC_ECHO, HIGH);
  distance = duration * 0.034 / 2; // Convert to centimeters

  // Read gas, flame, and vibration sensor values
  int gasValue = analogRead(GAS_SENSOR);
  int flameValue = analogRead(FLAME_SENSOR);
  int vibrationValue = analogRead(VIBRATION_SENSOR);

  // Initialize flags for logging
  bool waterMid = false;
  bool waterHigh = false;
  bool gasDetected = false;
  bool fireDetected = false;
  bool vibrationDetected = false;

  // Check for high water level
  // Serial.println(distance);
  if (distance <= 15) {
    digitalWrite(WATER_LED_HIGH, HIGH);
    digitalWrite(WATER_LED_MID, LOW);
    waterHigh = true;
  } else if (distance <= 18) {
    digitalWrite(WATER_LED_HIGH, LOW);
    digitalWrite(WATER_LED_MID, HIGH);
    waterMid = true;
  } else {
    digitalWrite(WATER_LED_HIGH, LOW);
    digitalWrite(WATER_LED_MID, LOW);
  }

  // Check gas detection
  if (gasValue > 100) { // Adjust threshold as needed
    gasDetected = true;
  }

  // Check flame detection
  if (flameValue < 300) { // Adjust threshold as needed
    fireDetected = true;
  }

  // Check vibration detection
  if (vibrationValue > 200) { // Adjust threshold as needed
    vibrationDetected = true;
  }

  // Update buzzer state
  if (waterHigh || gasDetected || fireDetected || vibrationDetected) {
    digitalWrite(BUZZER, HIGH);
  } else {
    digitalWrite(BUZZER, LOW);
  }

  // Print messages to Serial Monitor based on flags
  if (waterMid) {
    Serial.println("Water level mid!");
  }
  if (waterHigh) {
    Serial.println("Water level high!");
  }
  if (gasDetected) {
    Serial.println("Gas detected!");
  }
  if (fireDetected) {
    Serial.println("Fire detected!");
  }
  if (vibrationDetected) {
    Serial.println("Vibration detected!");
  }

  delay(1000); // Wait for 1 second before the next measurement
}
