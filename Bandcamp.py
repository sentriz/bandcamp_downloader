import urllib.request
import wgetter
import os
import mutagen.mp3, mutagen.id3 
import jsobj
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset = True)

class Bandcamp:
    def __init__(self, url, get_art, folder, exclude):
        self.url = url
        self.get_art = get_art
        self.folder = folder
        self.exclude = exclude
     
    def download():

        # open page, decode it, store it as data, close it
        try:
            page = urllib.request.urlopen(self.url)
        except urllib.error.URLError:
            print(Fore.RED + "\n" + "error: URL does not exist.")
            return
        data = page.read().decode("utf-8")
        page.close()

        # split page
        data = data.split("var TralbumData = {\n")[-1]
        data = data[0:data.index("};")]
        data = jsobj.read_js_object("var bcd = {" + data + "};")

        album_info = {
            "title": data["bcd"]["current"]["title"],
            "artist": data["bcd"]["artist"],
            "album_artist": data["bcd"]["artist"],
            "tracks": [],
            "total_tracks": len(data["bcd"]["trackinfo"]),
            "year": data["bcd"]["album_release_date"].split(" ")[2],
            "art_url": ""
        }

        # fill in "art_url" if get_art == True
        if get_art:
            album_info["art_url"] += data["bcd"]["artFullsizeUrl"]

        # fill in "tracks" of album_info
        for track in data["bcd"]["trackinfo"]:
            album_info["tracks"].append(
                (track["track_num"], track["title"], track["file"]["mp3-128"])
                    )

        album_name = "{} - {}".format(data["artist"], data["title"])

        if os.getcwd() != os.path.expanduser("~"):
            os.chdir(os.path.expanduser("~"))

        if not os.path.exists(folder):
            os.makedirs(folder)
        os.chdir(os.path.join(os.getcwd(), folder))    # cd "bandcamp_downloads"

        if not os.path.exists(album_name):
            os.makedirs(album_name)                         # mkdir "%album_artist% - %album_title%"
        os.chdir(os.path.join(os.getcwd(), album_name))     # cd "%album_artist% - %album_title%"

        # {tracks: [(track no., title, url), (track no., title, url)]}
        #            <         0         >    <         1         >
        #            <   0   >  < 1 >  <2>    <   0   >  < 1 >  <2>
        # track two title: data["tracks"][1][1] (eg)

        for track in data["tracks"]:
            if int(track[0]) not in exclude:
                print("downloading track {}. \"{}\" ...".format(
                    track[0], track[1]))

                raw_file = wgetter.download(track[2])
                new_file = "{}. {} - {}.mp3".format(track[0], data["artist"], track[1])
                os.rename(raw_file, new_file)

                write_tags(new_file, data, int(track[0]))
                
        if data["art_url"]:
            print("downloading artwork ...")
            raw_file = wgetter.download(data["art_url"])
            new_file = "front.jpg"
            os.rename(raw_file, new_file)


    def write_tags(filename, track_num):
        """
        > write tags to filename
        * not using EasyID3 because download() downloads files with no tags.
        """
        
        # print spacer bar
        def spacer(addition = 0):
            return "  {}  ".format("-"*(19+addition))
        
        # aesthetics
        print("[{}] writing id3 tags ...".format(filename))
        print(spacer(len(filename)))
        
        # ID3v2.4 tag ID as key, track metadata as values in dict "tags"
        tags = {
            "TIT2": (data["tracks"][track_num - 1][1], "title"),
            "TPE1": (data["artist"], "artist"),
            "TPE2": (data["album_artist"], "album artist"),
            "TRCK": ("{}/{}".format(
                data["tracks"][track_num - 1][0], data[\
                    "total_tracks"]), "track no./total"),
            "TYER": (data["year"], "year"),
            "TALB": (data["title"], "album")
            }

        # tag track with the help of dict "tags" and getattr()()
        track = mutagen.mp3.MP3(filename)
        for tag, string in tags.items():
            track[tag] = getattr(mutagen.id3, tag)(encoding = 3, text = [string[0]])
            print("[{}] {}: \"{}\"".format(filename, string[1], string[0]))
        track.save()

        # aesthetics
        print(spacer(len(filename)))
        print("[{}] done ...\n\n".format(filename))
    
# TODO:
#     - make bulletproof
#     - more try/except
