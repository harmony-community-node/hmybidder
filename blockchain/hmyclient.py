from utilities.globals import Globals
from utilities.hmybidder_logger import HmyBidderLog
from subprocess import PIPE, Popen
import json
import simplejson
import os
import os.path

class HmyClientError(Exception):
    pass

class HmyClient:

    @classmethod
    def __executeCommand(self, args):
        process = None
        if os.path.isdir(Globals._hmyDirectory):
            process = Popen(args, cwd=Globals._hmyDirectory, stdout=PIPE)
        else:
            process = Popen(args, stdout=PIPE)
        (output, err) = process.communicate()
        #print(err)
        if err != None:
            raise HmyClientError(err)
        try:
            return simplejson.loads(output)
        except simplejson.JSONDecodeError:
            raise HmyClientError(output)

    @classmethod
    def __getParameters(self, blskey):
        baseParameters =  ["./hmy", "--node", Globals.getHmyNetworkUrl(), "staking", "edit-validator",
            "--validator-addr", Globals._walletAddress,
            "--bls-pubkeys-dir", Globals._blsdirPath,
            "--true-nonce"]
        passFile = f'{Globals._blsdirPath}/{blskey}.pass'
        if os.path.exists(passFile):
            baseParameters = baseParameters + ["--passphrase-file", passFile]
        else:
            baseParameters = baseParameters + ["--passphrase-file", '']
        #print(baseParameters)
        return baseParameters


    @classmethod
    def getShardForBlsKey(self, key):
        shard = -1
        try:
            nodeUrl = Globals.getHmyNetworkUrl()
            response = HmyClient.__executeCommand(['./hmy', '--node', nodeUrl, 'utility', 'shard-for-bls', key])
            shard = response['shard-id']
            return shard
        except Exception as ex:
            HmyBidderLog.error(f'HmyClient getShardForBlsKey {ex}')
            return shard
    
    @classmethod
    def checkIfAccountofWalletAddressExists(self, walletAddress):
        exists = False
        try:
            nodeUrl = Globals.getHmyNetworkUrl()
            response = HmyClient.__executeCommand(['./hmy', '--node', nodeUrl, 'keys', 'list'])
            print(response)
            if walletAddress in json.dumps(response):
                exists = True
            return exists
        except Exception as ex:
            if walletAddress in str(ex):
                return True
            else:
                HmyBidderLog.error(f'HmyClient checkIfAccountofWalletAddressExists {ex}')
                return exists

    @classmethod
    def addBlsKey(self, bls_key):
        success = False
        try:
            response = HmyClient.__executeCommand(self.__getParameters(bls_key) + ["--add-bls-key", bls_key])
            #print(response)
            if 'result' in response:
                if 'transactionHash' in response['result']:            
                    success = True
            return success
        except Exception as ex:
            HmyBidderLog.error(f'HmyClient addBlskey {ex}')
            return success
    
    @classmethod
    def removeBlsKey(self, bls_key):
        success = False
        try:
            response = HmyClient.__executeCommand(self.__getParameters(bls_key) + ["--remove-bls-key", bls_key])
            #print(response)
            if 'result' in response:
                if 'transactionHash' in response['result']:
                    success = True
            return success
        except Exception as ex:
            HmyBidderLog.error(f'HmyClient removeBlskey {ex}')
            return success        