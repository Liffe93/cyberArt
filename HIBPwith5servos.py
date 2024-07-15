import json
import requests
import time
from pyfirmata import Arduino, SERVO

# Connect to Arduino (replace with your actual port)
board = Arduino('/dev/cu.usbmodem14101')

# Define servo pins (replace with your actual pin numbers for each servo)
#servos = (board.digital[pin] for pin in range(9, 12))  # Assuming 10 servos on pins 9 to 18
servo1 = board.digital[9]
servo2 = board.digital[10]
servo3 = board.digital[11]
servo4 = board.digital[12]


# Set all servos to SERVO mode
#for servo in servos:
 #   servo.mode = SERVO
servo1.mode = SERVO
servo2.mode = SERVO
servo3.mode = SERVO
servo4.mode = SERVO

#SET SERVOS TO neutral position 
servo1.write(90)
servo2.write(90)
servo3.write(90)
servo4.write(90)

# Define a function to set multiple servos simultaneously (optional)
def set_servo_angles(angles):
    """
    Sets the angles of multiple servos simultaneously.

    Args:
        angles (list): A list of angles (0-180) corresponding to each servo.
                       The number of angles must match the number of servos.
    """

    if len(angles) != len([servo1, servo2, servo3, servo4]):
        raise ValueError("Number of angles must match the number of servos")

    for i, angle in enumerate(angles):
        [servo1, servo2, servo3, servo4][i].write(angle)  # Access servos by index

def check_hibp(email):
    """
    This function checks if an email has been exposed in breaches using HIBP API.

    **Important:** This script demonstrates data retrieval only. You'll need
    separate Arduino code to communicate (potentially via serial or a web server).

    Args:
        email: The email address to check.

    Returns:
        The number of breaches the email was found in, or None if the API request fails.
    """

    # Replace with your actual HIBP API key (don't share this publicly!)
    api_key = "XXXX"
    headers = {"hibp-api-key": api_key}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Parse the JSON response
        try:
            data = json.loads(response.text)
            num_breaches = len(data)
            return num_breaches
        except json.JSONDecodeError:
            print("Error: Failed to parse HIBP API response as JSON.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HIBP API request failed: {e}")
        return None

# Get email input from the user
email = input("Enter email address: ")

# Check HIBP for breaches
num_breaches = check_hibp(email)

if num_breaches is not None:
    # Map number of breaches to servo angles (adjust mapping as needed)
    # This is a logarithmic mapping (more breaches = more servos activated)
    servo_angles = [90] * len([servo1, servo2, servo3, servo4])  # Initialize all servos to 0 degrees
    breach_thresholds = [1, 10, 50, 100]  # Thresholds for activating servos

    for i, threshold in enumerate(breach_thresholds):
        if num_breaches >= threshold:
            servo_angles[i] = 180  # Set activated servos to 180 degrees (adjust as needed)

    # Move the servos (optional function usage)
    set_servo_angles(servo_angles)

    print(f"Email '{email}' found in {num_breaches} breaches. Servos moved to: {servo_angles}")

    # Optional: delay and clean up (close connection)
    time.sleep(20)
    for servo in [servo1, servo2, servo3, servo4]:  # Use list comprehension for brevity
        servo.write(90)  # Set all servos to neutral position (optional)

else:
    print("HIBP API request failed.")
