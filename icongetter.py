import os.path
from icondownloader import download_images
from PIL import Image

images = {'saving', 'sequences', 'webp', 'local', 'gif', 'reading', 'tga', 'im', 'images', 'icns', 'ico', 'msp', 'bmp',
          'eps', 'jpeg', 'tiff', 'png', 'spider', 'pcx', 'ppm', 'sgi', 'xbm', 'jpg'}


def extension(filename):
    # trick for py2/3 compatibility
    if 'basestring' not in globals():
        basestring = str

    if isinstance(filename, basestring):

        if os.path.isdir(filename):
            return Image.open("icons/dir.png")
        else:
            if os.path.splitext(filename)[1][1:] in images:
                return Image.open(filename)
            if os.path.splitext(filename)[1][1:]  == "desktop":
                img = download_images(os.path.basename(filename).replace('.desktop', ''), verbose= False)
                return img
            iconpath = "icons/" + os.path.splitext(filename)[1][1:] + ".png"
            if os.path.isfile(iconpath):
                return Image.open(iconpath)
            else:
                return Image.open('icons/_blank.png')

    elif all(isinstance(item, basestring) for item in filename):
        list = []
        for item in filename:
            if os.path.isdir(item):
                list.append(Image.open("icons/dir.png"))
            else:
                iconpath = "icons/" + os.path.splitext(item)[1][1:] + ".png"
                if os.path.isfile(iconpath):
                    list.append(Image.open(iconpath))
                else:
                    list.append(Image.open("icons/_blank.png"))
        return list

    else:
        raise TypeError  # or something along that line

# print(extension('/home/manny/Desktop/Redacted_Transcript.pdf'))
