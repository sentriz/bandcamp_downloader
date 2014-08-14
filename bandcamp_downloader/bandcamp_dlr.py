"""
Usage:
  bandcamp_dlr.py (<url> | --artist=<name> --album=<name>)
                  [--get-art] [--folder=<name>] [--exclude=<list>]

Options:
  -h, --help       Show this screen.
  -v, --version    Show version.
  --get-art        Download album artwork.
  --folder=<name>  Name of download folder [default: downloads].
  --exclude=<list> List of tracks to exclude from download. (seperated by ",")

Examples:
  * no, these artists are /not/ not on Bandcamp *
  bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --get-art
  bandcamp_dlr.py --artist="the-doors" --album="la-woman" --folder="My Music"
  bandcamp_dlr.py --artist="pinkfloyd" --album="dsotm" --exclude="3, 5, 7"
"""

from docopt import docopt
import Bandcamp
import os, sys
import colorama
from show_status import show_status

def mk_cd(dir_name):

    try:
        show_status("creating directory \"%dim%{}%bright%\"".format(dir_name))
        os.makedirs(dir_name)
        show_status(status = "%green%done")
    except FileExistsError:
        show_status(status = "%yellow%already exists")
    except (PermissionError, OSError):
        show_status(status = "%red%failed")
        error()
    os.chdir(dir_name)
        
def error():
    print("- see bandcamp_dlr.py --help")
    sys.exit(1)
    
def url_is_valid(url):
    requirements = ["http", "://", ".bandcamp.com", "/album/"] 
    for part in requirements:
        if url.find(part) < 0:
            return False
    return True

if __name__ == "__main__":
    args = docopt(__doc__, version = "bandcamp_dlr v1.1")
    #print(args)

    show_status("parsing arguments")
    
    if args["--exclude"]:
        exclude_list = [int(n) for n in args["--exclude"].replace(" ", "").split(",")]
    else:
        exclude_list = [] # None is not iterable
        
    if args["--get-art"]:
        get_art = True
    else:
        get_art = False
        
    if args["--folder"]:
        folder = args["--folder"].strip()
    else:
        show_status(status = "%red%please provide a folder")
        error()
        
    if args['--artist'] and args['--album']:
        show_status(status = "%yellow%artist/album found")
        artist, album = args['--artist'], args['--album']
        url = "http://{}.bandcamp.com/album/{}".format(artist, album)
    elif args['<url>']:
        if url_is_valid(args["<url>"]):
            show_status(status = "%yellow%URL found")
            url = args['<url>']
            # remove trailing slash
            if url[-1] == "/": url = url[:-1] 
        else:
            show_status(status = "%red%invalid URL found")
            error()
    else:
        show_status(status = "%red%URL or artist/album not provided")
        error()
        
    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . # 
    
    show_status("config: ", once_off=True)
    show_status("  - get artwork: %yellow%" + ("yes" \
        if get_art else "no"), once_off=True)
    show_status("  - exclude: %yellow%" + ("none" \
        if not exclude_list else str(exclude_list)), once_off=True)
    show_status("  - folder: %yellow%" + args["--folder"], once_off=True)
        
    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . # 
        
    # "%album% - %title%"
    album_name = "{} - {}".format(
        *url.replace("http://", "").replace(".bandcamp.com/album/", "|").split("|")
    )
    
    # make and change directories
    mk_cd(folder)
    mk_cd(album_name)
        

    # start
    Bandcamp.download(url, get_art, exclude_list)
    
    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . # 
