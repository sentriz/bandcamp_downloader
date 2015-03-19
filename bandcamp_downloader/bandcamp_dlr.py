"""
Usage:
  bandcamp_dlr.py (<url> | --artist <name> --album <name>)
                  [--save-art | --embed-art] [--folder <name>] [--exclude <list>]
                  [--splash] [--help] [--version]

Options:
  --embed-art      Embed album artwork
  --exclude <list> List of tracks to exclude from download. (seperated by ",")
  --folder <name>  Name of download folder [default: downloads]
  --save-art       Download album artwork
  --splash         Show a splash screen on startup
  -h, --help       Show this screen
  -v, --version    Show version

Examples:
  bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --save-art
  bandcamp_dlr.py --artist "the-doors" --album "la-woman" --folder "My Music"
  bandcamp_dlr.py --artist "pinkfloyd" --album "dsotm" --exclude "3, 5, 7"
"""

from docopt import docopt
from lib.utilities.aesthetics import colour
from lib.utilities.aesthetics import show_status
from lib.utilities.functions import error
from lib.utilities.functions import url_is_valid
from lib.utilities.functions import yes_or_no
import Bandcamp
import sys

if __name__ == "__main__":
    args = docopt(__doc__, version="bandcamp_dlr v1.3.2")

    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . #

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
        download_folder_name = args["--folder"].strip()
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
    elif args["--embed-art"]:
        save_or_embed = "embed"
    else:
        save_or_embed = None

    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . #

    show_status("config: ", once_off=True)
    show_status("  - get artwork: %yellow%" + (save_or_embed \
        if save_or_embed in ["save", "embed"] else "no"), once_off=True)
    show_status("  - exclude: %yellow%" + ("none" \
        if not exclude else str(exclude)), once_off=True)
    show_status("  - folder: %yellow%" + download_folder_name, once_off=True)

    # . . . - - - . . . # . . . - - - . . . # . . . - - - . . . #

    # create class
    album = Bandcamp.Album(
        url = url,
        save_or_embed = save_or_embed,
        exclude = exclude,
        download_folder_name = download_folder_name
    )

    prompt = "%yellow%%dim%sure you want to download \"%bright%{title}%dim%\" by " \
        "%bright%{artist}%dim%? %bright%[y/N] %dim%> ".format(
            title = album.title,
            artist = album.artist
        )

    if yes_or_no(colour(prompt)):
        # start
        album.download()
    else:
        sys.exit()