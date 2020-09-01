from pyhmy import account, staking
from utilities.globals import Globals
from utilities.hmybidder_logger import HmyBidderLog

class ValidatorInfo:

    @classmethod
    def getTotalStakedToValidator(self, validatorAddress):
        validator_info = {}
        totalDelegation = 0
        try:
            validator_info = staking.get_validator_information(validatorAddress, Globals.getHmyNetworkUrl())
            #print(validator_info)
            if 'total-delegation' in validator_info:
                totalDelegation = validator_info['total-delegation']
        except Exception as ex:
            HmyBidderLog.error(ex)
        finally:
            return (totalDelegation / Globals._oneAmountDenominator)
    
    @classmethod
    def validateONEAddress(self, oneAddress):
        valid = False
        try:
            valid = account.is_valid_address(oneAddress)
        except Exception as ex:
            HmyBidderLog.error(ex)
        finally:
            return valid
