###########################################################################################
#This scripts starts all the Managed Servers in a Weblogic domain
#Author - rajeshr
#Questions - mwss.bi.team@qualcomm.com
#Date - 10/17/2012
###########################################################################################

def connectwls(tgtinst,wlsurl):
#    wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
#    wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')
#    str_nm=raw_input('Do you want NodeManager to be restarted - Type yes or no: ')
#    tgt_inst=raw_input('Enter the name of the environment that needs to be bounced example - EDWTST, ERPDEV2, QMTTS2: ')
    print tgtinst
    print wlsurl
#    WLS_URL=wlshostname + ":" + wlsport
    try:
       conncmd1="connect(userConfigFile='/prj/obiee-dev/" + tgtinst + "/credentials/" + tgtinst + "_configfile.secure',userKeyFile='/prj/obiee-dev/" + tgtinst + "/credentials/" + tgtinst + "_keyfile.secure',url='" + wlsurl + "')"
#      print conncmd1
       exec conncmd1
    except:
       print "Couldn't connect to the WLS admin server"

def server_state(svrName):
    sstate = 'UNKNOWN'
    try :
        myTree = currentTree()
        domainRuntime()
        #cd( '/ServerLifeCycleRuntimes/' + svrName.getName())
        #sstate = cmo.getState()
#        print svrName 
        sstate = cmo.lookupServerLifeCycleRuntime(svrName).getState()
#        print sstate
        myTree()
    except:
        print 'Exception while trying to get ServerRuntimeMBean'
        dumpStack()
        myTree()
    return sstate

def startManagedServers():
#    connectwls()
    srvs = cmo.getServers()
    for server in srvs:
        svrStatus = server_state(server.getName())
        ntries = 0
        if server.getName() != 'AdminServer':
           svrStatus = server_state(server.getName())
           print server.getName() + " is " + svrStatus + " state"
           if svrStatus == "SHUTDOWN":
              print "Starting server " + server.getName() + " : " +  str(datetime.now())
              start(server.getName(),'Server')
              PyTime.sleep(10)
              while (ntries < 3):
                   ntries = ntries+1
                   PyTime.sleep(10)
                   svrStatus = server_state(server.getName())
                   if svrStatus == "RUNNING":
                      print "Managed Server " + server.getName() + " is in the RUNNING state now" + " : " +  str(datetime.now())
                      break
           svrStatus = server_state(server.getName())
        elif svrStatus == "RUNNING":
           print "Managed Server " + server.getName() + " is already running" 
       
        elif (ntries == 3 and svrStatus != 'RUNNING'):
           print "Managed Server " + svrName + " couldn't be started" + " : " +  str(datetime.now())

        else:
           print "Script couldn't start Managed Server"
    disconnect()
    exit()

###############################################
#Main
###############################################

import sys
import os
import time as PyTime
from datetime import datetime
import socket
wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')
#str_nm=raw_input('Do you want NodeManager to be restarted - Type yes or no: ')
tgt_inst=raw_input('Enter the name of the environment that needs to be bounced in UPPER CASE example - EDWTST, ERPDEV2, QMTTS2: ')
WLS_URL=wlshostname + ":" + wlsport

connectwls(tgt_inst,WLS_URL)
startManagedServers()
