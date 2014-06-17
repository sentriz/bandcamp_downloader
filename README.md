bandcamp_dlr.py
=============

bandcamp_dlr is a python script for downloading, renaming, and tagging albums from [Bandcamp](http://bandcamp.com/).

You must supply the script and artist, and an album name. These must be exactly how you see them in the album url.

http://**artist**.bandcamp.com/album/**album-name**/

Installation
-----------

	pip install -r requirements.txt
	bandcamp_dlr --help
	

Requirements
-----

jsobj ((c) 2013 darkf, included) -website parsing.

[mutagen](https://pypi.python.org/pypi/mutagen/1.12) (1.23) -mp3 tagging.

[slimit](https://pypi.python.org/pypi/slimit) (0.8.1) -required by jsobj.

[wgetter](https://pypi.python.org/pypi/wgetter/) (0.3) -downloading files.

Usage
-----

	bandcamp_dlr artist album-name
	bandcamp_dlr artist album-name [--art] [--dir DIR]
	
Note
-----

Please note, I do not intend this script rip off emerging Bandcamp artists.

This script is useful to listen to Bandcamp albums on-the-go offline as a **try before you buy**.

Support Bandcamp artists if you like what you hear.