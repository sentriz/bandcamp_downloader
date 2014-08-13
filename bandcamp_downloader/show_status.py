"""
This module may be stupid, but I couldn't think of a better way of doing - 
what I wanted to do.. Maybe I'll think of it later. - sentriz
"""

from colorama import Fore, Style, init
init(autoreset = True)

last_message = None

def show_status(message = "", status = "", once_off = False):
    global last_message
    
    def replace_text(string):
        colours = {"%" + color.lower() + "%": getattr(Fore, color) \
            for color in dir(Fore) if "_" not in color}
        styles = {"%" + style.lower() + "%": getattr(Style, style) \
            for style in dir(Style) if "_" not in style}
        for alias, esc in colours.items() | styles.items():
            string = string.replace(alias, esc)
        return string
    
    message = replace_text(message)
    status = replace_text(status)
    
    if not once_off:
        print(">", message + "... ", end = "")
        if last_message:
            print("\r> " + last_message + "... " + status + " "*5)
            last_message = None
        else:
            last_message = message
    else:
        print(replace_text("> " + message))
        
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
    show_status("doing weird thing", once_off = True)
    time.sleep(.1)
    show_status("doing weird thing again", once_off = True)
    time.sleep(.1)
    show_status("doing something else, will faileds")
    time.sleep(.1)
    show_status(status = "%red%faileds")
  
