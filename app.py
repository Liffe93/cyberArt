from flask import Flask, render_template, request, redirect, url_for, flash
import json
import requests
import time
from pyfirmata import Arduino, SERVO
import smtplib
from email.mime.text import MIMEText
from config import SECRET_KEY

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY  # Needed for session management

# Connect to Arduino
board = Arduino('/dev/cu.usbmodem14101')

# Initialize servo pins
servos = [board.digital[pin] for pin in [3, 5, 6, 9, 10, 11]]

# Set all servos to SERVO mode
for servo in servos:
    servo.mode = SERVO
    servo.write(90)  # Set servos to neutral position


def check_hibp(email):
    api_key = "YOUR_HIBP_API_KEY"
    headers = {"hibp-api-key": api_key}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        return len(data)  # Number of breaches
    except requests.exceptions.RequestException as e:
        print(f"HIBP API request failed: {e}")
        return None


def control_servos(num_breaches):
    if num_breaches <= 10:
        servos[0].write(180)
    elif 11 <= num_breaches <= 20:
        servos[0].write(180)
        servos[1].write(180)
    elif 21 <= num_breaches <= 30:
        servos[0].write(180)
        servos[1].write(180)
        servos[2].write(180)
    elif 31 <= num_breaches <= 40:
        servos[0].write(180)
        servos[1].write(180)
        servos[2].write(180)
        servos[3].write(180)
    elif 41 <= num_breaches <= 50:
        servos[0].write(180)
        servos[1].write(180)
        servos[2].write(180)
        servos[3].write(180)
        servos[4].write(180)
    else:  # 51 or more breaches
        for servo in servos:
            servo.write(180)
    time.sleep(10)
    for servo in servos:
        servo.write(90)  # Reset all servos to neutral


def send_email(recipient):
    sender = 'youremail@example.com'
    password = 'yourpassword'

    msg = MIMEText("Here is your digital safety kit!")
    msg['Subject'] = 'Digital Safety Kit'
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        opt_in = 'opt_in' in request.form  # Check if opt-in is selected

        # Check HIBP for breaches
        num_breaches = check_hibp(email)

        if num_breaches is not None:
            control_servos(num_breaches)
            flash(f"Email '{email}' found in {num_breaches} breaches.")
            if opt_in:
                send_email(email)
                flash("A digital safety kit has been sent to your email.")
        else:
            flash("Failed to check breaches. Please try again.")

        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on Raspberry Pi
