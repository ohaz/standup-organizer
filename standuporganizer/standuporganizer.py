"""Main module."""
from PIL import ImageGrab
import PySimpleGUI as sg
from pytesseract import pytesseract
import random
import configargparse
import re

def main():
    p = configargparse.ArgParser(default_config_files=['config.yaml'])
    p.add('--tesseract-path', required=True, help='Path to tesseract binary (including binary)')  # this option can be set in a config file because it starts with '--'
    options = p.parse_args()
    pytesseract.tesseract_cmd = options.tesseract_path

    sg.theme('DarkAmber')   # Add a touch of color
    selected_index = 0
    # All the stuff inside your window.
    column = sg.Column([
        [sg.Listbox(values=[], enable_events=False, size=(30,15), key="member_list", font="Any 30", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, no_scrollbar=True)],
        [sg.Button(button_text="Import from image", key="import"), sg.Button(button_text="Reset", key="reset")],
        [sg.Button(button_text="Next", key="next")]
    ])
    layout = [ [column] ]

    # Create the Window
    window = sg.Window('Standup Organizer', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == "import":
            selected_index = 0
            img = ImageGrab.grabclipboard()
            img = img.convert('RGB').convert('L')
            img.save("image_name.jpg","JPEG")
            text = [re.sub('[^A-Za-z0-9\s]+', '', s).strip() for s in pytesseract.image_to_string(img).splitlines() if s and 'Organiser' not in s and 'Organisator' not in s]
            random.shuffle(text)
            window['member_list'].update(values=text, set_to_index=selected_index)
        if event == "next":
            selected_index = (selected_index + 1) % len(window['member_list'].Values)
            window['member_list'].update(set_to_index=selected_index)
        if event == "reset":
            selected_index = 0
            window['member_list'].update(values=[], set_to_index=selected_index)
    window.close()