import time
import threading

gweek = 1
gday = 1
ghour = 1
gmini = 1
gsecond = 0


def my_time():
    global gsecond, gmini, gweek, gday, ghour
    gsecond += 1
    if gsecond == 60 and gmini != 59:
        gsecond = 0
        gmini += 1
    elif gsecond == 60 and gmini == 59 and ghour != 23:
        gsecond = 0
        gmini = 0
        ghour += 1
    elif gsecond == 60 and gmini == 59 and ghour == 23 and gday != 7:
        gsecond = 0
        gmini = 0
        ghour = 0
        gday += 1
    elif gsecond == 60 and gmini == 59 and ghour == 23 and gday == 7:
        gsecond = 0
        gmini = 0
        ghour = 0
        gday = 1
        gweek += 1
    print(gweek, gday, ghour, gmini, gsecond)
    threading.Timer(0.00000001, my_time).start()
