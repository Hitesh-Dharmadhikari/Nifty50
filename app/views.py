from django.shortcuts import redirect, render, Http404, HttpResponse
import json
import traceback
#import urllib2
import redis
import datetime
from django.conf import settings

NIFTY_GAINER_SCRAPPER_URL = settings.SCRAPPER_URL.get('nifty_gainer', '')
NIFTY_LOSER_SCRAPPER_URL = settings.SCRAPPER_URL.get('nifty_loser', '')
POOL = redis.ConnectionPool(host='localhost', port=8000, db=0)
r_server = redis.StrictRedis(connection_pool=POOL)
API_TIME_DIFF = settings.API_TIME_DIFF


def index(request):
    if request.method == "GET":
        gainer_json , loser_json = check_and_save_in_redis()
        gainer_value = json.load(gainer_json)
        loser_value = json.load(loser_json)
        print(gainer_value)
        print(loser_value)
        return render(request, 'index.html', {'gainer_data' : json.dumps(gainer_json),
                                             'loser_data': json.dumps(loser_json)})


def get_data_from_nifty(gainer_flag, loser_flag):
    gainer_json = {}
    loser_json = {}
    header = {'User-Agent': 'Mozilla/5.0'}
    if gainer_flag:
        #req = urllib2.Request(NIFTY_GAINER_SCRAPPER_URL, headers=header)
        gainer_json = urlopen(NIFTY_GAINER_SCRAPPER_URL).read()
        gainer_json = json.loads(gainer_json)
    if loser_flag:
      #  req = urllib2.Request(NIFTY_LOSER_SCRAPPER_URL, headers=header)
        loser_json = urlopen(NIFTY_LOSER_SCRAPPER_URL).read()
        loser_json = json.loads(loser_json)
    return gainer_json, loser_json


def process_gainer_loser_data(request):
    gainer_json, loser_json = check_and_save_in_redis()
    response_nifty = {}
    response_nifty['gainer_json'] = gainer_json
    response_nifty['loser_json'] = loser_json
    return HttpResponse(json.dumps({'response': 'success',
                                    'response_nifty': response_nifty}))

def check_and_save_in_redis():
    gainer_key = 'gainer_data'
    loser_key = 'loser_data'
    gainer_data = r_server.get(gainer_key)
    loser_data = r_server.get(loser_key)
    if not gainer_data:
        gainer_data , loser_data = get_data_from_nifty(True, False)
        r_server.set(gainer_key, gainer_data)
    else:
        gainer_data = eval(gainer_data)
        server_time = datetime.datetime.strptime(gainer_data.get('time'), '%b %d, %Y %I:%M:%S')
        current_system_time = datetime.datetime.now()
        adjusted_time =  current_system_time - datetime.timedelta(minutes=5)
        if adjusted_time > server_time:
            gainer_data, loser_data = get_data_from_nifty(True, False)
            r_server.set(gainer_key, gainer_data)
    if not loser_data:
        gainer_data_dummy, loser_data = get_data_from_nifty(False, True)
        r_server.set(loser_key, loser_data)
    else:
        loser_data = eval(loser_data)
        server_time = datetime.datetime.strptime(loser_data.get('time'), '%b %d, %Y %I:%M:%S')
        current_system_time = datetime.datetime.now()
        adjusted_time = current_system_time - datetime.timedelta(minutes=5)
        if adjusted_time > server_time:
            gainer_data_dummy, loser_data = get_data_from_nifty(False, True)
            r_server.set(loser_key, loser_data)
    return gainer_data,loser_data





