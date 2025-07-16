import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pyjokes
import os
import smtplib

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Function to speak and print text
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Greet the user
def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your AI Assistant. How may I help you?")

# Listen to microphone input
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return "None"
    return query.lower()

# Email functionality
def send_email(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your_email@gmail.com", "your_password")  # Use App Password
    server.sendmail("your_email@gmail.com", to, content)
    server.quit()

# Main function
def main():
    speak("Hello! This is a test of your speech system.")
    greet_user()

    while True:
        command = listen_command()

        if 'wikipedia' in command:
            speak("Searching Wikipedia...")
            query = command.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)

        elif 'search youtube for' in command:
            query = command.replace("search youtube for", "").strip()
            speak(f"Searching YouTube for {query}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

        elif 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'time' in command:
            time_now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time_now}")

        elif 'date' in command:
            date_now = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {date_now}")

        elif 'joke' in command:
            speak(pyjokes.get_joke())

        elif 'send email' in command:
            try:
                speak("What should I say?")
                content = listen_command()
                to = "receiver_email@gmail.com"
                send_email(to, content)
                speak("Email has been sent!")
            except Exception as e:
                speak("Sorry, I could not send the email.")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("Sorry, I can't perform that task yet.")

if __name__ == "__main__":
    main()