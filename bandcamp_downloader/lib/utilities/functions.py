from .aesthetics import show_status, colour
import os
import sys
        
# sentriz
def url_is_valid(url):
    if url == "!testing!":
        return True
    requirements = ["http", "://", ".bandcamp.com", "/album/"] 
    for part in requirements:
        if url.find(part) < 0:
            return False
    return True
    
def error():
    print("- see bandcamp_dlr.py --help")
    sys.exit(1)           
            
def yes_or_no(question):
    yes = ["yes", "y", "ye"]
    no = ["no", "n", ""] # "" for default answer
    
    print(question, end="")
    choice = input().lower()
    if choice in yes:
       return True
    elif choice in no:
       return False
    else:
       print(colour("%red%please provide a valid option"))
    
if __name__ == "__main__":

    # damn relative imports ..
    # running this as __main__ won't work anymore.
    # anyone wanna tell me what's going on? :)
    
    mk_cd("test_folder")
    mk_cd("test_folder_in_test_folder")
    
    print(url_is_valid("http://artist.bandcamp.com/album/album"))
    print(url_is_valid("http://artist.bindcomp.com/album/album"))
    print(url_is_valid("https://artist.bandcamp.com/album/album/"))
    print(url_is_valid("http://artist.bandcamp.com/alboom/album"))
    print(url_is_valid("http:/artist.bandcamp.com/album/album"))