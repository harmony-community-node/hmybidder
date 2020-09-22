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
4) Provide the values to the parameters on the config file.
```
Network           mainnet,testnet
LogFilePath       location of the log file
HMYDir            location of the hmy binary
BLSDir            BLS keys directory (put all your keys along with the .pass files on this folder)
ONEADDRESS        your validator address (make sure the wallet exists using ./hmy keys list)
Leverage          leverage over the median stake using percentage (%). Ex: if -10 you will bid -10% below the median stake
ShardKeys         maximum number of keys set on each shard. Ex: 0:1:1:2:2:3:3:4 will set shard0[1 key],shard1[2 keys], shard2[3 keys], shard3[4 keys]
PassphraseFile    wallet passphrase. If your wallet has not passphrase, create the file and leave it empty
Slots             number of slots available on the network
BlockRange        block range where the bidding tool will try to evaluate keys
RefreshInSeconds  time in seconds till the script tries to evaluate keys again. Make sure the BlockRange matches the time you set
```

Example for mainnet:
```
[DEFAULT]
Network=mainnet
LogFilePath=/home/harmony/hmybidder/hmybidder.log
HMYDir=/home/harmony 
BLSDir=/home/harmony/hmybidder/blsdir
ONEADDRESS=one19ugus2az5a9m8tcgeq2pazcdht5kn3pe86434u
Leverage=0
ShardKeys=0:0:1:3:2:0:3:0
PassphraseFile=/home/harmony/hmybidder/wallet.pass
Slots=640
BlockRange=1440:10
RefreshInSeconds=3600
```

Example for testnet:
```
[DEFAULT]
Network=testnet
LogFilePath=/home/harmony/hmybidder/hmybidder.log
HMYDir=/home/harmony 
BLSDir=/home/harmony/hmybidder/blsdir
ONEADDRESS=one19ugus2az5a9m8tcgeq2pazcdht5kn3pe86434u
Leverage=0
ShardKeys=0:0:1:3:2:0:3:0
PassphraseFile=/home/harmony/hmybidder/wallet.pass
Slots=88
BlockRange=30:10
RefreshInSeconds=60
```

### Running the script

To test the script you can run it using:

```python3 hmybidder.py -c hmybidder.config```

For production we recommend you setup it using Systemd, [check here](https://github.com/harmony-community-node/hmybidder/tree/master/systemd).
