import sys
import time
import requests

from threading import Thread

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
    try:
        response = requests.get(url)
        moments = response.json()["moments"]
        for moment in moments:
            first_half = moment[0] <= 2
            objects = moment[5]
            ball_object = objects[0]
            #if ball_object[4] < 7.0 and ((first_half and ball_object[2] > 50) or (not first_half and ball_object[2] <= 50)):
            #ball_scatter_x.append(ball_object[2])
            #ball_scatter_y.append(ball_object[3])
        print len(moments)
    except:
        print "error"

url_queue = Queue(NUM_CONCURRENT * 2)
for i in range(NUM_CONCURRENT):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

add_urls_to_queue()
url_queue.join()

