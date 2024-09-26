import json
import requests
import time
from pyfirmata import Arduino, SERVO

# Connect to Arduino (replace with your actual port)
board = Arduino('/dev/ttyACM0')

# Define servo pins (replace with your actual pin numbers for each servo)
#servos = (board.digital[pin] for pin in range(9, 12))  # Assuming 10 servos on pins 9 to 18
servo1 = board.digital[3]
servo2 = board.digital[5]
servo3 = board.digital[6]

servo4 = board.digital[9]
servo5 = board.digital[10]
servo6 = board.digital[11]



# Set all servos to SERVO mode
#for servo in servos:
 #   servo.mode = SERVO
servo1.mode = SERVO
servo2.mode = SERVO
servo3.mode = SERVO
servo4.mode = SERVO
servo5.mode = SERVO
servo6.mode = SERVO


#SET SERVOS TO neutral position 
servo1.write(90)
servo2.write(90)
servo3.write(90)
servo4.write(90)
servo5.write(90)
servo6.write(90)



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
    api_key = "ENTER YOUR OWN KEY BBS"
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
    if num_breaches <= 10:
        servo1.write(180)
        time.sleep(10)
    elif 11 <= num_breaches <=20:
        servo1.write(180)
        servo2.write(180)
        time.sleep(20)
    elif 21 <= num_breaches <=30:
        servo1.write(180)
        servo2.write(180)
        servo3.write(180)
        time.sleep(20)
    elif 31 <= num_breaches <=40:
        servo1.write(180)
        servo2.write(180)
        servo3.write(180)
        servo4.write(180)
        time.sleep(20)
    elif 41 <= num_breaches <=50:
        servo1.write(180)
        servo2.write(180)
        servo3.write(180)
        servo4.write(180)
        servo5.write(180)
        time.sleep(20)
    elif num_breaches >=51:
        servo1.write(180)
        servo2.write(180)
        servo3.write(180)
        servo4.write(180)
        servo5.write(180)
        servo6.write(180)
        time.sleep(20)




    print(f"Email '{email}' found in {num_breaches} breaches.")

    # Optional: delay and clean up (close connection)
    time.sleep(10)
    for servo in [servo1, servo2, servo3, servo4, servo5, servo6]:  # Use list comprehension for brevity
        servo.write(0)  # Set all servos to neutral position (optional)
    #time.sleep(50)


else:
    print("HIBP API request failed.")
    
