import sys
from sys import argv
import subprocess
import json
from os import listdir
from os.path import isfile, join
from utilities.hmybidder_logger import HmyBidderLog
import argparse
from utilities.globals import Globals
from blockchain.validator import ValidatorInfo
from models import NetworkInfo

opts = {    
}

def main(bidArgs):
    #print(bidArgs)
    #if 'version' in opts:
        #print(f'Script version : {Globals._scriptVersion}')

    if 'wallet.address' in opts:
        Globals._walletAddress = opts['wallet.address']
        if not ValidatorInfo.validateONEAddress(Globals._walletAddress):
            HmyBidderLog.error('Wallet Address is in wrong format, please verify')
            return            

    if Globals._walletAddress == '':
        HmyBidderLog.error('Wallet Address is missing, stopping the script')
        return

    HmyBidderLog.info('Start the Harmony validator bidder script')

    #network_info = ValidatorInfo.getNetworkLatestInfo()
    #if network_info != None:
    #    print(network_info.to_dict())

def validateShardKey(shardKeys):
    valid = False
    parts = shardKeys.split(" ")
    if len(parts) == 8:
        keysOnShardZero = []
        keysOnShardOne = []
        keysOnShardTwo = []
        keysOnShardThree = []
        blskeyFiles = []
        hmyDir = Globals._hmyDirectory
        nodeUrl = Globals.getHmyNetworkUrl()
        try:
            for f in listdir(Globals._blsdirPath):
                if isfile(join(Globals._blsdirPath, f)):
                    if f.endswith(".key"):
                        blskeyFiles.append(f)
                        proc = subprocess.Popen(f'{hmyDir}/./hmy --node="{nodeUrl}" utility shard-for-bls {f.replace(".key", "")}', stdout=subprocess.PIPE, shell=True)
                        (out, err) = proc.communicate()
                        if err == None:
                            response = json.loads(out)
                            if response['shard-id'] == 0:
                                keysOnShardZero.append(f.replace(".key", ""))
                            elif response['shard-id'] == 1:
                                keysOnShardOne.append(f.replace(".key", ""))
                            elif response['shard-id'] == 2:
                                keysOnShardTwo.append(f.replace(".key", ""))
                            elif response['shard-id'] == 3:
                                keysOnShardThree.append(f.replace(".key", ""))
                        else:
                            HmyBidderLog.error(err)
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
                    if not validateShardKey(argv[1]):
                        HmyBidderLog.error("BLS Keys set on --shards.keys don't match the minimum number of keys available on --blsdir")
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
        except Exception as ex:
            print(f'Command line input error {ex}')
        finally:
            argv = argv[1:]
    return opts

if __name__ == '__main__':
    bidArgs = getopts(argv)
    main(bidArgs)