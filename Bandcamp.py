import urllib.request
import wgetter
import os
import mutagen.mp3, mutagen.id3 
import jsobj
import colorama
from colorama import Fore, init

colorama.init(autoreset = True)
last_message = None

# "doing task ... DONE"
# "doing another task ... DONE"
def show_status(message = "", status = Fore.GREEN + "done"):
    global last_message
    print(message + " ... ", end = "")
    if last_message:
        print("\r" + last_message + " ... " + status)
        last_message = None
    else:
        last_message = message

# not using command line?
# download("http://URL", True, [1, 2])

def download(url, get_art = False, exclude = None): #{

    def write_tags(filename, track_num): #{
        """
        > write tags to filename
        * not using EasyID3 because download() downloads files with no tags.
        """
        
        # aesthetics
        print("[{}] writing id3 tags ...".format(filename))
        print("  {}  ".format("-"*(19 + len(filename))))
        
        # ID3v2.4 tag ID as key, track metadata as values in dict "tags"
        tags = {
            "TIT2": (album_meta["tracks"][track_num - 1][1], "title"),
            "TPE1": (album_meta["artist"], "artist"),
            "TPE2": (album_meta["album_artist"], "album artist"),
            "TRCK": ("{}/{}".format(
                album_meta["tracks"][track_num - 1][0], album_meta[\
                    "total_tracks"]), "track no./total"),
            "TYER": (album_meta["year"], "year"),
            "TALB": (album_meta["title"], "album")
            }

        # tag track with the help of dict "tags" and getattr()()
        track = mutagen.mp3.MP3(filename)
        for tag, tuple in tags.items():
            value, name = tuple
            track[tag] = getattr(mutagen.id3, tag)(encoding = 3, text = [value])
            print("[{}] {}: \"{}\"".format(filename, name, value))
        track.save()

        # aesthetics
        print("  {}  ".format("-"*(19 + len(filename))))
        show_status("[{}] writing id3 tags ...".format(filename))
        show_status()
    #}
        
    def download_art(url): #{
        raw_file = wgetter.download(url)
        os.rename(raw_file, "front.jpg")
    #}

    # open page, decode it, store it as data, close it
    try:
        show_status("attempting to open URL")
        page = urllib.request.urlopen(url)
        show_status()
    except urllib.error.URLError:
        show_status(status = Fore.RED + "failed")
        print(__doc__)
        exit()
    data = page.read().decode("utf-8")
    page.close()

    # split page
    show_status("stripping page")
    data = data.split("var TralbumData = {\n")[-1]
    data = data[0:data.index("};")]
    data = jsobj.read_js_object("var bcd = {" + data + "};")
    show_status()

    show_status("sorting data")
    album_meta = {
        "title": data["bcd"]["current"]["title"],
        "artist": data["bcd"]["artist"],
        "album_artist": data["bcd"]["artist"],
        "tracks": [],
        "total_tracks": len(data["bcd"]["trackinfo"]),
        "year": data["bcd"]["album_release_date"].split(" ")[2],
        "art_url": data["bcd"]["artFullsizeUrl"]
    }

    # fill in "tracks" of album_meta
    for track in data["bcd"]["trackinfo"]:
        album_meta["tracks"].append(
            (int(track["track_num"]), track["title"], track["file"]["mp3-128"])
                )
    
    show_status()

    # {tracks: [(track no., title, url), (track no., title, url)]}
    #            <         0         >    <         1         >
    #            <   0   >  < 1 >  <2>    <   0   >  < 1 >  <2>
            

    for track in album_meta["tracks"]:
        track_num, title, url = track
        show_status("downloading track \"{}\" (#{})".format(title, track_num))
        if track_num not in exclude:
            show_status(status = "")
            raw_file = wgetter.download(url)
            show_status("downloading track \"{}\" (#{})".format(title, track_num))
            show_status()
            new_file = "{}. {}.mp3".format(track_num, title)
            show_status("renaming file to \"{}\"".format(new_file))
            os.rename(raw_file, new_file)
            show_status()
            
            write_tags(new_file, track_num)
        else:
            show_status(status = Fore.RED + "skipped")
            
    if get_art:
        show_status("downloading artwork")
        download_art(album_meta["art_url"])
        show_status()
        
#}
        
    
# TODO:
#     - make bulletproof
#     - more try/except
