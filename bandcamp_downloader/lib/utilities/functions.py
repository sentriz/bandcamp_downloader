from .aesthetics import show_status
from .aesthetics import colour
import os
import sys
        
def url_is_valid(url):
    if url == "!testing!":
        return True
        
    requirements = ["http", "://", ".bandcamp.com", "/album/"] 
    
    for part in requirements:
        if part not in url:
            return False
            
    return True         
            
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
   
    print(url_is_valid("http://artist.bandcamp.com/album/album"))
    print(url_is_valid("http://artist.bindcomp.com/album/album"))
    print(url_is_valid("https://artist.bandcamp.com/album/album/"))
    print(url_is_valid("http://artist.bandcamp.com/alboom/album"))
    print(url_is_valid("http:/artist.bandcamp.com/album/album"))
