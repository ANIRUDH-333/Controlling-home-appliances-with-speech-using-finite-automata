# Controlling-home-appliances-with-speech-using-finite-automata

**Project Description**
* Developed a system for controlling home appliances using speech commands and finite automata.
* Implemented hardware components such as LEDs, buzzers, motors, and Raspberry Pi with integrated microphone and speaker for input and output.
* Utilized speech recognition and Google Translate modules for converting speech to commands, and Python for the backend processing.

**Knowledge**
Finite Automata, Speech Recognition, Google Translate API, Raspberry Pi, Hardware Integration, Python


# Directory structure
main.ipynb          -   Contains all the python code for speech to text conversion and the defined automaton
requirements.txt    -   Contains the required packages



# Environment
```
python=3.8
```

# Installing packages
```
pip install -r requirements.txt
```

# Issue with installing PyAudio
### Common Issue in Ubuntu
```
sudo apt install build-essential portaudio19-dev python3.8-dev
```
Once this is successfully installed, continue installing PyAudio
```
pip install PyAudio
```
This should work in maximum cases

# Hardware Setup with Raspberry Pi
This has been extended to a real world application of controlling home appliances with the speech which gets coverted to text.
This text is given to the defined automata which accepts specific strings like "turn on" , "turn off" etc. Based on its acceptance, the LED which we have connected to the raspberry pi lights up or dims down.
