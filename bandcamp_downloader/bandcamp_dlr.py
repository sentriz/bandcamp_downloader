"""
Usage:
  bandcamp_dlr.py (<url> | --artist <name> --album <name>)
                  [--save-art | --embed] [--folder <name>] [--exclude <list>]

Options:
  -h, --help       Show this screen
  -v, --version    Show version
  --save-art       Download album artwork
  --embed-art      Embed album artwork
  --folder <name>  Name of download folder [default: downloads]
  --exclude <list> List of tracks to exclude from download. (seperated by ",")

Examples:
  bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --save-art
  bandcamp_dlr.py --artist "the-doors" --album "la-woman" --folder "My Music"
  bandcamp_dlr.py --artist "pinkfloyd" --album "dsotm" --exclude "3, 5, 7"
"""

from docopt import docopt
from lib.utilities.aesthetics import show_status, colour
from lib.utilities.functions import url_is_valid, mk_cd, error, yes_or_no
import Bandcamp
import sys

if __name__ == "__main__":
    args = docopt(__doc__, version = "bandcamp_dlr v1.1")
    #print(args)

    show_status("parsing arguments")
    
    if args["--exclude"]:
        try:
            exclude = [int(n) for n in args["--exclude"].replace(" ", "").split(",")]
        except ValueError:
            show_status(status = "%red%invalid exclude list")
            error()
    else:
        exclude = []
        
    if args["--folder"]:
        folder = args["--folder"].strip()
    else:
        show_status(status = "%red%please provide a folder")
        error()
        
    if args['--artist'] and args['--album']:
        show_status(status = "%yellow%artist/album found")
        url = "http://{}.bandcamp.com/album/{}".format(
            args['--artist'], args['--album']
        )
    elif args['<url>']:
        if url_is_valid(args["<url>"]):
            show_status(status = "%yellow%URL found")
            url = args['<url>']
        else:
            show_status(status = "%red%invalid URL")
            error()
            
    if args["--save-art"]:
        save_or_embed = "save"
    elif args["--embed"]
        save_or_embed = "embed"
    else:
        save_or_embed = None
        
    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . # 
    
    show_status("config: ", once_off=True)
    show_status("  - get artwork: %yellow%" + (save_or_embed \
        if save_or_embed in ["save", "embed"] else "no"), once_off=True)
    show_status("  - exclude: %yellow%" + ("none" \
        if not exclude else str(exclude)), once_off=True)
    show_status("  - folder: %yellow%" + args["--folder"], once_off=True)
        
    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . # 
    
    # create class
    album = Bandcamp.Album(
        url = url, 
        save_or_embed = save_or_embed
        exclude = exclude
    )
    
    prompt = "%yellow%do you want to download \"%dim%{}%bright%\" by " \
        "%dim%{}%bright%? %dim%[y/N] %bright%> ".format(album.artist, album.title)
        
    if yes_or_no(colour(prompt)):
        
        # make and change directories
        mk_cd(folder)
        mk_cd("{} - {}".format(album.artist, album.title))
        
        #album.download()
    else:
        sys.exit()
     
    
    
        
    
