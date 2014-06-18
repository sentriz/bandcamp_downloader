"""
Bandcamp Downloader by sentriz.

Usage:
  bandcamp_dlr.py (<url> | --artist=<name> --album=<name>)
                  [--get-art] [--folder=<name>] [--exclude=<list>]

Options:
  -h, --help       Show this screen.
  -v, --version    Show version.
  --get-art        Download album artwork.
  --folder=<name>  Name of download folder [default: bandcamp_downloads].
  --exclude=<list> List of tracks to exclude from download. (seperated by a space)

Examples:
  * no, these artists are /not/ not on Bandcamp *
  bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --get-art
  bandcamp_dlr.py --artist="the-doors" --album="la-woman" --folder="My Music"
  bandcamp_dlr.py --artist="pinkfloyd" --album="dsotm" --exclude="3 5 7"
"""

from docopt import docopt
from Bandcamp import Bandcamp


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
            url = args['<url>']

            # fixes = {
                # 'bandcamp':
                    # ('badncamp', 'bbandcamp', 'bandcmap'),
                # 'album':
                    # ('alubm', 'albun', 'abulm')
                # }

            # for right in fixes.items():
                # for wrong in right[1]:
                    # if wrong in url:
                        # url = url.replace(wrong, right[0])

            # was it a valid URL?
            if not "bandcamp" in url and not "album" in url and \
                url.startswith("http://"):
                    print(__doc__)
                    print("\n" + "error: invalid URL.")
                    exit()
        else:
            print(__doc__)
            print("\n" + "error: please provide URL or artist/album.")
            exit()

        if args["--exclude"]:
            exclude = args["--exclude"].split()
        else:
            exclude = None

    # or not.
    else:
        print(__doc__)
        print("\n" + "error: please provide arguments.")
        exit()

    bandcamp = Bandcamp(
        url,
        get_art = args["--get-art"],
        folder = args["--folder"],
        exclude = exclude
        )
    bandcamp.download()
