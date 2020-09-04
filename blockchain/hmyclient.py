from utilities.globals import Globals
from utilities.hmybidder_logger import HmyBidderLog
from subprocess import PIPE, Popen
import simplejson
import os

class HmyClientError(Exception):
    pass

class HmyClient:

    _baseParameter =  ["hmy", "--node", Globals.getHmyNetworkUrl(), "staking", "edit-validator",
            "--validator-addr", Globals._walletAddress,
            "--passphrase-file", Globals._walletPassFile,
            "--bls-pubkeys-dir", Globals._blsdirPath,
            "--true-nonce"]

    @classmethod
    def executeCommand(self, args):
        process = None
        if os.path.isdir(Globals._hmyDirectory):
            process = Popen(args, cwd=Globals._hmyDirectory, stdout=PIPE)
        else:
            process = Popen(args, stdout=PIPE)
        (output, err) = process.communicate()
        try:
            return simplejson.loads(output)
        except simplejson.JSONDecodeError:
            raise HmyClientError(output)

    @classmethod
    def getShardForBlsKey(self, key):
        shard = -1
        nodeUrl = Globals.getHmyNetworkUrl()
        response = HmyClient.executeCommand(['./hmy', '--node', nodeUrl, 'utility', 'shard-for-bls', key])
        shard = response['shard-id']
        return shard
    
    @classmethod
    def addBlsKey(self, bls_key):
        success = False
        response = HmyClient.executeCommand(self._baseParameter + ["--add-bls-key", bls_key])
        if 'transaction-hash' in response:
            success = True
        return success
    
    @classmethod
    def removeBlsKey(self, bls_key):
        success = False
        response = HmyClient.executeCommand(self._baseParameter + ["--remove-bls-key", bls_key])
        if 'transaction-hash' in response:
            success = True
        return success