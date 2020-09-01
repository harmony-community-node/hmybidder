import random

class Globals:
    _walletAddress = ''
    _defaultLogfile = 'hmybidder.log'
    _scriptVersion = 'v1.0'
    _epochBlock = random.randint(100, 200)
    _walletPassFile = 'wallet.pass'
    _network_type = 'mainnet'
    _oneAmountDenominator = 1000000000000000000

    _network_end_points = {
        'mainnet' : 'https://api.s0.t.hmny.io',
        'testnet' : 'https://api.s0.b.hmny.io',
        'pangaea' : 'https://api.s0.b.hmny.io',
        'localnet' : 'http://localhost:9500',
        'partner' : 'https://api.s0.b.hmny.io',
        'stressnet' : 'https://api.s0.b.hmny.io',
        'devnet' : 'https://api.s0.b.hmny.io'
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