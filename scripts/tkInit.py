import tkinter as tk
from PIL import Image, ImageTk
from spellingHandler import getWord, checkSpelling, speak
import threading
import queue

class SpellingApp:
    def __init__(self, root, spellings):
        self.root = root
        self.spellings = spellings

        self.lastWord = None
        self.word = getWord(self.lastWord, spellings)
        self.score = 0
        self.total = 0

        self.uiSetup()

    def __str__(self):
        return f"Score: {self.score}/{self.total}"
    
    def __repr__(self):
        return f"SpellingApp(score={self.score}, total={self.total}, word='{self.word}')"

    def uiSetup(self):
        self.root.title("Spellings")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        image = Image.open("assets/button.png").resize((200, 200))
        self.img = ImageTk.PhotoImage(image)

        self.playButton = tk.Button(
            frame,
            image=self.img,
            command=self.playWord,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg=frame.cget("bg"),
            activebackground=frame.cget("bg")
        )
        self.playButton.pack(pady=10)

        self.userTextbox = tk.Entry(frame, font=("Arial", 16), width=20)
        self.userTextbox.pack(pady=10)

        self.submitButton = tk.Button(frame, text="Submit", font=("Arial", 20), command=self.submit)
        self.submitButton.pack(pady=10)

        self.resultLabel = tk.Label(frame, text="", font=("Arial", 20))
        self.resultLabel.pack(pady=10)

        self.scoreLabel = tk.Label(self.root, text=str(self), font=("Arial", 24))
        self.scoreLabel.place(x=10, y=10)

        self.userTextbox.bind("<Key>", lambda _: self.resultLabel.config(text=""))
        self.userTextbox.bind("<Return>", lambda _: self.submit())

    def playWord(self):
        self.playButton.config(state="disabled")

        def run():
            speak(self.word)
            self.root.after(0, lambda: self.playButton.config(state="normal"))

        threading.Thread(target=run, daemon=True).start()
    
    def submit(self):
        
        correct = checkSpelling(self.userTextbox.get(), self.word)
        self.lastWord = self.word
        self.word = getWord(self.lastWord, self.spellings)

        if correct:
            text = f"Correct!"
            self.score+=1
        else:
            text = f"Incorrect. The word was {self.lastWord}"
        self.total+=1
        self.resultLabel.config(text=text)
        self.scoreLabel.config(text=str(self))
        self.userTextbox.delete(0, tk.END)
        self.playWord()


def initWindow(spellings: list):
    root = tk.Tk()
    app = SpellingApp(root, spellings)
    app.playWord()
    root.mainloop()