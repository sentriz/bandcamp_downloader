import colorama
from colorama import Fore

colorama.init(autoreset = True)

# "doing task ... DONE"
# "doing another task ... DONE"

last_message = None

def show_status(message = "", status = (Fore.GREEN + "done")):

    global last_message
    
    print(message + " ... ", end = "")
    
    if last_message:
        print("\r" + last_message + " ... " + status)
        last_message = None
        
    else:
        last_message = message