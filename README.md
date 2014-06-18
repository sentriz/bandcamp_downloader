bandcamp_dlr.py
=============

bandcamp_dlr is a python 3+ script for downloading, renaming, and tagging albums from [Bandcamp](http://bandcamp.com/).

You must supply the script and artist, and an album name. These must be exactly how you see them in the album url.

http://**artist**.bandcamp.com/album/**album-name**/

Installation
-----------

	pip install -r requirements.txt
	python bandcamp_dlr.py --help
	

Requirements
-----

jsobj (**(c)** 2013 *darkf*, **included**) (website parsing)

[mutagen](https://pypi.python.org/pypi/mutagen) (mp3 tagging).

[slimit](https://pypi.python.org/pypi/slimit) (required by jsobj).

[wgetter](https://pypi.python.org/pypi/wgetter) (downloading files).

[colorama](https://pypi.python.org/pypi/colorama) (CLI colours).

--

Please note, you can download all of these in one step with

    pip install -r requirements.txt

Usage
-----
    bandcamp_dlr.py (<url> | --artist=<name> --album=<name>)
                    [--get-art] [--folder=<name>] [--exclude=<list>]

Options
-----
    -h, --help       Show this screen.
    -v, --version    Show version.
    --get-art        Download album artwork.
    --folder=<name>  Name of download folder [default: bandcamp_downloads].
    --exclude=<list> List of tracks to exclude from download. (seperated by a space)

Examples
-----
no, these artists are *not* on Bandcamp

    bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --get-art
    bandcamp_dlr.py --artist="the-doors" --album="la-woman" --folder="My Music"
    bandcamp_dlr.py --artist="pinkfloyd" --album="dsotm" --exclude="3 5 7"
	
Note
-----

Please note, I do not intend this script rip off emerging Bandcamp artists.

This script is useful to listen to Bandcamp albums on-the-go offline as a **try before you buy**.

Support Bandcamp artists if you like what you hear.