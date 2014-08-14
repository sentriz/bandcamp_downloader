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

import os, sys
from docopt import docopt

import Bandcamp
from lib.utilities.aesthetics import show_status
from lib.utilities.functions import url_is_valid, mk_cd, error

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
            show_status(status = "%red%invalid URL")
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
        *url.replace("https://", "").replace("http://", "") \
            .replace(".bandcamp.com/album/", "|").split("|")
    )
    
    # make and change directories
    mk_cd(folder)
    mk_cd(album_name)

    # start
    Bandcamp.download(url, get_art, exclude_list)
    
    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . # 
