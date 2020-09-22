# Harmony Protocol Staking Validator auto bidder script

1) Install required packages:

```
sudo apt install git python3 python3-pip
sudo pip3 install pyhmy
```
2) Clone repository:

```
git clone https://github.com/harmony-community-node/hmybidder.git
```
3) Create the hmybidder.config file and save it into the directory path which is given in the above service file, this config file will provide all the parameters required to run the script:

```
sudo nano [Directory]/hmybidder.config
```
4) Provide the values to the parameters, following are example values, please provide your actual values:

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
RefreshInSeconds = 60
```
### Running the script

To test the script you can run it using:

```python3 hmybidder.py -c hmybidder.config```

For instructions on how to setup it using Systemd, [check here](https://github.com/harmony-community-node/hmybidder/tree/master/systemd).
