import speech_recognition as sr
from googletrans import Translator
import RPi.GPIO as GPIO
from time import sleep
import subprocess
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
alarm = 18
light = 17
red = 24
green = 23
fan = 21
# Setting up output pins
GPIO.setup(alarm, GPIO.OUT)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)

def article_remover(text):
    if "the" in text:
        return text.replace("the ","")
    else:
        return text
def exit_check():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio).lower()
                return text
            except:
                pass
    return text


def Speech_to_Text():
    # Initialize an empty language variable
    lan = ""
    
    # Keep looping until a valid language is selected
    while True:
        # Initialize the speech recognizer
        rec = sr.Recognizer()
        
        # Use the default microphone to listen for the language selection
        with sr.Microphone() as source:
            subprocess.call(["espeak", "Select Language"])
            print("Select Language")
            lang = rec.listen(source)
        
        # Try to recognize the selected language using Google's speech recognition
        try :
            language = rec.recognize_google(lang).lower()
            
            # Set the appropriate language code based on the selected language
            if language == "telugu":
                lan = "te"
            elif language == "tamil":
                lan = "ta"
            elif language == "english":
                lan = "en"
            
            # Break out of the loop if a valid language was selected
            if lan == "ta" or lan =="te" or "en":
                break
        
        # If the language couldn't be recognized, print an error message
        except sr.UnknownValueError:
            print("unknown error occurred")

    # Print out the selected language
    subprocess.call(["espeak", f"{language} selected"])
    print(f"{language} selected")
    
    # Keep looping until the program is interrupted
    while True:
        # Initialize the speech recognizer
        r = sr.Recognizer()
        
        # Initialize the translator
        translator = Translator()
        
        # Use the default microphone to listen for speech
        with sr.Microphone() as source:
            subprocess.call(["espeak", "Listening"])
            print("Listening...")
            audio = r.listen(source)
            
            # Try to recognize the speech and translate it to English
            try:
                # Recognize the speech in the selected language
                MyText_te = r.recognize_google(audio,language=f"{lan}-IN").lower()
                print(f"Original Text: {MyText_te}")
                
                # Translate the recognized speech to English
                result_te = translator.translate(MyText_te,src=f"{lan}",dest='en')
                print(f"Translated Text: {result_te.text.lower()}")
                return article_remover(result_te.text.lower())
            
            # If the speech couldn't be recognized, print an error message
            except sr.UnknownValueError:
                print("unknown error occurred")
    
    # Return the translated text
    return result_te.text

def finite_automaton():

    while True:
        # Define the states of the automaton
        states = ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]

        # Define the transitions of the automaton

        transitions = [("q0", "q1", "turn"),
                        ("q1", "q2", "on"),
                        ("q2", "q3", "light"),
                        ("q2", "q4", "fan"),
                        ("q2", "q5", "alarm"),
                        ("q0", "q6", "switch"),
                        ("q6", "q2", "on"),
                        ("q1", "q7", "off"),
                        ("q6", "q7", "off"),
                        ("q7", "q8", "light"),
                        ("q7", "q9", "fan"),
                        ("q7", "q10", "alarm")]

        # Define the final states of the automaton
        final_states = ["q3","q4","q5","q8","q9","q10"]
        light_on = ["q3"]
        light_off = ["q8"]
        fan_on = ["q4"]
        fan_off = ["q9"]
        alarm_on = ["q5"]
        alarm_off = ["q10"]

        # Define the input string
        input_string = Speech_to_Text()  # or "turn off", "switch on", or "switch off"
        if input_string == "exit":
            subprocess.call(["espeak", "Thank you"])
            break
        # Split the input string into a list of words
        words = input_string.split(" ")

        # Initialize the current state to the start state
        current_state = "q0"

        # Iterate through the list of words
        for word in words:
            # Check if there is a transition from the current state with the current word
            for (from_state, to_state, word_required) in transitions:
                if from_state == current_state and word == word_required:
                    # If there is a valid transition, update the current state
                    current_state = to_state
                    break

        # # Check if the current state is a final state
        # if current_state in final_states:
        #     print("Yes, Input string accepted by automaton!")
        #     # Trigger the appropriate action (e.g. turning on or off an appliance)
        # else:
        #     print("No, Input string not accepted by automaton.")

        if current_state in final_states:
            subprocess.call(["espeak", "String accepted"])
            GPIO.output(green,GPIO.HIGH)
            time.sleep(3)
            GPIO.output(green,GPIO.LOW)
            print("Enable green light")
        elif current_state not in final_states:
            subprocess.call(["espeak", "String rejected"])
            GPIO.output(red,GPIO.HIGH)
            time.sleep(3)
            GPIO.output(red,GPIO.LOW)
            print("Enable red light")
        
        if current_state in light_on:
            subprocess.call(["espeak", "Turning on light"])
            GPIO.output(light,GPIO.HIGH)
            print("Turn on or Switch off light")
        elif current_state in light_off:
            subprocess.call(["espeak", "Turning off light"])
            GPIO.output(light,GPIO.LOW)
            print("Turn off or Switch off light")
        elif current_state in fan_on:
            subprocess.call(["espeak", "Turning on fan"])
            GPIO.output(fan,GPIO.HIGH)
            print("Turn on or Switch on fan")
        elif current_state in fan_off:
            subprocess.call(["espeak", "Turning off fan"])
            GPIO.output(fan,GPIO.LOW)
            print("Turn off or Switch off fan")
        elif current_state in alarm_on:
            subprocess.call(["espeak", "Turning on alarm"])
            GPIO.output(alarm,GPIO.HIGH)
            print("Turn on or Switch on buzzer")
        elif current_state in alarm_off:
            subprocess.call(["espeak", "Turning off alarm"])
            GPIO.output(alarm,GPIO.LOW)
            print("Turn off or Switch off buzzer")


# while True:
#     if exit_check() == 'exit':
#         break
#     else:
#         finite_automaton()
finite_automaton()