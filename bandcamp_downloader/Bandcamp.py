from lib.utilities.aesthetics import colour
from lib.utilities.aesthetics import show_status
from lib.utilities.aesthetics import pretty_print
from lib.utilities.debugging import debugmethods
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen
import lib.utilities.jsobj as jsobj
import lib.utilities.wgetter as wgetter
import mutagen.id3
import mutagen.mp3
import os
import sys

#@debugmethods
class Album:

    def __init__(self, url, save_or_embed, exclude, download_folder_name):
        self.config = {
            "url": url,
            "save_or_embed": save_or_embed,
            "exclude": exclude,
            "download_folder_name": download_folder_name
        }
        
        data = self._get_data()
        show_status("sorting data")
        
        self.album_artist = data["_"]["artist"]
        self.art_url = data["_"]["artFullsizeUrl"]
        self.artist = data["_"]["artist"]
        self.title = data["_"]["current"]["title"]
        self.total_tracks = len(data["_"]["trackinfo"])
        self.tracks = []
        self.year = data["_"]["album_release_date"].split(" ")[2]
        
        for track in data["_"]["trackinfo"]:
            self.tracks.append({
                "track_num": int(track["track_num"]), 
                "title": track["title"],
                "url": track["file"]["mp3-128"]
            })
            
        show_status(status = "%green%done")
        
    def _write_tags(self, filename, track_num):
        """
        > write ID3 tags to .mp3 files.
        * 
        """
        pretty_print("writing id3 tags for file \"{}\"".format(filename))

        tags = {
            # "KEY": (tag, "tag name")
            "TALB": (self.title, "album"),
            "TIT2": (self.tracks[track_num]["title"], "title"),
            "TPE1": (self.artist, "artist"),
            "TPE2": (self.album_artist, "album artist"),
            "TRCK": ("{}/{}".format(self.tracks[track_num]["track_num"], 
                self.total_tracks), "track no./total"),
            "TYER": (self.year, "year")
        }

        track = mutagen.mp3.MP3(filename)
        for tag, tuple in tags.items():
            value, name = tuple
            track[tag] = getattr(mutagen.id3, tag)(encoding=3, text=value)
            print("- {}: \"{}\"".format(name, value))
        track.save()
        
    def _get_data(self, user_agent=None): #{
        user_agent = user_agent or "Mozilla/5.0 (compatible; MSIE 9.0;" \
            " Windows NT 6.1; Win64; x64; Trident/5.0)"

        try:
            show_status("downloading webpage")
            req = Request(self.config["url"], headers = {"User-Agent": user_agent})
            response = urlopen(req)
            data = response.read()
            response.close()
            show_status(status = "%green%done")
        except URLError as e:
            if hasattr(e, "reason"):
                print("er")
                show_status(status = "%red%failed to reach a server." \
                    " reason: \"{}\"".format(e.reason))
            elif hasattr(e, "code"):
                print("er")
                show_status(status = "%red%server couldn't fulfil the request." \
                    " code: \"{}\"".format(e.code))
            sys.exit(1)
        
        data = data.decode(sys.stdout.encoding)
        show_status("stripping page")
        data = data.split("var TralbumData = {\n")[-1]
        data = data[0:data.index("};")]
        show_status(status = "%green%done")
        
        return jsobj.read_js_object("var _ = {" + data + "};")
        
    def _download_tracks(self):
        for track in self.tracks:
            if track["track_num"] not in self.config["exclude"]:
                pretty_print("%green%downloading %reset%track #{} \"{}\" ".format(
                    track["track_num"], track["title"])
                )
                raw_file = wgetter.download(track["url"])
                new_file = "{}. {}.mp3".format(track["track_num"], track["title"])
                os.rename(raw_file, new_file)
                self._write_tags(new_file, track["track_num"] - 1)
            else:
                pretty_print("%red%skipping %reset%track #{} \"{}\" ".format(
                    track["track_num"], track["title"])
                )

    def _download_art(self):
        try:
            pretty_print("%green%downloading %reset%artwork")
            raw_file = wgetter.download(self.art_url)
            os.rename(raw_file, "front.jpg")
        except (FileNotFoundError, FileExistsError):
            pretty_print("%red%failed %reset%to download (or rename) artwork")
        finally:              
            if os.path.isfile(raw_file):
                os.remove(raw_file)
                
    def _embed_art(self):
        pretty_print("%dim%downloading temporary artwork to embed")
        raw_file = wgetter.download(self.art_url)
        
        all_tracks = [file for file in os.listdir() if \
            os.path.splitext(file)[1] == ".mp3"]
        for track in all_tracks:
            muta_track = mutagen.mp3.MP3(track)
            muta_track["APIC:Cover"] = mutagen.id3.APIC(
                encoding = 3,
                mime = "image/jpeg",
                type = 3,
                desc = "Cover",
                data = open(raw_file, "rb").read()
            )
            muta_track.save()
            pretty_print("%dim%embeded artowork for track \"{}\"".format(track))
        try:
            os.remove(raw_file)
            pretty_print("%dim%deleted temporary artwork")
        except (PermissionError, OSError):
            show_status("%dim%%red%failed %reset%to delete temporary art file " + raw_file)
        
    def _mk_cd(self, dir_name):
        try:
            show_status("creating directory \"%dim%{}%bright%\"".format(dir_name))
            os.makedirs(dir_name)
            show_status(status = "%green%done")
        except FileExistsError:
            show_status(status = "%yellow%already exists")
        except (PermissionError, OSError):
            show_status(status = "%red%failed")
            sys.exit(1)
        os.chdir(dir_name)
         
    # start
    def download(self):
        # make and change directories
        self._mk_cd(self.config["download_folder_name"])
        self._mk_cd("{} - {}".format(self.artist, self.title))
        
        self._download_tracks()
        if self.config["save_or_embed"] == "save":
            self._download_art()
        elif self.config["save_or_embed"] == "embed":
            self._embed_art()

class Track:
    # maybe later
    pass
