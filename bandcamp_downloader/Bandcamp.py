from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import wgetter, jsobj
import os, sys
import mutagen.mp3, mutagen.id3
from show_status import show_status

def download(url, get_art = False, exclude = None): #{

    def write_tags(filename, track_num): #{
        """
        > write tags to filename
        * not using EasyID3 because download() downloads files with no tags.
        """
        
        # aesthetics
        show_status("\n[{}] writing id3 tags ...".format(filename))
        
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

    #}
        
    def download_art(url):
        raw_file = wgetter.download(url)
        os.rename(raw_file, "front.jpg")

    # open page, decode it, store it as data, close it
    def open_url(url, user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"):
    
        try:
            show_status("downloading webpage")
            req = Request(url, headers = {"User-Agent": user_agent})
            response = urlopen(req)
            data = response.read()
            response.close()
            show_status(status = "%green%done")
        except URLError as e:
            if hasattr(e, "reason"):
                show_status(status = "%red%failed to reach a server. reason: \"{}\"".format(e.reason))
            elif hasattr(e, "code"):
                show_status(status = "%red%server couldn't fulfil the request. code: \"{}\"".format(e.code))
            sys.exit(1)
                
        return data.decode(sys.stdout.encoding)

    # split page
    data = open_url(url)
    show_status("stripping page")
    data = data.split("var TralbumData = {\n")[-1]
    data = data[0:data.index("};")]
    data = jsobj.read_js_object("var _ = {" + data + "};")
    show_status()

    show_status("sorting data")
    album_meta = {
        "title": data["_"]["current"]["title"],
        "artist": data["_"]["artist"],
        "album_artist": data["_"]["artist"],
        "tracks": [],
        "total_tracks": len(data["_"]["trackinfo"]),
        "year": data["_"]["album_release_date"].split(" ")[2],
        "art_url": data["_"]["artFullsizeUrl"]
    }

    # fill in "tracks" of album_meta
    for track in data["_"]["trackinfo"]:
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