import json
import requests
import time
from pyfirmata import Arduino, SERVO

# Connect to Arduino (replace with your actual port)
board = Arduino('/dev/cu.usbmodem14101')

 # Servo pin (replace with your actual pin number)
servo = board.digital[9]

   # Define servo object
servo.mode = SERVO
#set servo to 0 place
servo.write(0)

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
  api_key = "xxxxx"
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
   
 
  # Map number of breaches to servo angle (adjust mapping as needed)
  # This is a simple example, refine the mapping for desired behavior
  angle = int(num_breaches * 10)  # 10 breaches = 180 degrees

  # Move the servo
  servo.write(angle)
  print(f"Email '{email}' found in {num_breaches} breaches. Servo moved to {angle} degrees.")

  
  # Optional: delay and clean up (close connection)
  time.sleep(10)
  servo.write(0)  # Set servo to neutral position (optional)
  
  
else:
  print("HIBP API request failed.")
