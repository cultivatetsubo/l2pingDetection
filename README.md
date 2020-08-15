# what is this  
detection  
push in google calendar  
you have to make pairing at once by rfcomm.
# environment  
raspberry pi zero WH
Distributor ID: Raspbian
Description:    Raspbian GNU/Linux 10 (buster)
Release:        10
Codename:       buster

# how to use  
pip3 install -r requirements.txt
you have to create another file, credentials.json.  

googlecalendarAPI  
create credentials.json in this directry following the way.  
if calendarID  is "foo@bar.google.com", in bashrc,
export calendarID=foo@bar.google.com  

and if you have decided the location installing the detection device,in bash
export deviceLocation=foobar  

you have to describe the Bluetooth Addresses of devices to detect and the name of the person having the device in devicesList.csv.

aa:bb:cc:XX:XX:XX,foo

sudo -E python3 main.py

# detailed  
detection by 15 minutes and if continuously fail to detect, it is decided that one having the device has left.
