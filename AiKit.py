#include <Arduino.h>
#include "esp_camera.h"  // Include the camera library

// Pin Definitions
#define PIR_PIN 13     // PIR motion sensor pin
#define BUZZER_PIN 12  // Buzzer pin

// Camera Configuration (Adapt these for your ESP32-CAM board)
#define CAMERA_MODEL_AI_THINKER  // ESP32-CAM board type
#include "camera_pins.h"

// Initialize variables
bool motionDetected = false;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.begin(115200);
  
  // Initialize camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // Initialize camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.println("Camera init failed!");
    return;
  }
  Serial.println("Camera initialized!");
}

void loop() {
  motionDetected = digitalRead(PIR_PIN);

  if (motionDetected) {
    Serial.println("Motion Detected!");

    // Activate buzzer
    digitalWrite(BUZZER_PIN, HIGH);
    delay(1000);  // Buzzer on for 1 second
    digitalWrite(BUZZER_PIN, LOW);

    // Capture image
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed!");
      return;
    }

    // Display image capture info
    Serial.printf("Image captured: %d bytes\n", fb->len);
    
    // Free memory buffer
    esp_camera_fb_return(fb);
    
    delay(5000);  // Wait 5 seconds before next motion detection
  }
}
