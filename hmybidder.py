import sys
from sys import argv
from utilities.hmybidder_logger import HmyBidderLog
import argparse
from utilities.globals import Globals
from blockchain.validator import ValidatorInfo

opts = {    
}

def main(bidArgs):
    print(bidArgs)
    if 'logfile' in opts:
        HmyBidderLog.setLogFileLocation(opts['logfile'])
    else:
        HmyBidderLog.setLogFileLocation(Globals._defaultLogfile)
    if 'version' in opts:
        print(f'Script version : {Globals._scriptVersion}')

    if 'wallet.address' in opts:
        Globals._walletAddress = opts['wallet.address']
        if not ValidatorInfo.validateONEAddress(Globals._walletAddress):
            HmyBidderLog.error('Wallet Address is in wrong format, please verify')
            return            

    if Globals._walletAddress == '':
        HmyBidderLog.error('Wallet Address is missing, stopping the script')
        return
        
    HmyBidderLog.info('Start the Harmony validator bidder script')

    print(ValidatorInfo.getTotalStakedToValidator(Globals._walletAddress))

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
                elif argv[0].lower() == '--blsdir':
                    opts['blsdir'] = argv[1]
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