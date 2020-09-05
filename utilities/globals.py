import random
from utilities.hmybidder_logger import HmyBidderLog

class Globals:
    _totalSlots = 640
    _hmyDirectory = '~/hmydir'
    _logFile = ''
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
    _numberOfShards = 4
    _shardsKeys = {
        'shard0' : [],
        'shard1' : [],
        'shard2' : [],
        'shard3' : []
    }

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
    