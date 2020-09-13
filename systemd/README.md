
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
RestartSec=1
User=satish
WorkingDirectory=[Your Working Directory]
EnvironmentFile=[Your .hmybidderconfig File Location]
ExecStart=/usr/bin/python3 [Directory of hmybidder.py]/hmybidder.py --network $Network --logfile $LogFilePath --blsdir $BLSDir --hmydir $HMYDir  --wallet.address $ONEADDRESS --leverage $Leverage --shards.keys $ShardKeys --passphrase-file $PassphraseFile --slots $Slots --epoch-block $EpochBlock
SyslogIdentifier=hmybidder
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
```

Create the .hmybidderconfig file and save it into the directory path which is given in the above service file, this config file will provide all the parameters required to run the script

```
sudo nano [Directory]/.hmybidderconfig
```

Provide the values to the parameters, following are example values, please provide your actual values.

```
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

Create a timer file for scheduling the hmybidder service to run every 60 seconds

```
sudo nano /etc/systemd/system/hmybidder.timer
```
Add following config to hmybidder.timer file

```
[Unit]
Description=Schedule a hmybidder to run every 1 minute
RefuseManualStart=no        # Allow manual starts
RefuseManualStop=no         # Allow manual stops

[Timer]
# Execute job if it missed a run due to machine being off
Persistent=true
# Run 120 seconds after boot for the first time
OnBootSec=120
# Run every 1 minute thereafter
OnUnitActiveSec=60
# File describing job to execute
Unit=hmybidder.service

[Install]
WantedBy=timers.target
```

Now all required files are create, need to enable and start running the service
```
sudo chmod 644 /etc/systemd/system/hmybidder.service
sudo systemctl daemon-reload
sudo systemctl enable hmybidder.service
sudo systemctl start hmybidder.service 
sudo systemctl enable hmybidder.timer
sudo systemctl start hmybidder.timer
```

To stop or restart the services
```
sudo systemctl stop hmybidder.timer
sudo systemctl stop hmybidder.service 
```
```
sudo systemctl restart hmybidder.timer
sudo systemctl restart hmybidder.service 
```


To delete the services

```
sudo systemctl stop hmybidder.timer
sudo systemctl disable hmybidder.timer
sudo systemctl stop hmybidder.service
sudo systemctl disable hmybidder.service
sudo systemctl daemon-reload
sudo systemctl reset-failed
```
