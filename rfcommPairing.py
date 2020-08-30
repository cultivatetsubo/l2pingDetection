import csv
import sys
import subprocess
import datetime
import time
import calenderAPI
import os



def doRfcommPairing(BDAddr):
  rfcommP = subprocess.Popen(['rfcomm connect 0',str(BDAddr)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  time.sleep(1)
  rfcommP.kill()
  isL2pingRes=doL2ping(BDAddr)
  return isL2pingRes

def doL2ping(BDAddr):
  l2pingRes = subprocess.run(['l2ping',str(BDAddr),"-c","3"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  try:
    failureRate = str(l2pingRes.stdout).split()[-2]
    failureRate = int(failureRate.split("%")[0])
  except ValueError:
    failureRate = 100
  if(failureRate < 100):
    return True
  else:
    return False

def makeListOfDevices(Reader):
  ListOfDevices=[]
  for row in Reader:
    ListOfDevices.append(row)
  return ListOfDevices

def rfcommPairingMain():
  if(True):
    with open('./devicesList.csv', 'r') as devices_f:
      devicesListReader=csv.reader(devices_f)
      ListDevices=makeListOfDevices(devicesListReader)
      for device in ListDevices:
        BDAddr=device[0]
        isRes=doL2ping(BDAddr)
        if (isRes==False):
          res=doRfcommPairing(BDAddr)
          
        else:
          continue

