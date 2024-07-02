#use in arduino 
#define fanPin 9  // PWM pin for fan control

int fanSpeed = 0;  // Variable to store calculated fan speed
int digitalInputPin = 2; // Change this to the actual digital input pin

void setup() {
  pinMode(fanPin, OUTPUT);
  pinMode(digitalInputPin, INPUT);
}

void loop() {
  int digitalInputValue = digitalRead(digitalInputPin);

  // Define voltage thresholds and corresponding fan speeds (adjust based on your setup)
  if (digitalInputValue == LOW) {
    fanSpeed = 0; // Minimum speed (LOW voltage)
  } else if (digitalInputValue == HIGH) {
    fanSpeed = 255; // Maximum speed (HIGH voltage)
  } else {
    // Handle unexpected input values (optional)
    fanSpeed = 127; // Set a default speed (consider adding error handling)
  }

  // Write the fan speed as a PWM signal
  analogWrite(fanPin, fanSpeed);
}
