import cv2
import requests
import serial

# Initialize the serial connection to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600) # Adjust the port as necessary

# Initialize the camera
camera = cv2.VideoCapture(0)

def capture_image():
    ret, frame = camera.read()
    if ret:
        image_path = 'face.jpg'
        cv2.imwrite(image_path, frame)
        return image_path
    else:
        raise Exception("Failed to capture image")

def send_image_to_server(image_path):
    url = "https://government-facial-recognition-api.com/submit" # Placeholder URL
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()['matches']
    else:
        raise Exception("Failed to get response from server")

def main():
    try:
        image_path = capture_image()
        matches = send_image_to_server(image_path)
        if 0 <= matches <= 10:
            ser.write(str(matches).encode())
        else:
            print("Invalid number of matches received")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
