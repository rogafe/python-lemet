import re
import requests
import json
import sys
import argparse
from datetime import datetime, date, time, timedelta
#import time
#print("Debug")

def usage():
    print("use -f to force")

def bus():
    url = "https://lemet.fr/helpers/app_script/temps_reel.php?stop=EGLISE&line=3"
    r = requests.get(url)
    # Legacy
    #print(json.loads(r.content), "\n")

    data  = json.loads(r.content)

    now = datetime.now()
    now_time = now.time()

    print("theorique = ", data['next'][0]['theorique'], "\n")

def metis_mercy():
    url = "https://lemet.fr/helpers/app_script/temps_reel.php?stop=GARE&line=b"
    r = requests.get(url)
    #print(json.loads(r.content), "\n")
    data = json.loads(r.content)
    print("theorique = ", data['next'][0]['theorique'], "\n")
    sys.exit()


def print_home(aa):
    r = requests.get(aa)
    data = json.loads(r.content)
    print("Depart bus colson:", data[0]['parcours'][0]['departure_time'], "\n")
    print("Arriver REP", data[0]['parcours'][0]['arrival_time'], "\n")
    print("Depart metis B rep", data[0]['parcours'][1]['departure_time'], "\n")

def home_to_saulcy():

    today = date.today()
    t = today + timedelta(days=1)
    url_tomorow = "https://lemet.fr/helpers/app_script/app_router.php?arret_depart=EGLISE%20(arret)&arret_arrivee=SAULCY%20(arret)&jour={d}-{m}-{y}&heure=06:00&mode=1&typerecherche=1".format(d=t.day, m=t.month, y=t.year)
    url_today = "https://lemet.fr/helpers/app_script/app_router.php?arret_depart=EGLISE%20(arret)&arret_arrivee=SAULCY%20(arret)&jour={d}-{m}-{y}&heure=06:00&mode=1&typerecherche=1".format(d=today.day, m=today.month, y=today.year)
    now = datetime.now()
    now_time = now.time().strftime('%H:%M:%S')
    #print_home(url_tomorow)
    if now_time >= time(00,00):
        print_home(url_today)
    else:
        print_home(url_tomorow)



def l3_rep():
    now = datetime.now()
    now_time = now.time().strftime('%H:%M:%S')
    today = date.today()
    url_next = "https://lemet.fr/helpers/app_script/app_router.php?arret_depart=EGLISE%20(arret)&arret_arrivee=REPUBLIQUE%20(arret)&jour{d}-{m}-{y}&heure={H}:{M}&mode=1&typerecherche=1".format(d=today.day, m=today.month, y=today.year, H=now.hour, M=now.minute)
print(url_next)


def main():
    #force = False
    parser = argparse.ArgumentParser(description='get time of BUS in metz')
    parser.add_argument("-f", help="force",
                        action="store_true")
    parser.add_argument("--mercy", help="get metis from gare to grande ecole",
                        action="store_true")
    parser.add_argument("--saulcy", help="home to saulcy",
                        action="store_true")
    parser.add_argument("--l3rep", help="get next bus from colson to REPUBLIQUE", action="store_true")
    args = parser.parse_args()

    if args.f:
        bus()
    elif args.mercy:
        metis_mercy()
    elif args.saulcy:
        home_to_saulcy()
    elif args.l3_rep:
        l3_rep()
    else:
        now = datetime.now()
        now_time = now.time()
        if now_time >= time(21,00) or now_time <= time(00,00):
            print("the bus dont drive at this time")
            sys.exit()

if __name__ == "__main__":
    main()
