import os, time
import urllib

def download_uri(uri, app="", save_as="ebook"):
    if app == '':
        filename, _ = urllib.urlretrieve(urllib2.quote(uri))
        return filename

    if app == 'aria':
        os.system("aria2c '" + uri + "'")
    elif app == 'curl':
        filename
        os.system("curl '" + uri + "' -o " + str(int(time.time())) + ".ebook-download")
    elif app == 'wget':
        os.system("wget '" + uri + "'")

    return
