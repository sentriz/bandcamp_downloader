
![!](.logo.png)

**bandcamp_dlr** is a python *3+* script for downloading, renaming, and tagging albums from [Bandcamp](http://bandcamp.com/).  
You must supply the script an artist and an album name. These must be exactly how you see them in the album url.  
http://**artist**.bandcamp.com/album/**album_name**/

###### note: this software has only been tested on Python 3.4.0, please report any issues you may have on earlier Python 3 versions

Installation
-----------
    pip install -r requirements.txt
    python bandcamp_dlr.py --help


Third party modules
-----

#### required ####

|name/link|use|
|--|--|
|[docopt](https://pypi.python.org/pypi/docopt)|argument parsing|
|[mutagen](https://pypi.python.org/pypi/mutagen)|mp3 tagging|
|[slimit](https://pypi.python.org/pypi/slimit)|JavaScript minifier|

#### included ####

|name/link|use|author|
|:--|:--|--:|
|[wgetter](https://pypi.python.org/pypi/wgetter)|simple file downloading|(c) *phoemur*|
|[jsobj](https://github.com/darkf/py-js-object-parser)|JavaScript object literal reading|(c) *darkf*|
|[colorama](https://pypi.python.org/pypi/colorama)|CLI colours|(c) *tartley*|

--

Please note, you can download the required modules in one step with:

    pip install -r requirements.txt

Usage
-----
    bandcamp_dlr.py (<url> | --artist <name> --album <name>)
                    [--save-art | --embed-art] [--folder <name>] [--exclude <list>]
                    [--help] [--version]

Options
-----
    --embed-art      Embed album artwork
    --exclude <list> List of tracks to exclude from download. (seperated by ",")
    --folder <name>  Name of download folder [default: downloads]
    --save-art       Download album artwork

    -h, --help       Show this screen
    -v, --version    Show version

Examples
-----
    bandcamp_dlr.py http://frank-zappa.bandcamp.com/album/hot-rats/ --get-art
    bandcamp_dlr.py --artist="the-doors" --album="la-woman" --folder="My Music"
    bandcamp_dlr.py --artist="pinkfloyd" --album="dsotm" --exclude="3, 5, 7"

API Example
-----
````python
import Bandcamp

album = Bandcamp.Album(
    url = "http://{artist}.bandcamp.com/album/{album}",
    # "save" or "embed" album artwork
    save_or_embed = "save",
    # a list of integers to exclude when downloading
    # "exclude = [1, 2]", for example, will exclude tracks 1 and 2
    exclude = [],
    # download tracks to folder "downloads"
    download_folder_name = "downloads"
)
print(album.title + " by " + album.artist)
album.download()
````

FAQ
-----

* *Download has stopped at x%, help?*  
    Send your shell a KeyboardInterrupt. ^C, ^Z, ect.

* *Will this software work on any OS?*  
    It has only been tested on a Windows machine (so far), but it has been developed in a way that should make it cross-platform. (but not cross-pyversion)

Terms of service/use
-----

By using the script above, you acknowledge and agree to the following terms of service/use:  
1.   Do not use this script to download copyrighted audio.  
2.   High quality audio is not guaranteed; the script uses audio provided by Bandcamp.  
Piracy: I do not condone piracy in any form. My goal that this tool be used to obtain legal audio that would otherwise be extremely difficult to find. Bandcamp is a good source for these audio clips and allows new artists to showcase their work and earn a rightful income from it.  
*To ensure the survival of this tool and to help the artists who are providing the music, please buy their singles/albums directly from Bandcamp.*  
