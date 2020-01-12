#!/home/cbyte/.virtualenvs/bing/bin/python
import requests
import os
import sys
import shutil
from os.path import expanduser
from os import listdir
from requests.exceptions import ConnectionError
def changeImage(arg=""):
    home = expanduser("~")
    if(arg != ""): 
        get_env(arg)
    else:
        try:
            resp = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
            j = resp.json()
            urlBase = "https://www.bing.com"
            resolution = os.popen("xrandr | awk '/*/ {print $1}'").read()
            try:
                if(os.path.exists(home+"/wallpaper")==False):
                    os.mkdir(home+"/wallpaper")
                    print(os.path.exists(home+"/wallpaper"))
            except Exception as e:
                print(e)

            if resp.status_code == 200:
                for i in j['images']:
                    urlpart=i['url']
                    res = requests.get(urlBase+urlpart.replace("_1920x1080", "_"+resolution[:-1]), stream=True)
                    print(i['title'])
                    with open(home+ f'/wallpaper/{i["title"]}.jpg','wb') as out_file:
                        shutil.copyfileobj(res.raw, out_file)
                    del resp
                    get_env(actualImage=i['title'])

                    #print(urlBase+urlpart.replace("_1920x1080", "_"+resolution[:-1]))
        except ConnectionError as e:
            print("Connection Error!")
def get_env(image="",actualImage=""):
    home = expanduser('~')
    if (image ==""):
        env_session = os.environ.get("DESKTOP_SESSION")
        if("xfce" in env_session):
            os.system(f'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s "{home}/wallpaper/{actualImage}.jpg"')
            print("Background Changed!")
            
        elif("ubuntu" in env_session):
            os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {home}/wallpaper/{actualImage}.jpg")
            print("Background Changed!")
        else:
            print("NO - Some error")
    else:
        env_session = os.environ.get("DESKTOP_SESSION")
        if("xfce" in env_session):
            os.system(f'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s {home}/wallpaper/old/{image}.jpg')
            print("Background Changed!")
        elif("ubuntu" in env_session):
            os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {home}/wallpaper/{image}.jpg")
            print("Background Changed!")
        else:
            print("NO - Some error")

def save_Image(arg):
    home = expanduser('~')
    urlBase = "https://www.bing.com"
    resolution = os.popen("xrandr | awk '/*/ {print $1}'").read()
    try:
        resp = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
        j = resp.json()
        if resp.status_code == 200:
            for i in j['images']:
                urlpart=i['url']
                res = requests.get(urlBase+urlpart.replace("_1920x1080", "_"+resolution[:-1]), stream=True)
                with open(home+ f'/wallpaper/old/{arg}.jpg','wb') as out_file:
                        shutil.copyfileobj(res.raw, out_file)
            print("Image saved !")
    except ConnectionError :
        print("Connection Error!")
    
def remove_Image(arg):
    home = expanduser("~")
    answer = input("Do you really want to delete the file [y or n]")
    if(answer == "y"):
        if os.path.exists(home+ f'/wallpaper/old/{arg}.jpg'):
            os.remove(home+ f'/wallpaper/old/{arg}.jpg')
            print("The file is deleted!")
        else:
            print("The file doesn't exist!")
    else:
        return
def main(argv):
    home = expanduser('~')
    files = [f for f in listdir(home+'/wallpaper/old')]
    try:
        if (argv==[]):
            changeImage(arg="")
        elif(argv[0] == '-ls'):
            for f in files:
                print(f)
        elif(argv[0] == "-s"):
            changeImage(arg="")
            save_Image(argv[1])
        elif(argv[0] == "-r"):
            remove_Image(argv[1])
        
        else:
            changeImage(argv[0])
    except:
        print("Argument error! (Wrong or missing argument))")

if __name__ == "__main__" : main(sys.argv[1:])
