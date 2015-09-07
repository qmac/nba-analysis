import sys
import time
import requests
import csv

from threading import Thread
from threading import Lock

from Queue import Queue

NUM_CONCURRENT = 200

def add_urls_to_queue():
    try:
        for i in range(1, 1230):
            for j in range (1, 600):
                url = "http://stats.nba.com/stats/locations_getmoments/?eventid=%d&gameid=002140%04d" % (j, i)
                url_queue.put(url)
    except KeyboardInterrupt:
        sys.exit(1)

def worker():
    while True:
        url = url_queue.get()
        fetch_url(url)
        print "Done: " + url 
        url_queue.task_done()

def fetch_url(url):
    csv_data = []
    try:
        response_json = requests.get(url).json()
        moments = response_json["moments"]
        home_team = response_json["home"]["abbreviation"]
        away_team = response_json["visitor"]["abbreviation"]
        for moment in moments:
            first_half = moment[0] <= 2
            ball_up_court = moment[3] <= 19.5 # Check the shot clock 

            ball_object = moment[5][0]

            ball_x = ball_object[2]
            ball_y = ball_object[3]
            ball_height = ball_object[4]

            # Filter out shots and before ball is up the court
            if ball_height < 7.0 and ball_up_court:
                # Determine possession by ball location and half
                off_team = ""
                def_team = ""

                if ((first_half and ball_x <= 50) or (not first_half and ball_x > 50)):
                    off_team = home_team
                    def_team = away_team
                else:
                    off_team = away_team
                    def_team = home_team

                csv_data.append([off_team, def_team, ball_x, ball_y])

    except ValueError, KeyError:
        print "error"

    write_to_csv(csv_data)

def write_to_csv(data):
    lock.acquire()
    with open('ball_data.csv', 'a+') as db:
        writer = csv.writer(db, delimiter=',')
        writer.writerows(data)
    lock.release()

lock = Lock()
url_queue = Queue(NUM_CONCURRENT * 2)
for i in range(NUM_CONCURRENT):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

add_urls_to_queue()
url_queue.join()

