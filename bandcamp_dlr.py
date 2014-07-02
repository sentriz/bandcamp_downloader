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
import os
import colorama
from colorama import Fore, Style
from show_status import show_status

colorama.init(autoreset = True)

if __name__ == "__main__":
    args = docopt(__doc__, version = "bandcamp_dlr 0.6")

    # check if the user provided arguments ...
    if args:
        # did they use the artist/album --flags ...
        if args['--artist'] and args['--album']:
            artist, album = args['--artist'], args['--album']
            url = "http://{}.bandcamp.com/album/{}/".format(artist, album)

        # or did they provide a URL?
        elif args['<url>']:
        
            # was it a valid URL?
            if not "bandcamp" in args['<url>'] or not "album" in args['<url>'] or \
                not args['<url>'].startswith("http://"):
                
                    print(Fore.RED + "\n" + "error: invalid URL.")
                    normal = Style.RESET_ALL + Fore.RED + Style.DIM
                    bold = Style.RESET_ALL + Fore.RED + Style.BRIGHT
                    print(
                        normal
                        + "URL must be in the format "
                        + "http://" + bold + "artist"
                        + normal + ".bandcamp.com/album/"
                        + bold + "album" + normal
                        + "/"
                    )
                    print("\n" + "\n".join(__doc__.split("\n")[1:4]))
                    exit()
            else:
                url = args['<url>']
                
        else:
            print(__doc__)
            print(Fore.RED + "\n" + "error: please provide URL or artist/album.")
            exit()

        # "1 2 3" >> [1, 2, 3]
        if args["--exclude"]:
            exclude = [int(n) for n in args["--exclude"].split()]
        else:
            # None is not iterable, using []
            exclude = []
            
        #if args["--get-art"]:
            

    # or not.
    else:
        print(__doc__)
        print(Fore.RED + "\n" + "error: please provide arguments.")
        exit()

    ######################## <DIRECTORY CHANGING> ########################

    # mkdir *"--folder" if needed
    if not os.path.exists(args["--folder"]):
        show_status("creating directory \"{}\"".format(args["--folder"]))
        os.makedirs(args["--folder"])
        
        if os.path.exists(args["--folder"]):
            show_status()
        else:
            show_status(status = Fore.RED + "failed")
            print(__doc__)
            exit()
            
    # cd *"--folder"
    show_status("changing directory to \"{}\"".format(args["--folder"]))
    os.chdir(os.path.join(os.getcwd(), args["--folder"]))
    
    if os.path.split(os.getcwd())[-1] == args["--folder"]:
        show_status()
    else:
        show_status(status = Fore.RED + "failed")
        print(__doc__)
        exit()
        
    ########################
        
    # "%album% - %title%"
    album_name = list(url.replace("http://", "").replace(".bandcamp.com/album/", "|").split("|"))
    if album_name[1].endswith("/"):
        album_name[1] = album_name[1].replace("/", "")
        
    folder_name = "{} - {}".format(*album_name)
        
    # mkdir *foldername if needed
    if not os.path.exists(folder_name):
        show_status("creating directory \"{}\"".format(folder_name))
        os.makedirs(folder_name)
        
        if os.path.exists(folder_name):
            show_status()
        else:
            show_status(status = Fore.RED + "failed")
            print(__doc__)
            exit()
            
    # cd *folder_name
    show_status("changing directory to \"{}\"".format(folder_name))
    os.chdir(os.path.join(os.getcwd(), folder_name))
    
    if os.path.split(os.getcwd())[-1] == folder_name:
        show_status()
    else:
        show_status(status = Fore.RED + "failed")
        print(__doc__)
        exit()
        
    ######################## </DIRECTORY CHANGING> ########################
    
    # start
    Bandcamp.download(url, args["--get-art"], exclude)

    
