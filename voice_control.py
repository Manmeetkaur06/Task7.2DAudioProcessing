import speech_recognition as sr  # Speech recognition for voice commands
import RPi.GPIO as GPIO  # GPIO control for Raspberry Pi
import time  # Time module for delays

# GPIO setup for controlling the LED
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme for Raspberry Pi GPIO
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setup(27, GPIO.OUT)  # Set GPIO pin 27 as output for controlling the LED

def turn_on_light():
    # Function to turn on the LED connected to GPIO pin 27
    GPIO.output(27, GPIO.HIGH)  # Set GPIO 27 output to HIGH, turning the LED on
    print("Light turned ON")  # Print message for confirmation

def turn_off_light():
    # Function to turn off the LED connected to GPIO pin 27
    GPIO.output(27, GPIO.LOW)  # Set GPIO 27 output to LOW, turning the LED off
    print("Light turned OFF")  # Print message for confirmation

# Initialize the recognizer to handle speech commands
recognizer = sr.Recognizer()  # Create an instance of the speech recognizer

def listen_for_command():
    # Function to listen for voice commands using the microphone
    with sr.Microphone() as source:  # Use the system microphone as the input source
        print("Listening for command...")  # Indicate that the system is listening
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)  # Record the audio input

    try:
        # Attempt to recognize the command using Google Speech Recognition
        command = recognizer.recognize_google(audio).lower()  # Convert audio to lowercase text
        print(f"Command received: {command}")  # Print recognized command
        return command  # Return the recognized command
    except sr.UnknownValueError:
        # Handle the case where the speech could not be understood
        print("Could not understand the audio")  # Print error message
    except sr.RequestError:
        # Handle any issues with the API request
        print("API request error")  # Print error message
    return None  # Return None if the command wasn't recognized

def main():
    # Main loop to continuously listen for commands and control the LED
    while True:
        command = listen_for_command()  # Get the command from the user
        if command:
            # Check if the command is to turn the light on or off
            if "turn on" in command:
                turn_on_light()  # Call the function to turn on the LED
            elif "turn off" in command:
                turn_off_light()  # Call the function to turn off the LED
        time.sleep(1)  # Pause for a second before listening for the next command

if __name__ == "__main__":
    # Run the program and handle any cleanup on exit
    try:
        main()  # Start the main loop
    except KeyboardInterrupt:
        GPIO.cleanup()  # Reset the GPIO pins when the program is interrupted
        print("Program stopped.")  # Print message confirming the program has stopped
