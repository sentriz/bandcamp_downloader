from ..colorama import Fore, Style, init
import os

"""
This module may be stupid, but I couldn't think of a better way of doing - 
what I wanted to do.. Maybe I'll think of it later. - sentriz
"""

init(autoreset = True)

last_message = None

def colour(string):
    colours = {"%" + color.lower() + "%": getattr(Fore, color) \
        for color in dir(Fore) if "_" not in color}
    styles = {"%" + style.lower() + "%": getattr(Style, style) \
        for style in dir(Style) if "_" not in style}
    for alias, esc in colours.items() | styles.items():
        string = string.replace(alias, esc)
    return string
    
def show_status(message = "", status = "", once_off = False):
    global last_message
    
    if not once_off:
        print(colour("%dim%> %bright%" + message + "... "), end = "")
        if last_message:
            print(colour("\r%dim%> %bright%" + last_message + "... " + status + " "*5))
            last_message = None
        else:
            last_message = message
    else:
        print(colour("%dim%> %bright%" + message))
        
def get_console_width():
    """Return width of available window area. Autodetection works for
       Windows and POSIX platforms. Returns 80 for others

       Code from http://bitbucket.org/techtonik/python-pager
    """

    if os.name == 'nt':
        STD_INPUT_HANDLE  = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE  = -12

        # get console handle
        from ctypes import windll, Structure, byref
        try:
            from ctypes.wintypes import SHORT, WORD, DWORD
        except ImportError:
            # workaround for missing types in Python 2.5
            from ctypes import (
                c_short as SHORT, c_ushort as WORD, c_ulong as DWORD)
        console_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        # CONSOLE_SCREEN_BUFFER_INFO Structure
        class COORD(Structure):
            _fields_ = [("X", SHORT), ("Y", SHORT)]

        class SMALL_RECT(Structure):
            _fields_ = [("Left", SHORT), ("Top", SHORT),
                        ("Right", SHORT), ("Bottom", SHORT)]

        class CONSOLE_SCREEN_BUFFER_INFO(Structure):
            _fields_ = [("dwSize", COORD),
                        ("dwCursorPosition", COORD),
                        ("wAttributes", WORD),
                        ("srWindow", SMALL_RECT),
                        ("dwMaximumWindowSize", DWORD)]

        sbi = CONSOLE_SCREEN_BUFFER_INFO()
        ret = windll.kernel32.GetConsoleScreenBufferInfo(console_handle, byref(sbi))
        if ret == 0:
            return 0
        return sbi.srWindow.Right+1

    elif os.name == 'posix':
        from fcntl import ioctl
        from termios import TIOCGWINSZ
        from array import array

        winsize = array("H", [0] * 4)
        try:
            ioctl(sys.stdout.fileno(), TIOCGWINSZ, winsize)
        except IOError:
            pass
        return (winsize[1], winsize[0])[0]

    return 80
        
# testing
if __name__ == "__main__":
    import time
    
    show_status("doing thing")
    time.sleep(.1)
    show_status(status = "%green%done")
    time.sleep(.1)
    show_status("doing something else")
    time.sleep(.1)
    show_status(status = "%red%failed")
  
    time.sleep(.1)
    show_status("doing weird thing", once_off=True)
    time.sleep(.1)
    show_status("doing weird thing again", once_off=True)
    time.sleep(.1)
    show_status("doing something else, will faileds")
    time.sleep(.1)
    show_status(status = "%red%faileds")
  
