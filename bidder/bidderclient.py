from utilities.globals import Globals
from blockchain.hmyclient import HmyClient
from blockchain.validator import Validator
from bidder.biddingcalculator import BiddingCalculator
from utilities.hmybidder_logger import HmyBidderLog
from models import NetworkInfo, ValidatorInfo, BlsKey

class HMYBidder:
    @classmethod
    def startBiddingProcess(self, network_info):
        requiredBlsKeysCount = BiddingCalculator.calculateBlsKeysForNextEpoch(network_info)
        #print(f'numberOfBlsKeys - {requiredBlsKeysCount}')
        validator_info = Validator.getValidatorInfo(Globals._walletAddress)
        allowedKeysInAShard = int((Globals._totalSlots / Globals._numberOfShards) * (2/3))
        if validator_info != None:
            currentBlsKeysCount = len(validator_info.blsKeys)
            HmyBidderLog.info(f'Current bls keys {currentBlsKeysCount} Ideal bls keys for next epoch {requiredBlsKeysCount}')
            currentBlsKeys = {}
            for shardId in range(0, Globals._numberOfShards):
                shardKey = f'shard{shardId}'
                currentBlsKeys[shardKey] = []

            for blsKey in validator_info.blsKeys:
                if blsKey.shardId != None and blsKey.shardId >= 0:
                    currentBlsKeys[f'shard{blsKey.shardId}'].append(blsKey.blskey)

            if currentBlsKeysCount < requiredBlsKeysCount:
                keysToAdd = requiredBlsKeysCount - currentBlsKeysCount
                HmyBidderLog.info(f'Started adding bls keys, {keysToAdd} key(s) needs to be added')
                try:
                    keysAdded = 0
                    for shardId in range(0, Globals._numberOfShards):
                        shardKey = f'shard{shardId}'
                        if shardKey in Globals._shardsKeys:
                            if len(currentBlsKeys[shardKey]) < len(Globals._shardsKeys[shardKey]):
                                for key in Globals._shardsKeys[shardKey]:
                                    if not key in currentBlsKeys[shardKey]:
                                        if len(currentBlsKeys[shardKey]) < allowedKeysInAShard:
                                            success = HmyClient.addBlsKey(key)
                                            if success:
                                                currentBlsKeys[shardKey].append(key)
                                                HmyBidderLog.info(f'blskey {key} added on Shard : {shardKey}')
                                                keysAdded = keysAdded + 1
                                            else:
                                                HmyBidderLog.info(f'Failed to add blskey {key} on Shard : {shardKey}')
                                        else:
                                            HmyBidderLog.info(f'Shard {shardKey} already has allowed number of keys, keys allowed in shard {allowedKeysInAShard} current number of keys in shard {len(currentBlsKeys[shardKey])}')
                                            break
                                    if keysToAdd == keysAdded:
                                       break
                        if keysToAdd == keysAdded:
                            break
                except Exception as ex:
                    HmyBidderLog.error(f'StartBidding Process Add Key {ex}')
                    
            elif currentBlsKeysCount > requiredBlsKeysCount:
                keysToRemove = abs(requiredBlsKeysCount - currentBlsKeysCount)
                HmyBidderLog.info(f'Started removing bls keys, {keysToRemove} key(s) needs to be removed')
                try:
                    keysRemoved = 0
                    for shardId in range(0, Globals._numberOfShards):
                        shardKey = f'shard{shardId}'
                        if len(currentBlsKeys[shardKey]) > 0:
                            for key in currentBlsKeys[shardKey]:
                                success = HmyClient.removeBlsKey(key)
                                if success:
                                    currentBlsKeys[shardKey].remove(key)
                                    HmyBidderLog.info(f'blskey {key} removed on Shard : {shardKey}')
                                    keysRemoved = keysRemoved + 1
                                else:
                                    HmyBidderLog.info(f'Failed to remove blskey {key} on Shard : {shardKey}')
                                if keysToRemove == keysRemoved:
                                    break
                        if keysToRemove == keysRemoved:
                            break
                except Exception as ex:
                    HmyBidderLog.error(f'StartBidding Process Remove Key {ex}')
            logString = 'Blskeys : '
            for shardId in range(0, Globals._numberOfShards):
                shardKey = f'shard{shardId}'
                logString = f'{logString} {shardKey}[{len(currentBlsKeys[shardKey])}], '
            HmyBidderLog.info(logString)