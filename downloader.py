import os, time
import urllib, posixpath

def download_uri(uri, app="", fmt="mobi"):
    filename = ".booksnake_" + str(int(time.time())) + "." + fmt

    if app == '':
        filename, _ = urllib.urlretrieve(uri, filename)
    elif app == 'aria':
        os.system("aria2c '" + uri + "' -o " + filename)
    elif app == 'curl':
        filename
        os.system("curl '" + uri + "' -o " + filename)
    elif app == 'wget':
        os.system("wget '" + uri + "' -O " + filename)

    return filename
