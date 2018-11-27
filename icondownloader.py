import os
import time
import re
import logging
import urllib.request
import urllib.error


from PIL import Image
import requests
from io import BytesIO
from multiprocessing import Pool
from user_agent import generate_user_agent


def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = generate_user_agent()
        headers['Referer'] = 'https://www.google.com'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        return str(resp.read())
    except:
        pass
        return None


def parse_page(url, verbose=False):
    page_content = download_page(url)
    if page_content:
        link_list = re.findall('"ou":"(.*?)"', page_content)
        if len(link_list) == 0:
            if verbose == True:
                print('get 0 links from page {0}'.format(url))
            logging.info('get 0 links from page {0}'.format(url))
            return set()
        else:
            return set(link_list)
    else:
        return set()


def download_images(main_keyword, verbose =False):

    stored_images = os.listdir("pop_icons/")
    try:
        for stored_image in stored_images:
            if stored_image == main_keyword + ".png":
                img = Image.open("pop_icons/" +stored_image)
                img.load()
                if img != None:
                    return img
                else:
                    break
    except OSError as e:
        print("OSError,", e)
        print(main_keyword,stored_image )
        pass
    search = main_keyword + " software logo icon png,g_1:transparent,online_chips:logo"


    url = 'https://www.google.com/search?q=' + search.replace(' ', '%20') + '&source=lnt&tbs=ic:trans&'
    image_links = parse_page(url)
    if verbose == True:
        print('Process {0} get {1} links so far'.format(os.getpid(), len(image_links)))
    time.sleep(2)

    if verbose == True:

        print ("Process {0} get totally {1} links".format(os.getpid(), len(image_links)))

    if verbose == True:
        print ("Testing...")
    count = 1
    for link in image_links:
        try:
            if ".png" in link:
                response = requests.get(link)
                img = Image.open(BytesIO(response.content))
                img.load()
                if img != None:
                    img.save('pop_icons/'+main_keyword + ".png","PNG")
                    return img
        except:
            pass


