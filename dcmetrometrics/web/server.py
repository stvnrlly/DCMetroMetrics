#!/usr/bin/env python
"""
server.py

Implementation of the DC Metro Metrics server, using bottle.
This module defines the routes for web pages,
and the Bottle Server.

NOTE: Before importing this module, you may have to call:
"from gevent import monkey; monkey.patch_all()"
Otherwise, the Server will not run correctly.
"""

import os
import pymongo
from StringIO import StringIO
from datetime import datetime
from operator import itemgetter
from collections import defaultdict, Counter

# Import bottle
import gevent
from gevent import monkey; monkey.patch_all() # Needed before importing bottle
import bottle
from bottle import static_file
from dcmetrometrics.common.restartingGreenlet import RestartingGreenlet

REPO_DIR = os.environ['OPENSHIFT_REPO_DIR']
DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']
SCRIPT_DIR = os.path.join(REPO_DIR, 'scripts')
STATIC_DIR = os.path.join(REPO_DIR, 'wsgi', 'static')
WEBPAGE_DIR = os.path.join(DATA_DIR, 'webpages')
SHARED_DATA_DIR = os.path.join(DATA_DIR, 'shared')

bottle.TEMPLATE_PATH.append(os.path.join(REPO_DIR, 'wsgi', 'views'))

########################################
@bottle.route('/')
def index():
    filename = 'home.html'
    return static_file(filename, root=WEBPAGE_DIR)

########################################
@bottle.route('/hotcars')
@bottle.route('/hotcars/')
def hotCars():
    filename = 'hotcars.html'
    return static_file(filename, root=WEBPAGE_DIR)

########################################
@bottle.route('/hotcars/<carNum>')
@bottle.route('/hotcars/<carNum>/')
def hotCar(carNum):
    filename = 'hotcar_%s.html'%carNum
    return static_file(filename, root=WEBPAGE_DIR)

########################################
@bottle.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=STATIC_DIR)

########################################
@bottle.route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root=WEBPAGE_DIR)

########################################
@bottle.route('/data')
@bottle.route('/data/')
def data():
    filename = 'data.html'
    return static_file(filename, root=WEBPAGE_DIR)
 
########################################
@bottle.route('/press')
@bottle.route('/press/')
def press():
    filename = 'press.html'
    return static_file(filename, root=WEBPAGE_DIR)

#########################################
@bottle.route('/data/<filename>')
def serve_data(filename):
    return static_file(filename, root=SHARED_DATA_DIR, download=True)

########################################
@bottle.route('/escalators/<unitId>')
@bottle.route('/escalators/<unitId>/')
def genEscalatorStatus(unitId):
    filename = 'escalator_%s.html'%unitId
    return static_file(filename, root=WEBPAGE_DIR)

###############################################
@bottle.route('/stations/<shortName>')
@bottle.route('/stations/<shortName>/')
def stationStatus(shortName):
    filename = 'station_%s.html'%shortName
    return static_file(filename, root=WEBPAGE_DIR)

###############################################
@bottle.route('/escalators/directory')
@bottle.route('/escalators/directory/')
def allEscalators():
    filename = 'escalators.html'
    return static_file(filename, root=WEBPAGE_DIR)

###############################################
@bottle.route('/escalators')
@bottle.route('/escalators/')
@bottle.route('/escalators/outages')
@bottle.route('/escalators/outages/')
def escalatorOutages():
    filename = 'escalatorOutages.html'
    return static_file(filename, root=WEBPAGE_DIR)

###############################################
@bottle.route('/escalators/rankings')
@bottle.route('/escalators/rankings/')
def escalatorRankings():
    filename = 'escalatorRankings.html'
    return static_file(filename, root=WEBPAGE_DIR)

@bottle.route('/elevators/directory')
@bottle.route('/elevators/directory/')
@bottle.route('/elevators')
@bottle.route('/elevators/')
def allElevators():
    filename = 'elevators.html'
    return static_file(filename, root=WEBPAGE_DIR)

########################################
@bottle.route('/elevators/<unitId>')
@bottle.route('/elevators/<unitId>/')
def genElevatorStatus(unitId):
    filename = 'elevator_%s.html'%unitId
    return static_file(filename, root=WEBPAGE_DIR)

###############################################
@bottle.route('/stations')
@bottle.route('/stations/')
# Listing of all stations
def stationListing():
    filename = 'stations.html'
    return static_file(filename, root=WEBPAGE_DIR)

########################################
@bottle.route('/glossary')
@bottle.route('/glossary/')
def glossary():
    filename = 'glossary.html'
    return static_file(filename, root=WEBPAGE_DIR)

#################################################
# Run the bottle app in a greenlet 
class Server(RestartingGreenlet):

    def __init__(self):
        RestartingGreenlet.__init__(self)

    def _run(self):
        try:
            # Run the server.
            ip   = os.environ['OPENSHIFT_INTERNAL_IP']
            port = 8080
            bottleApp = bottle.default_app()
            # This call blocks
            bottle.run(host=ip, port=port, server='gevent')

        except Exception as e:
            logName = os.path.join(DATA_DIR, 'server.log')
            fout = open(logName, 'a')
            fout.write('Caught Exception while running bottle server! %s\n'%(str(e)))
            fout.close()