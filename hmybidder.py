import sys
import time
import random
import argparse
import threading
import configparser
from sys import argv
from os import listdir
from os.path import isfile, join, exists
from utilities.hmybidder_logger import HmyBidderLog
from utilities.globals import Globals
from models import NetworkInfo, ValidatorInfo
from blockchain.hmyclient import HmyClient
from bidder.bidderclient import HMYBidder
from blockchain.validator import Validator

version = 'v1.0.0'

def main():

    network_info = Validator.getNetworkLatestInfo()
    if network_info != None:
        HmyBidderLog.info(network_info.to_dict())
        curretEpoch = Validator.getCurrentEpoch() # Dont run the bidding process if it is been run for current epoch
        HmyBidderLog.info(f'Current Epoch {curretEpoch} Global Current Epoch {Globals._currentEpoch} Block Range {Globals._upperBlock} : {Globals._lowerBlock}')
        if network_info.blocks_to_next_epoch in range(Globals._lowerBlock, Globals._upperBlock) and curretEpoch != Globals._currentEpoch: # checking extra 5 block to make sure not missing the bidding process
        #if True:
            HmyBidderLog.info('Started Evaluating the BLS Keys')
            HMYBidder.startBiddingProcess(network_info)
            Globals._currentEpoch = Validator.getCurrentEpoch() # reset current epoch after running the bidding process
    if Globals._refreshInSeconds == None or Globals._refreshInSeconds <= 0:
        Globals._refreshInSeconds = 60
    threading.Timer(Globals._refreshInSeconds, main).start() #Keep running the process every N seconds

def validateShardKey(shardKeys):
    valid = False
    parts = shardKeys.split(":")
    if len(parts) == 8:
        try:
            Globals._shardsKeys = {}
            for shardId in range(0, Globals._numberOfShards):
                shardKey = f'shard{shardId}'
                Globals._shardsKeys[shardKey] = []
            for f in listdir(Globals._blsdirPath):
                if isfile(join(Globals._blsdirPath, f)):
                    if f.endswith(".key"):
                        blsKey = f.replace(".key", "")
                        shard = int(HmyClient.getShardForBlsKey(blsKey))
                        if shard != -1:
                            if shard == 0:
                                if not blsKey in Globals._shardsKeys['shard0']:
                                    Globals._shardsKeys['shard0'].append(blsKey)
                            elif shard == 1:
                                if not blsKey in Globals._shardsKeys['shard1']:
                                    Globals._shardsKeys['shard1'].append(blsKey)
                            elif shard == 2:
                                if not blsKey in Globals._shardsKeys['shard2']:
                                    Globals._shardsKeys['shard2'].append(blsKey)
                            elif shard == 3:
                                if not blsKey in Globals._shardsKeys['shard3']:
                                    Globals._shardsKeys['shard3'].append(blsKey)
                        else:
                            HmyBidderLog.error(f" Error while getting the Shard for BLS Key {blsKey}")
            #print(f'{len(Globals._shardsKeys["shard0"])} - {len(Globals._shardsKeys["shard1"])} - {len(Globals._shardsKeys["shard2"])} - {len(Globals._shardsKeys["shard3"])}')
            if int(parts[1]) <= len(Globals._shardsKeys['shard0']) and int(parts[3]) <= len(Globals._shardsKeys['shard1']) and int(parts[5]) <= len(Globals._shardsKeys['shard2']) and int(parts[7]) <= len(Globals._shardsKeys['shard3']):
                valid = True
            else:
                valid = False
        except Exception as ex:
            HmyBidderLog.error(f'Hmybidder validateShardKey {ex}')
            valid = False
        finally:
            return valid        
    

def getopts(argv):
    showHelp = False
    showVersion = False
    while argv:  
        try:
            if argv[0][0] == '-':
                if argv[0].lower() == '-c' or argv[0].lower() == '--config':
                    stopScript = False
                    Globals._configFile = argv[1]
                    if not exists(Globals._configFile):
                        stopScript = True
                        HmyBidderLog.error('Missing config file')

                    config = configparser.ConfigParser()
                    config.read(Globals._configFile)
                    if config.get('DEFAULT','Network') != None:
                        Globals._network_type = config.get('DEFAULT','Network')
                    if config.get('DEFAULT', 'LogFilePath') != None:
                        Globals._logFile = config.get('DEFAULT', 'LogFilePath')
                        HmyBidderLog.setLogFileLocation(Globals._logFile)
                    if config.get('DEFAULT', 'HMYDir') != None:
                        Globals._hmyDirectory = config.get('DEFAULT', 'HMYDir')
                    if config.get('DEFAULT', 'BLSDir') != None:
                        Globals._blsdirPath = config.get('DEFAULT', 'BLSDir')
                    if config.get('DEFAULT', 'ONEADDRESS') != None:
                        Globals._walletAddress = config.get('DEFAULT', 'ONEADDRESS')
                        if not Validator.validateONEAddress(Globals._walletAddress):
                            HmyBidderLog.error('Wallet Address is in wrong format, please verify')
                            stopScript = True
                        if not HmyClient.checkIfAccountofWalletAddressExists(Globals._walletAddress):
                            HmyBidderLog.error('Wallet Address is not in wallet accounts')
                            stopScript = True
                    if config.get('DEFAULT', 'Leverage') != None:
                        Globals._leverage = int(config.get('DEFAULT', 'Leverage'))
                    if config.get('DEFAULT', 'ShardKeys') != None:
                        Globals._shardsKeys = config.get('DEFAULT', 'ShardKeys')
                        if not validateShardKey(Globals._shardsKeys):
                            HmyBidderLog.error("BLS Keys set on --shards.keys don't match the minimum number of keys available on --blsdir")
                            stopScript = True
                    if config.get('DEFAULT', 'PassphraseFile') != None:
                        Globals._passphraseFile = config.get('DEFAULT', 'PassphraseFile')
                    if config.get('DEFAULT', 'Slots') != None:
                        Globals._totalSlots = int(config.get('DEFAULT', 'Slots'))
                    if config.get('DEFAULT', 'BlockRange') != None:
                        blockRange = config.get('DEFAULT', 'BlockRange')
                        parts = blockRange.split(":")
                        if len(parts) == 2:
                            Globals._upperBlock = int(parts[0])
                            if Globals._upperBlock <= 0:
                                Globals._upperBlock = 50
                            Globals._lowerBlock = int(parts[1])
                            if Globals._lowerBlock <= 0:
                                Globals._lowerBlock = 30
                    if config.get('DEFAULT', 'RefreshInSeconds') != None:
                        Globals._refreshInSeconds = int(config.get('DEFAULT', 'RefreshInSeconds'))

                    if stopScript:
                        HmyClient.stopSystemdService("hmybidder.service")
                        return False
                    return True
                elif argv[0].lower() == '-v' or argv[0].lower() == '--version':
                    showVersion = True                    
                elif argv[0].lower() == '-h' or argv[0].lower() == '--help':
                    showHelp = True
        except Exception as ex:
            print(f'Command line input error {ex}')
        finally:
            argv = argv[1:]
    
    if showHelp:
        with open('help.txt', 'r') as file:
            print(file.read())
    elif showVersion:
        print(f'Version {version}')
    elif Globals._walletAddress == '':
        HmyBidderLog.error('Wallet Address is missing, stopping the script')
        return False
    if Globals._epochBlock == None:
        Globals._epochBlock = random.randint(100, 200)
    return True

if __name__ == '__main__':
    if getopts(argv):
        main()