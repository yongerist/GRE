import time
import threading

gweek = 1
gday = 1
ghour = 7
gmini = 1
gsecond = 0


def my_time():
    global gsecond, gmini, gweek, gday, ghour
    gsecond += 1
    if gsecond == 60 and gmini != 60:
        gsecond = 0
        gmini += 1
        print(gweek, gday, ghour, gmini, gsecond)
    elif gsecond == 60 and gmini == 60 and ghour != 24:
        gsecond = 0
        gmini = 0
        ghour += 1
        print(gweek, gday, ghour, gmini, gsecond)
    elif gsecond == 60 and gmini == 60 and ghour == 24 and gday != 8:
        gsecond = 0
        gmini = 0
        ghour = 0
        gday += 1
        print(gweek, gday, ghour, gmini, gsecond)
    elif gsecond == 60 and gmini == 60 and ghour == 24 and gday == 8:
        gsecond = 0
        gmini = 0
        ghour = 0
        gday = 1
        gweek += 1
        print(gweek, gday, ghour, gmini, gsecond)
    print(gweek, gday, ghour, gmini, gsecond)
    threading.Timer(0.0000000000001, my_time).start()

