import sys
from sys import argv
from os import listdir
from os.path import isfile, join
import threading
from utilities.hmybidder_logger import HmyBidderLog
import argparse
from utilities.globals import Globals
from models import NetworkInfo, ValidatorInfo
from blockchain.hmyclient import HmyClient
from bidder.bidderclient import HMYBidder
from blockchain.validator import Validator

version = 'v1.0.0'

def main():

    HmyBidderLog.info('Start the Harmony validator bidder script')
    network_info = Validator.getNetworkLatestInfo()
    if network_info != None:
        print(network_info.to_dict())
        curretEpoch = Validator.getCurrentEpoch() # Dont run the bidding process if it is been run for current epoch
        if network_info.blocks_to_next_epoch in range(Globals._epochBlock - 5, Globals._epochBlock) and curretEpoch != Globals._currentEpoch: # checking extra 5 block to make sure not missing the bidding process
            HMYBidder.startBiddingProcess(network_info)
            Globals._currentEpoch = Validator.getCurrentEpoch() # reset current epoch after running the bidding process
    #threading.Timer(60.0, main).start() #Keep running the process every 60 seconds
        

def validateShardKey(shardKeys):
    valid = False
    parts = shardKeys.split(" ")
    if len(parts) == 8:
        try:
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
            HmyBidderLog.error(f'Hmybidder getMedianRawStakeSnapshot {ex}')
            valid = False
        finally:
            return valid        
    

def getopts(argv):
    while argv:  
        try:
            if argv[0][0] == '-':  
                if argv[0].lower() == '-n' or argv[0].lower() == '--network':
                    Globals._network_type = argv[1]
                elif argv[0].lower() == '-v' or argv[0].lower() == '--version':
                    print(f'Version {version}')
                elif argv[0].lower() == '-h' or argv[0].lower() == '--help':
                    # TODO : Prepare Help
                    print(f'Help')
                elif argv[0].lower() == '--logfile':
                    Globals._logFile = argv[1]
                    HmyBidderLog.setLogFileLocation(Globals._logFile)
                elif argv[0].lower() == '--blsdir':
                    Globals._blsdirPath = argv[1]
                elif argv[0].lower() == '--hmydir':
                    Globals._hmyDirectory = argv[1]
                elif argv[0].lower() == '--shards.keys':
                    if not validateShardKey(argv[1]):
                        HmyBidderLog.error("BLS Keys set on --shards.keys don't match the minimum number of keys available on --blsdir")
                        return False
                elif argv[0].lower() == '--wallet.address':
                    Globals._walletAddress = argv[1]
                    if not Validator.validateONEAddress(Globals._walletAddress):
                        HmyBidderLog.error('Wallet Address is in wrong format, please verify')
                        return False
                elif argv[0].lower() == '--wallet.passfile':
                    Globals._walletPassFile = argv[1]
                elif argv[0].lower() == '--epochblock':
                    Globals._epochblock = int(argv[1])
                elif argv[0].lower() == '--leverage':
                    if int(argv[1]) != 0:
                        Globals._leverage = int(argv[1])
                    else:
                        Globals._leverage = 0
        except Exception as ex:
            print(f'Command line input error {ex}')
        finally:
            argv = argv[1:]
        
    if Globals._walletAddress == '':
        HmyBidderLog.error('Wallet Address is missing, stopping the script')
        return False
    return True

if __name__ == '__main__':
    if getopts(argv):
        main()