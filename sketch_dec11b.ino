/*
 * This Arduino Sketch reads temperature data from an Adafruit MAX31865 RTD Sensor
 * Breakout connected to an ESP32-C3 microcontroller via SPI. The temperature data
 * is then printed to the Serial Monitor.
 */

#include <SPI.h>
#include <Adafruit_MAX31865.h>

// Define the pins for the SPI interface
#define MAX31865_CS 2
#define MAX31865_MOSI 10
#define MAX31865_MISO 9
#define MAX31865_SCK 8

// Create an instance of the Adafruit_MAX31865 class
Adafruit_MAX31865 max31865 = Adafruit_MAX31865(MAX31865_CS,MAX31865_MOSI,MAX31865_MISO,MAX31865_SCK);

void setup() {
  // Initialize Serial communication
  Serial.begin(115200);
  while (!Serial) delay(10); // Wait for Serial to be ready

  // Initialize the MAX31865 sensor
  if (!max31865.begin(MAX31865_3WIRE)) {
    Serial.println("Failed to initialize MAX31865 sensor!");
    while (1) delay(10);
  }
}

void loop() {
  // Read the temperature from the MAX31865 sensor
  float temperature = max31865.temperature(100, 430);

  // Print the temperature to the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // Wait for 1 second before reading again
  delay(1000);
}
