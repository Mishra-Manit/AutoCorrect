import threading
from pynput import keyboard
from pynput.keyboard import Controller
from autocorrect import Speller

spell = Speller()

current_keys = []
controller = Controller()
spaces = []
timer = None

def correct_spelling():
    global timer
    if len(spaces) >= 2:
        lastSpaceIndex = spaces[-1]
        secondLastSpaceIndex = spaces[-2]

        word_between_spaces = ''.join(current_keys[secondLastSpaceIndex + 1:lastSpaceIndex])

        print("words between spaces: ", word_between_spaces)
            
        correctSpelling = spell(word_between_spaces)

        if (correctSpelling != word_between_spaces):
            print("correct spelling: ", correctSpelling, " NOOOOOO")
            for _ in range(len(word_between_spaces)):
                controller.press(keyboard.Key.left)
                controller.release(keyboard.Key.left)
            controller.type(correctSpelling + " ")

    timer = None

def on_press(key):
    global timer
    if timer:
        timer.cancel()

    try:
        current_keys.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            current_keys.append(" ")
        elif key == keyboard.Key.delete and current_keys: 
            current_keys.pop()

    if current_keys[-1] == " ":
        spaces.append(len(current_keys)-1)
        timer = threading.Timer(0.5, correct_spelling)  # Wait for 0.5 second of inactivity
        timer.start()

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()