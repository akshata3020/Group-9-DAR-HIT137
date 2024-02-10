import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline

class TkinterBaseApp:
    def __init__(self, title="Tkinter Application", size="600x400"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)

    def run(self):
        self.root.mainloop()
# Encapsulation: The AI model's translation logic is encapsulated within the translate method of the TranslationModel class, keeping it separate from the UI logic.
class TranslationModel:
    def __init__(self):
        self.translator = pipeline("translation_en_to_fr")

    def translate(self, text):
            translation = self.translator(text, max_length=40)[0]['translation_text']
            return translation
# Polymorphism: The Handle_Translate method in the TranslateHandler class is designed to be overridden by derived classes to provide specific translation functionality, demonstrating polymorphism.    
class TranslateHandler:
    def Handle_Translate(self, path):
        print(f"The word to be translate {path}")

# Multiple Inheritance: TranslationApp inherits from TkinterBaseApp, TranslationModel. This allows it to use methods and properties from all base classes.
class TranslationApp(TkinterBaseApp, TranslationModel, TranslateHandler):
    def __init__(self, title, size):
        TkinterBaseApp.__init__(self, title, size)  # Initialize the Tkinter app base
        TranslationModel.__init__(self)  # Initialize the translation model
        self.setup_ui()

    def setup_ui(self):
        self.text_input = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD)
        self.text_input.pack(pady=20)

# Decorators: The command=self.translate_button argument in tk.Button is a form of a decorator that binds the button click event to the on_translate method.
        self.translate_button = tk.Button(self.root, text="Translate to French", command=self.on_translate)
        self.translate_button.pack(pady=10)

        self.translation_output = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.translation_output.pack(padx=10, pady=5)

    def on_translate(self):
        input_text = self.text_input.get("1.0", tk.END).strip()
        if not input_text:
            self.Handle_Translate(input_text)
            return

        translation = self.translate(input_text)
        self.translation_output.config(state=tk.NORMAL)
        self.translation_output.delete("1.0", tk.END)
        self.translation_output.insert(tk.END, translation)
        self.translation_output.config(state=tk.DISABLED)
# Method overriding for polymorphic behavior
    def Handle_Translate(self, path):
        # Override to add GUI-related translate the words functionality
        print(f"Final word: {path}") 
if __name__ == "__main__":
    app = TranslationApp("Translate from English to French", "800x600")
    app.run()
