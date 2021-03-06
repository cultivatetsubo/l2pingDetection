import csv
import sys
import subprocess
import datetime
import time
import calenderAPI
# import rfcommPairing
import os



def addObjOfDetectedInfo(BDAddr,deviceName,detectedTime,dict):
  dict[BDAddr]={"BDAddr":BDAddr,"Name":deviceName,"beginTime":detectedTime,"endTime":None,"uploadFlag":False}
  return dict

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

def doRfcommPairing(BDAddr):
  rfcommP = subprocess.Popen(['rfcomm','connect','0',str(BDAddr)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  time.sleep(1)
  rfcommP.kill()
  isL2pingRes=doL2ping(BDAddr)
  return isL2pingRes

def main():
  dictOfActiveDevices={}
  location=os.environ.get('deviceLocation')
  for env in os.environ:
    print(env)
  print("location=",location)
  #{"keyBDAddr":{"BDAddr":None,"Name":None,"beginTime":None,"endTime":None,"uploadFlag":False}}
  while True:
    with open('./devicesList.csv') as devicesList:
    # print(devicesList)
        devicesListReader = csv.reader(devicesList)
        dt_now = datetime.datetime.now()
        strDate=dt_now.strftime('%Y-%m-%d')
        strTime=dt_now.strftime('%H:%M')
        if strTime=="23:59":
          for BDAddr in dictOfActiveDevices:
            dictOfActiveDevices[BDAddr]["endTime"]=strTime
            calenderAPI.uploadfunc(strDate,location,dictOfActiveDevices[BDAddr]["Name"],dictOfActiveDevices[BDAddr]["beginTime"],dictOfActiveDevices[BDAddr]["endTime"])
          dictOfActiveDevices={}
        minutes=dt_now.minute
        if(True):
          for row in devicesListReader:
            #subprocess.call(['echo','"'+str(AddrAndName[0])+'"'])
            BDAddr=row[0]
            Name=row[1]
            shouldDoRfcomm = not(doL2ping(BDAddr))
            if(shouldDoRfcomm):
              doRfcommPairing(BDAddr)

            hasSucceededL2ping=doL2ping(BDAddr)
            if(hasSucceededL2ping):
              print(strTime,BDAddr,"l2pingSuccess")
              if BDAddr in dictOfActiveDevices.keys():
                print(BDAddr,"in activeList")
                if dictOfActiveDevices[BDAddr]["endTime"]!=None:
                  dictOfActiveDevices[BDAddr]["endTime"]=None
                  dictOfActiveDevices[BDAddr]["uploadFlag"]=False
              else:
                dictOfActiveDevices=addObjOfDetectedInfo(BDAddr,Name,strTime,dictOfActiveDevices)
                print("add",BDAddr)

            else:
              print(strTime,BDAddr,"failure")
              if (BDAddr in dictOfActiveDevices.keys())==False:
                print(BDAddr,"not active")
              else:
                if  dictOfActiveDevices[BDAddr]["uploadFlag"]==False:
                  dictOfActiveDevices[BDAddr]["uploadFlag"]=True
                  dictOfActiveDevices[BDAddr]["endTime"]=strTime
                  print("on uploadFlag",dictOfActiveDevices[BDAddr])
                else:
                  print("beforePop",dictOfActiveDevices)
                  calenderAPI.uploadfunc(strDate,location,dictOfActiveDevices[BDAddr]["Name"],dictOfActiveDevices[BDAddr]["beginTime"],dictOfActiveDevices[BDAddr]["endTime"])
                  dictOfActiveDevices.pop(BDAddr)
                  print("afterPop",dictOfActiveDevices)
          l2pingRes=None
          time.sleep(60)
        else:
          time.sleep(30)

if __name__ == "__main__":
    main()