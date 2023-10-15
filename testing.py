from pynput import keyboard
from pynput.keyboard import Controller

from autocorrect import Speller

from textblob import Word

import time

spell = Speller()
#fast=True

current_keys = []
controller = Controller()

spaces = []

programmatic_keypress = False  # Global flag

def correct_word(correctSpelling, word_between_spaces):
    if (correctSpelling != word_between_spaces):
        #time.sleep(0.2)
        
        print("correct spelling: ", correctSpelling, " NOOOOOO")

        for _ in range(len(word_between_spaces) + 1):  # +1 for the space after the word
            controller.press(keyboard.Key.left)
            controller.release(keyboard.Key.left)


        # Delete the word using the "Delete" key
        for _ in range(len(word_between_spaces)):
            controller.press(keyboard.Key.delete)
            controller.release(keyboard.Key.delete)
        
        controller.type(correctSpelling + " ")

def on_press(key):

    global programmatic_keypress

    if programmatic_keypress:
        return  # Ignore this key press

    try:
        current_keys.append(key.char)
        
        #print("key.char: ", key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            current_keys.append(" ")

        if (key == keyboard.Key.delete and current_keys): 
            current_keys.pop()

    print("current keys: ", current_keys)

# also make sure to not count punctuation

    if current_keys[-1] == " ":
        spaces.append(len(current_keys)-1)

    #print("spaces: ", spaces)

    if len(spaces) >= 2:
        lastSpaceIndex = spaces[-1]
        secondLastSpaceIndex = spaces[-2]

        if current_keys[-1] == " ":
            word_between_spaces = ''.join(current_keys[secondLastSpaceIndex + 1:lastSpaceIndex])

            print("words between spaces: ", word_between_spaces)
            
            correctSpelling = spell(word_between_spaces)

            print("correct spelling: ", word_between_spaces)

            word = Word(word_between_spaces)
 
            #correctSpelling = word.spellcheck()[0][0]
            correct_word(correctSpelling, word_between_spaces)
            

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()