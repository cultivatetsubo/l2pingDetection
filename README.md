# what is this  
l2pingを用いてBluetoothデバイスの検出を行います。
# environment  
raspberry pi zero WH
Distributor ID: Raspbian  
Description:    Raspbian GNU/Linux 10 (buster)  
Release:        10  
Codename:       buster  

# how to use  
pip3 install -r requirements.txt  
googlecalendarAPIを使うためにcredentials.jsonの作製と使用するgooglecalendarのIDを発行します。  

googlecalendarAPI  
googlecalendarIDを環境変数に登録します。
IDが"foo@bar.google.com"でbashで実行する場合、bashrcに
export calendarID=foo@bar.google.com  
を追記してください。
設置するデバイスの識別子を環境変数に登録します。
export deviceLocation=foobar  

Bluetooth addressと、その識別子をdevicesList.csvに記入します。 

aa:bb:cc:XX:XX:XX,hoge
dd:ee:ff:XX:XX:XX,fuga 

sudo -E python3 main.py  


# detailed  
detection by 15 minutes and if continuously fail to detect, it is decided that one having the device has left.
検出は15分毎に行い、連続で検出に失敗した場合、最初の検出の失敗の時間までの時間を記録します。
