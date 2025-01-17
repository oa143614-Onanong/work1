/*
 * This Arduino Sketch reads temperature data from four Adafruit MAX31865 RTD Sensors
 * Breakout connected to an ESP32-C3 microcontroller via SPI. The temperature data
 * is then printed to the Serial Monitor.
 */

#include <SPI.h>
#include <Adafruit_MAX31865.h>

// Define the pins for the SPI interface
#define MAX31865_CS1 2
#define MAX31865_CS2 3
#define MAX31865_CS3 4
#define MAX31865_CS4 5
#define MAX31865_MOSI 10
#define MAX31865_MISO 9
#define MAX31865_SCK 8

// Create instances of the Adafruit_MAX31865 class for each sensor
Adafruit_MAX31865 max31865_1 = Adafruit_MAX31865(MAX31865_CS1, MAX31865_MOSI, MAX31865_MISO, MAX31865_SCK);
Adafruit_MAX31865 max31865_2 = Adafruit_MAX31865(MAX31865_CS2, MAX31865_MOSI, MAX31865_MISO, MAX31865_SCK);
Adafruit_MAX31865 max31865_3 = Adafruit_MAX31865(MAX31865_CS3, MAX31865_MOSI, MAX31865_MISO, MAX31865_SCK);
Adafruit_MAX31865 max31865_4 = Adafruit_MAX31865(MAX31865_CS4, MAX31865_MOSI, MAX31865_MISO, MAX31865_SCK);

void setup() {
  // Initialize Serial communication
  Serial.begin(115200);
  while (!Serial) delay(10); // Wait for Serial to be ready

  // Initialize the MAX31865 sensors
  if (!max31865_1.begin(MAX31865_3WIRE)) {
    Serial.println("Failed to initialize MAX31865 sensor 1!");
    while (1) delay(10);
  }
  if (!max31865_2.begin(MAX31865_3WIRE)) {
    Serial.println("Failed to initialize MAX31865 sensor 2!");
    while (1) delay(10);
  }
  if (!max31865_3.begin(MAX31865_3WIRE)) {
    Serial.println("Failed to initialize MAX31865 sensor 3!");
    while (1) delay(10);
  }
  if (!max31865_4.begin(MAX31865_3WIRE)) {
    Serial.println("Failed to initialize MAX31865 sensor 4!");
    while (1) delay(10);
  }
}

void loop() {
  // Read the temperature from each MAX31865 sensor
  float temperature1 = max31865_1.temperature(100, 430);
  float temperature2 = max31865_2.temperature(100, 430);
  float temperature3 = max31865_3.temperature(100, 430);
  float temperature4 = max31865_4.temperature(100, 430);

  // Print the temperatures to the Serial Monitor
  Serial.print("Temperature 1: ");
  Serial.print(temperature1);
  Serial.println(" °C");

  Serial.print("Temperature 2: ");
  Serial.print(temperature2);
  Serial.println(" °C");

  Serial.print("Temperature 3: ");
  Serial.print(temperature3);
  Serial.println(" °C");

  Serial.print("Temperature 4: ");
  Serial.print(temperature4);
  Serial.println(" °C");

  // Wait for 1 second before reading again
  delay(1000);
}
