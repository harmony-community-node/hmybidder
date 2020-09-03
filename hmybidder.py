import sys
from sys import argv
from os import listdir
from os.path import isfile, join
from utilities.hmybidder_logger import HmyBidderLog
import argparse
from utilities.globals import Globals
from blockchain.validator import Validator
from models import NetworkInfo, ValidatorInfo
from bidder.biddingcalculator import BiddingCalculator

opts = {    
}

def main(bidArgs):
    #print(bidArgs)
    #if 'version' in opts:
        #print(f'Script version : {Globals._scriptVersion}')

    if 'wallet.address' in opts:
        Globals._walletAddress = opts['wallet.address']
        if not Validator.validateONEAddress(Globals._walletAddress):
            HmyBidderLog.error('Wallet Address is in wrong format, please verify')
            return            

    if Globals._walletAddress == '':
        HmyBidderLog.error('Wallet Address is missing, stopping the script')
        return

    HmyBidderLog.info('Start the Harmony validator bidder script')

    numberOfBlsKeys = BiddingCalculator.calculateBlsKeysForNextEpoch()
    print(f'numberOfBlsKeys - {numberOfBlsKeys}')
    #network_info = ValidatorInfo.getNetworkLatestInfo()
    #if network_info != None:
    #    print(network_info.to_dict())
    validator_info = Validator.getValidatorInfo(Globals._walletAddress)
    print(len(validator_info.blsKeys))

def validateShardKey(shardKeys):
    valid = False
    parts = shardKeys.split(" ")
    if len(parts) == 8:
        keysOnShardZero = []
        keysOnShardOne = []
        keysOnShardTwo = []
        keysOnShardThree = []
        try:
            for f in listdir(Globals._blsdirPath):
                if isfile(join(Globals._blsdirPath, f)):
                    if f.endswith(".key"):
                        blsKey = f.replace(".key", "")
                        shard = int(Globals.getShardForBlsKey(blsKey))
                        if shard != -1:
                            if shard == 0:
                                keysOnShardZero.append(blsKey)
                            elif shard == 1:
                                keysOnShardOne.append(blsKey)
                            elif shard == 2:
                                keysOnShardTwo.append(blsKey)
                            elif shard == 3:
                                keysOnShardThree.append(blsKey)
                        else:
                            HmyBidderLog.error(f" Error while getting the Shard for BLS Key {blsKey}")
            if int(parts[1]) <= len(keysOnShardZero) and int(parts[3]) <= len(keysOnShardOne) and int(parts[5]) <= len(keysOnShardTwo) and int(parts[7]) < len(keysOnShardThree):
                valid = True
            else:
                valid = False
        except Exception as ex:
            HmyBidderLog.error(ex)
            valid = False
        finally:
            return valid        
    

def getopts(argv):
    while argv:  
        try:
            if argv[0][0] == '-':  
                if argv[0].lower() == '-n' or argv[0].lower() == '--network':
                    opts['network'] = argv[1]
                elif argv[0].lower() == '-v' or argv[0].lower() == '--version':
                    opts['version'] = "True"
                elif argv[0].lower() == '-h' or argv[0].lower() == '--help':
                    opts['help'] = "True"
                elif argv[0].lower() == '--logfile':
                    opts['logfile'] = argv[1]
                    HmyBidderLog.setLogFileLocation(opts['logfile'])
                elif argv[0].lower() == '--blsdir':
                    opts['blsdir'] = argv[1]
                    Globals._blsdirPath = argv[1]
                elif argv[0].lower() == '--shards.keys':
                    opts['shards.keys'] = argv[1]
                    #if not validateShardKey(argv[1]):
                    #    HmyBidderLog.error("BLS Keys set on --shards.keys don't match the minimum number of keys available on --blsdir")
                elif argv[0].lower() == '--wallet.address':
                    opts['wallet.address'] = argv[1]
                elif argv[0].lower() == '--wallet.passfile':
                    opts['wallet.passfile'] = argv[1]
                    Globals._walletPassFile = argv[1]
                elif argv[0].lower() == '--epochblock':
                    opts['epochblock'] = argv[1]
                    Globals._epochblock = int(argv[1])
                elif argv[0].lower() == '--leverage':
                    opts['leverage'] = int(argv[1])
                    if int(argv[1]) != 0:
                        Globals._leverage = int(argv[1])
                    else:
                        Globals._leverage = 0
        except Exception as ex:
            print(f'Command line input error {ex}')
        finally:
            argv = argv[1:]
    return opts

if __name__ == '__main__':
    bidArgs = getopts(argv)
    main(bidArgs)