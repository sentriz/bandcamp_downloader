from colorama import Fore, init
init(autoreset = True)

# "doing task ... DONE"
# "doing another task ... DONE"

last_message = None

def show_status(message = "", once_off = False):
    global last_message

    def replace_all(string, dict):
        for alias, assumed in dict.items():
            string = string.replace(alias, assumed)
        return string
    
    colours = {
        "%" + color.lower() + "%": getattr(Fore, color) \
            for color in dir(Fore) if "_" not in color
    }
    message = replace_all(message, colours)
        
    print(message + " ... ", end = "")
    
    if last_message:
        print("\r" + last_message + " ... " + message)
        last_message = None
    else:
        last_message = message
        
# testing
if __name__ == "__main__":
    import time
    
    show_status("testing")
    time.sleep(1)
    show_status("%red%niples")