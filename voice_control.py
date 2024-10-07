import speech_recognition as sr  # Speech recognition for voice commands
import RPi.GPIO as GPIO  # GPIO control for Raspberry Pi
import time  # Time module for delays

# GPIO setup for controlling the LED
GPIO.setmode(GPIO.BCM)  # Using BCM pin numbering
GPIO.setwarnings(False)  # Disabling warnings
GPIO.setup(27, GPIO.OUT)  # Setting GPIO 27 as output

def turn_on_light():
    GPIO.output(27, GPIO.HIGH)  # Turn LED on
    print("Light turned ON")

def turn_off_light():
    GPIO.output(27, GPIO.LOW)  # Turn LED off
    print("Light turned OFF")

# Initialize the recognizer for speech commands
recognizer = sr.Recognizer()

def listen_for_command():
    with sr.Microphone() as source:  # Using the microphone as input
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Capture audio

    try:
        command = recognizer.recognize_google(audio).lower()  # Convert audio to text
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("API request error")
    return None

def main():
    while True:
        command = listen_for_command()
        if command:
            if "turn on" in command:
                turn_on_light()
            elif "turn off" in command:
                turn_off_light()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on exit
        print("Program stopped.")
