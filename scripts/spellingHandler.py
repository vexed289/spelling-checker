import random
import pyttsx3



def getWord(last: str | None, spellings: list) -> str:
    current = last
    if current is None:
        return random.choice(spellings).strip()
    
    while current == last and len(spellings) > 1:
        current = random.choice(spellings).strip()
    return current

def speak(word: str):
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()

def checkSpelling(input: str, correct: str):
    return input.strip().lower() == correct.strip().lower()