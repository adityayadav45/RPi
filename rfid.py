import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import board
import pwmio
from adafruit_motor import servo

# Setup RFID reader
reader = SimpleMFRC522()

# Setup Servo Motor
SERVO_PIN = 17  # Connect Servo signal wire to GPIO 17
pwm = pwmio.PWMOut(SERVO_PIN, duty_cycle=0, frequency=50)  
servo_motor = servo.Servo(pwm)

# Predefined authorized RFID tags
AUTHORIZED_TAGS = {
    "123456789012": "Tag 1 - Access Granted",
    "987654321098": "Tag 2 - Access Granted"
}

def rotate_servo():
    """Rotates the servo motor 90 degrees and returns after 5 seconds."""
    print("Rotating Servo: 90°")
    servo_motor.angle = 90  # Move to 90°
    time.sleep(5)  # Wait for 5 seconds
    print("Returning Servo to 0°")
    servo_motor.angle = 0  # Return to 0°

try:
    print("Place your RFID tag near the reader...")
    while True:
        id, text = reader.read()
        tag_id = str(id).strip()

        if tag_id in AUTHORIZED_TAGS:
            print(f"{AUTHORIZED_TAGS[tag_id]}")
            rotate_servo()  # Rotate servo if tag is authorized
        else:
            print(f"Access Denied: Unknown Tag {tag_id}")

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    GPIO.cleanup()
