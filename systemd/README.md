
### Create a Service to run hmybidder python script to run as Systemd Service


Open the terminal and create a service
```
sudo nano /etc/systemd/system/hmybidder.service
```
Add following configuaration in the service file, please provide your actual 
```
[Unit]
Description=Harmony Validator Bidder Script
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=60
User=root
WorkingDirectory=[Your Working Directory]
ExecStart=/usr/bin/python3 [Directory of hmybidder.py]/hmybidder.py -c [Config File Location]
SyslogIdentifier=hmybidder
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
```

Create the hmybidder.config file and save it into the directory path which is given in the above service file, this config file will provide all the parameters required to run the script

```
sudo nano [Directory]/hmybidder.config
```

Provide the values to the parameters, following are example values, please provide your actual values.

```
[DEFAULT]
Network=mainnet
LogFilePath=[Directory]/hmybidder.log
HMYDir= [Your hmydir Directory] 
BLSDir=[Your BLS Keys Direcotry]
ONEADDRESS=one1pcdsadfkl23423zxxzc23423nsdft38hku2m
Leverage=-5
ShardKeys=0:4:1:3:2:5:3:2
PassphraseFile=[Your Wallet pass Directory]/wallet.pass
Slots=640
EpochBlock=178
```


Now all required files are create, need to enable and start running the service
```
sudo chmod 644 /etc/systemd/system/hmybidder.service
sudo systemctl daemon-reload
sudo systemctl enable hmybidder.service
sudo systemctl start hmybidder.service 
```

To stop or restart the services
```
sudo systemctl stop hmybidder.service 
```
```
sudo systemctl restart hmybidder.service 
```


To delete the services

```
sudo systemctl stop hmybidder.service
sudo systemctl disable hmybidder.service
sudo systemctl daemon-reload
sudo systemctl reset-failed
```
