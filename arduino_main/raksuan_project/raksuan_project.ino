// Vibration
const int LED_PIN = 12;
const int BUZZER_PIN = 7;
const int VIBRATION_SENSOR_PIN = 9;

// Ultrasonic
const unsigned int TRIG_PIN = 4;
const unsigned int ECHO_PIN = 2;
const unsigned int LED_PIN_CLOSE = 3;
const unsigned int LED_PIN_MEDIUM = 6;

void setup() {
  pinMode(VIBRATION_SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT); // Vibration sensor

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN_CLOSE, OUTPUT);
  pinMode(LED_PIN_MEDIUM, OUTPUT); // Ecco
  Serial.begin(9600);
}

void loop() {
  long measurement = vibration();
  delay(50);

  // Vibration Measurement
  if (measurement > 10000 && measurement < 20000) {
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, 370);
    Serial.println("Medium measurement");
  } else if (measurement >= 20000) {
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, 740);
    Serial.println("High measurement");
  } else {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }

  // Ultrasonic Distance Measurement
  long distance = getDistance();

  // LED Indicators based on distance
  if (distance < 14) {
    digitalWrite(LED_PIN_CLOSE, HIGH);
    digitalWrite(LED_PIN_MEDIUM, HIGH);
    Serial.println("Close distance");
  } else if (distance >= 14 && distance <= 16) {
    digitalWrite(LED_PIN_CLOSE, LOW);
    digitalWrite(LED_PIN_MEDIUM, HIGH);
    Serial.println("Medium distance");
  } else {
    digitalWrite(LED_PIN_CLOSE, LOW);
    digitalWrite(LED_PIN_MEDIUM, LOW);
    Serial.println("Far distance");
  }
}

long vibration() {
  return pulseIn(VIBRATION_SENSOR_PIN, HIGH);
}

long getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  return (duration / 2) / 29.1;
}



// Craft By : Vish Siriwatana