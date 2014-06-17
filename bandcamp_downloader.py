import urllib.request
import wgetter
import os
import mutagen.mp3, mutagen.id3 
import jsobj

def get_data(artist, album, get_art = True):
    print("loading...")

    try:
        url = "http://{}.bandcamp.com/album/{}/".format(artist, album)
    except IndexError:
        print("please supply correct artist, and album.")
        return

    # open page, decode it, store it as data, close it
    page = urllib.request.urlopen(url)
    data = page.read().decode("utf-8")
    page.close()

    # split page
    data = data.split("var TralbumData = {\n")[-1]
    data = data[0:data.index("};")]
    data = jsobj.read_js_object("var TralbumData = {" + data + "};")

    album_info = {
        "title": data["TralbumData"]["current"]["title"],
        "artist": data["TralbumData"]["artist"],
        "album_artist": data["TralbumData"]["artist"],
        "tracks": [],
        "total_tracks": len(data["TralbumData"]["trackinfo"]),
        "year": data["TralbumData"]["album_release_date"].split(" ")[2],
        "art_url": ""
    }

    # fill in "art_url" if get_art == True
    if get_art:
        album_info["art_url"] += data["TralbumData"]["artFullsizeUrl"]

    # fill in "tracks" of album_info
    for track in data["TralbumData"]["trackinfo"]:
        album_info["tracks"].append(
            (track["track_num"], track["title"], track["file"]["mp3-128"])
                )

    return album_info

def download(data, exclude = None):
    """
    > download
    """

    folder_name = "bandcamp_downloads"
    album_name = "{} - {}".format(data["artist"], data["title"])

    if os.getcwd() != os.path.expanduser("~"):
        os.chdir(os.path.expanduser("~"))

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(os.path.join(os.getcwd(), folder_name))    # cd "bandcamp_downloads"

    if not os.path.exists(album_name):
        os.makedirs(album_name)                         # mkdir "%album_artist% - %album_title%"
    os.chdir(os.path.join(os.getcwd(), album_name))     # cd "%album_artist% - %album_title%"

    # {tracks: [(track no., title, url), (track no., title, url)]}
    #            <         0         >    <         1         >
    #            <   0   >  < 1 >  <2>    <   0   >  < 1 >  <2>

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


def write_tags(filename, data, track_num):
    """
    > write tags to filename
    * not using EasyID3 because download() downloads files with no tags.
    """
    print("[{}] writing id3 tags ...".format(filename))
    print("  {}  ".format("-"*(19+len(filename))))

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

    track = mutagen.mp3.MP3(filename)
    for tag, string in tags.items():
        track[tag] = getattr(mutagen.id3, tag)(encoding = 3, text = [string[0]])
        print("[{}] {}: \"{}\"".format(filename, string[1], string[0]))
    track.save()

    print("  {}  ".format("-"*(19+len(filename))))
    print("[{}] done ...\n\n".format(filename))

if __name__ == "__main__":

    # http://[artist].bandcamp.com/album/[album]/
    artist, album = "homeshake", "dynamic-meditation"

    download(get_data(artist, album, get_art = False), exclude = [])
