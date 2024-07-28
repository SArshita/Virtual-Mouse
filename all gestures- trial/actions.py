import pyautogui
import ctypes

# Move mouse cursor
def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

# Left click
def click_left():
    pyautogui.click(button='left')

# Right click
def click_right():
    pyautogui.click(button='right')

# Drag
def drag():
    pyautogui.mouseDown(button='left')

# Release drag
def release_drag():
    pyautogui.mouseUp(button='left')

# Control volume (increase/decrease)
def control_volume(increase=True):
    if increase:
        pyautogui.press('volumeup')
    else:
        pyautogui.press('volumedown')

# Minimize all windows
def minimize_windows():
    pyautogui.hotkey('win', 'd')

# Restore all windows
def restore_windows():
    pyautogui.hotkey('win', 'shift', 'm')

# Open start menu
def open_start_menu():
    pyautogui.press('win')
