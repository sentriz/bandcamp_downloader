"""
Usage:
  bandcamp_dlr.py (<url> | --artist=<name> --album=<name>)
                  [--get-art] [--folder=<name>] [--exclude=<list>]

Options:
  -h, --help       Show this screen.
  -v, --version    Show version.
  --get-art        Download album artwork.
  --folder=<name>  Name of download folder [default: downloads].
  --exclude=<list> List of tracks to exclude from download. (seperated by a space)

Examples:
  * no, these artists are /not/ not on Bandcamp *
  bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --get-art
  bandcamp_dlr.py --artist="the-doors" --album="la-woman" --folder="My Music"
  bandcamp_dlr.py --artist="pinkfloyd" --album="dsotm" --exclude="3 5 7"
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
    finally:
        os.chdir(dir_name)
        
def error():
    print("see bandcamp_dlr.py --help")
    sys.exit(1)

if __name__ == "__main__":
    args = docopt(__doc__, version = "bandcamp_dlr 0.6")

    show_status("parsing arguments")
    if args:
        if args['--artist'] and args['--album']:
            show_status(status = "%yellow%artist/album found")
            artist, album = args['--artist'], args['--album']
            url = "http://{}.bandcamp.com/album/{}".format(artist, album)
        elif args['<url>']:
            if (not "bandcamp" in args['<url>']) or (not "album" in args['<url>']) or (not args['<url>'].startswith("http://")):
                show_status(status = "%red%invalid URL found")
                error()
            else:
                show_status(status = "%yellow%URL found")
                url = args['<url>']
                # remove trailing slash
                if url[-1] == "/":
                    url = url[:-1] 
        else:
            show_status(status = "%red%URL or artist/album not provided")
            error()
            
        if args["--exclude"]:
            exclude = [int(n) for n in args["--exclude"].split()]
        else:
            exclude = [] # None is not iterable
            
        # "%album% - %title%"
        album_name = url.replace("http://", "").replace(".bandcamp.com/album/", "|").split("|")
        album_name = "{} - {}".format(*album_name)
        
        mk_cd(args["--folder"])
        mk_cd(album_name)

        # start
        Bandcamp.download(url, args["--get-art"], exclude)
    else:
        show_status(status = "%red%none found")
        error()
