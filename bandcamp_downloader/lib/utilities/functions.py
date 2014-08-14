from .aesthetics import show_status
import os
import sys
    
def mk_cd(dir_name):

    try:
        show_status("creating directory \"%dim%{}%bright%\"".format(dir_name))
        os.makedirs(dir_name)
        show_status(status = "%green%done")
    except FileExistsError:
        show_status(status = "%yellow%already exists")
    except (PermissionError, OSError):
        show_status(status = "%red%failed")
        error()
    os.chdir(dir_name)
        
def url_is_valid(url):
    requirements = ["http", "://", ".bandcamp.com", "/album/"] 
    for part in requirements:
        if url.find(part) < 0:
            return False
    return True
    
def error():
    print("- see bandcamp_dlr.py --help")
    print("- ^ that message may not be appropriate")
    sys.exit(1)
    
if __name__ == "__main__":

    # damn relative imports ..
    # running this as __main__ won't work anymore.
    # anyone wanna tell me what's going on? :)
    
    mk_cd("test_folder")
    mk_cd("test_folder_in_test_folder")
    
    print(url_is_valid("http://artist.bandcamp.com/album/album"))
    print(url_is_valid("http://artist.bindcomp.com/album/album"))
    print(url_is_valid("https://artist.bandcamp.com/album/album/"))
    print(url_is_valid("http://artist.bandcamp.com/alboom/album"))
    print(url_is_valid("http:/artist.bandcamp.com/album/album"))