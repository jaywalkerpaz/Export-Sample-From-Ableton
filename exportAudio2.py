#DRAG AND DROP SAMPLE FILE INTO A DRUM RACK

#USAGE:
#CD to the directory containing this script and run 'python exportAudio2.py'.

#DESCRIPTION:
#This is a custom script to simulate drag-drop behavior, which appears to be necessary to move samples into Ableton Sampler devices.

#In my setup, a Max4Live device selects the appropriate Sampler device of the selected Drum Rack. At the same time, a temp folder with a single sample file is opened and centered to allow drag and drop to work correctly.

#NOTES:
#'pyautogui' must be downloaded.

import pyautogui, os

pyautogui.moveTo(267, 111)
pyautogui.click()
pyautogui.dragTo(1076, 699, button='left', duration=.2)

os.system('''
  /usr/bin/osascript -e
    'tell app "Finder" to set frontmost of process "Finder" to true'
  ''')
