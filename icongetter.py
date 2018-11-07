import os.path

images = {'saving', 'sequences', 'webp', 'local', 'gif', 'reading', 'tga', 'im', 'images', 'icns', 'ico', 'msp', 'bmp',
          'eps', 'jpeg', 'tiff', 'png', 'spider', 'pcx', 'ppm', 'sgi', 'xbm', 'jpg'}


def extension(filename):
    # trick for py2/3 compatibility
    if 'basestring' not in globals():
        basestring = str

    if isinstance(filename, basestring):

        if os.path.isdir(filename):
            return "icons/dir.png"
        else:
            if os.path.splitext(filename)[1][1:] in images:
                return filename
            iconpath = "icons/" + os.path.splitext(filename)[1][1:] + ".png"
            if os.path.isfile(iconpath):
                return iconpath
            else:
                return 'icons/_blank.png'

    elif all(isinstance(item, basestring) for item in filename):
        list = []
        for item in filename:
            if os.path.isdir(item):
                list.append("icons/dir.png")
            else:
                iconpath = "icons/" + os.path.splitext(item)[1][1:] + ".png"
                if os.path.isfile(iconpath):
                    list.append(iconpath)
                else:
                    list.append("icons/_blank.png")
        return list

    else:
        raise TypeError  # or something along that line

# print(extension('/home/manny/Desktop/Redacted_Transcript.pdf'))
