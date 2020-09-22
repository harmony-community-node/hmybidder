# Harmony Protocol Staking Validator auto bidder script


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
BlockRange=50:30
RefreshInSeconds=60
```

### Install python dependencies

> pip3 install pyhmy

### Running the script

> python3 hmybidder.py -c hmybidder.config
