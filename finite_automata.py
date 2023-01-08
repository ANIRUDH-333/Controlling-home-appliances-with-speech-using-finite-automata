import speech_recognition as sr
from googletrans import Translator
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)

def Speech_to_Text():
    # Initialize an empty language variable
    lan = ""
    
    # Keep looping until a valid language is selected
    while True:
        # Initialize the speech recognizer
        rec = sr.Recognizer()
        
        # Use the default microphone to listen for the language selection
        with sr.Microphone() as a:
            print("Select Language")
            lang = rec.listen(a)
        
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
    print(f"{language} selected")
    
    # Keep looping until the program is interrupted
    while True:
        # Initialize the speech recognizer
        r = sr.Recognizer()
        
        # Initialize the translator
        translator = Translator()
        
        # Use the default microphone to listen for speech
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            
            # Try to recognize the speech and translate it to English
            try:
                # Recognize the speech in the selected language
                MyText_te = r.recognize_google(audio,language=f"{lan}-IN")
                print(MyText_te)
                
                # Translate the recognized speech to English
                result_te = translator.translate(MyText_te,src=f"{lan}",dest='en')
                print(result_te.text)
                return result_te.text
            
            # If the speech couldn't be recognized, print an error message
            except sr.UnknownValueError:
                print("unknown error occurred")
    
    # Return the translated text
    return result_te.text

def finite_automaton():
    # Define the states of the automaton
    states = ["q0", "q1", "q2", "q3", "q4"]

    # Define the transitions of the automaton

    transitions = [("q0", "q1", "turn"),
                    ("q1", "q2", "on"),
                    ("q1", "q3", "off"),
                    ("q0", "q4", "switch"),
                    ("q4", "q2", "on"),
                    ("q4", "q3", "off")]

    # Define the final states of the automaton
    final_states = ["q2", "q3"]
    final_states_on = ["q2"]
    final_states_off = ["q3"]

    # Define the input string
    input_string = Speech_to_Text()  # or "turn off", "switch on", or "switch off"

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

    if current_state in final_states_on:
        GPIO.output(buzzer,GPIO.HIGH)
        print("Turn on or Switch on")
    elif current_state in final_states_off:
        GPIO.output(buzzer,GPIO.LOW)
        print("Turn off or Switch off")

finite_automaton()