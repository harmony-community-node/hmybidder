from utilities.globals import Globals
from blockchain.validator import Validator
from models import NetworkInfo

class BiddingCalculator:

    @classmethod
    def calculateBlsKeysForNextEpoch(self) -> int:
        totalStaked = Validator.getTotalStakedToValidator(Globals._walletAddress)
        network_info = Validator.getNetworkLatestInfo()
        median_stake = network_info.median_raw_staking
        if Globals._leverage != 0:
            median_stake = median_stake + ((median_stake * Globals._leverage) / 100)
        
        return int(totalStaked / median_stake)

