from pyhmy import account, staking, blockchain
from utilities.globals import Globals
from utilities.hmybidder_logger import HmyBidderLog
from models import NetworkInfo
import requests

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
    
    @classmethod
    def getNetworkLatestInfo(self):

        block_number = 0
        try:
            block_number = blockchain.get_block_number(Globals.getHmyNetworkUrl())
            #print(f"Block Number {block_number}")
        except Exception as ex:
            HmyBidderLog.error(ex)

        url = Globals.getHmyNetworkUrl()
        try:
            response = staking.get_staking_network_info(url)
            #print(response)
            if response != None and not 'error' in response:
                epoch_last_block = int(response['epoch-last-block'])
                median_raw_stake = float(response['median-raw-stake']) / Globals._oneAmountDenominator
                blocks_to_next_epoch = (epoch_last_block - block_number)
                network_info = NetworkInfo(epoch_last_block, median_raw_stake, block_number, blocks_to_next_epoch)
                return network_info
            else:
                return None
        except Exception as ex:
            HmyBidderLog.error(ex)
