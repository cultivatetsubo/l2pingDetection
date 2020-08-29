import csv
import sys
import subprocess
import datetime
import time
import calenderAPI
import os


def makeCSVLogSucceededPairing():
  with open('./devicesList.csv') as devices_f:
    devicesListReader = csv.reader(devices_f)
    with open('./pairedDevicesLog.csv', 'a') as pairing_f:
      pairedLogWriter = csv.writer(pairing_f)
      for deviceRow in devicesListReader:
        pairedDeviceLog=deviceRow.append(False)
        print(pairedDeviceLog)
        pairedLogWriter.writerow(pairedDeviceLog)
  return

def doRfcommPairing(BDAddr):
  rfcommRes = subprocess.run(['rfcomm connect 0',str(BDAddr)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return rfcommRes

def doL2ping(BDAddr):
  l2pingRes = subprocess.run(['l2ping',str(BDAddr),"-c","3"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  try:
    failureRate = str(l2pingRes.stdout).split()[-2]
    failureRate = int(failureRate.split("%")[0])
  except ValueError:
    failureRate = 100
  if(failureRate>50):
    return False
  else:
    return True

def makeListOfDevices(Reader):
  ListOfDevices=[]
  for row in Reader:
    ListOfDevices.append(row)
  return ListOfDevices

def rfcommPairingMain():
  makeCSVLogSucceededPairing()
  with open('./pairedDevicesLog.csv') as devicesList:
    # print(devicesList)
    devicesListReader = csv.reader(devicesList)
    if(True):
      ListDevices=makeListOfDevices(devicesListReader)
      with open('./pairedDevicesLog.csv', 'w') as pairing_f:
        pairedLogWriter = csv.writer(pairing_f)
        for device in ListDevices:
          hasPaired=device[2]
          BDAddr=device[0]
          if(hasPaired==False):
            res=doRfcommPairing(BDAddr)
            time.sleep(3)
            isL2pingRes=doL2ping(BDAddr)

        pairedLogWriter.writerow(device)

