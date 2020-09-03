import random
import subprocess
import json
from utilities.hmybidder_logger import HmyBidderLog

class Globals:
    _hmyDirectory = '~/hmydir'
    _walletAddress = ''
    _defaultLogfile = 'hmybidder.log'
    _blsdirPath = '~/blsdir'
    _scriptVersion = 'v1.0'
    _epochBlock = random.randint(100, 200)
    _walletPassFile = 'wallet.pass'
    _network_type = 'mainnet'
    _oneAmountDenominator = 1000000000000000000
    _numberOfSecondsForEpoch = 7.5
    _leverage = 0

    _network_end_points = {
        'mainnet' : 'https://api.s0.t.hmny.io',
        'testnet' : 'https://api.s0.b.hmny.io',
        'localnet' : 'http://localhost:9500'
    }

    @classmethod
    def getHmyNetworkUrl(self):
        # Return main net URL if network type is not specified
        if self._network_type == None or self._network_type == '':
            return self._network_end_points['mainnet']
        if self._network_type in self._network_end_points:
            return self._network_end_points[self._network_type]
        # Return Main Net URL if invalid network parameter
        return self._network_end_points['mainnet']
    
    @classmethod
    def getShardForBlsKey(self, key):
        shard = -1
        hmyDir = Globals._hmyDirectory
        nodeUrl = Globals.getHmyNetworkUrl()
        try:
            proc = subprocess.Popen(f'{hmyDir}/./hmy --node="{nodeUrl}" utility shard-for-bls {key}', stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            if err == None:
                response = json.loads(out)
                shard = response['shard-id']
        except Exception as ex:
            HmyBidderLog.error(ex)
        finally:
            return shard
