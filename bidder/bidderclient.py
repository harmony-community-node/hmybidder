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
            
            parts = Globals._allowedShardKeys.split(":")
            userAllowedKeysInShard = {
                'shard0' : len(Globals._shardsKeys['shard0']),
                'shard1' : len(Globals._shardsKeys['shard1']),
                'shard2' : len(Globals._shardsKeys['shard2']),
                'shard3' : len(Globals._shardsKeys['shard3'])
            }
            if len(parts) == 8:
                userAllowedKeysInShard = {
                    'shard0' : int(parts[1]),
                    'shard1' : int(parts[3]),
                    'shard2' : int(parts[5]),
                    'shard3' : int(parts[7])
                }
            arrKeysToAdd = []
            arrKeysToRemove = []
            HmyBidderLog.info(f'Shard Keys Config : {userAllowedKeysInShard}')
            HmyBidderLog.info('Identifying the extra keys, if Shard Keys Config reduced number of keys allowed in each shard')
            for shardId in range(0, Globals._numberOfShards):
                shardKey = f'shard{shardId}'
                while len(currentBlsKeys[shardKey]) > userAllowedKeysInShard[shardKey]:
                    key = currentBlsKeys[shardKey][0]
                    currentBlsKeys[shardKey].remove(key)
                    currentBlsKeysCount = currentBlsKeysCount - 1
                    arrKeysToRemove.append(
                        {
                            'key' : key,
                            'shard_key' : shardKey
                        }
                    )
            HmyBidderLog.info('Finished Identifying the extra keys')                
            # Remove the keys if Shard Keys Config reduced number of keys allowed in each shard
            if currentBlsKeysCount < requiredBlsKeysCount:
                keysToAdd = requiredBlsKeysCount - currentBlsKeysCount
                if (keysToAdd - len(arrKeysToRemove)) > 0:
                    HmyBidderLog.info(f'Started identifying bls keys to be added, {keysToAdd - len(arrKeysToRemove)} key(s) needs to be added')
                elif (keysToAdd - len(arrKeysToRemove)) < 0:
                    HmyBidderLog.info(f'{keysToAdd - len(arrKeysToRemove)} key(s) needs to be removed, due to Shard Keys config change')
                try:
                    keysAdded = 0
                    for shardId in range(0, Globals._numberOfShards):
                        shardKey = f'shard{shardId}'
                        if shardKey in Globals._shardsKeys:
                            if len(currentBlsKeys[shardKey]) < len(Globals._shardsKeys[shardKey]):
                                for key in Globals._shardsKeys[shardKey]:
                                    if not key in currentBlsKeys[shardKey]:
                                        if len(currentBlsKeys[shardKey]) < allowedKeysInAShard and len(currentBlsKeys[shardKey]) < userAllowedKeysInShard[shardKey]:
                                            currentBlsKeys[shardKey].append(key)
                                            arrKeysToAdd.append(
                                                {
                                                    'key' : key,
                                                    'shard_key' : shardKey
                                                }
                                            )
                                            keysAdded = keysAdded + 1
                                        else:
                                            #HmyBidderLog.info(f'Shard {shardKey} already has allowed number of keys, keys allowed in shard {userAllowedKeysInShard[shardKey]} current number of keys in shard {len(currentBlsKeys[shardKey])}')
                                            break
                                    if keysToAdd == keysAdded:
                                       break
                        if keysToAdd == keysAdded:
                            break
                except Exception as ex:
                    HmyBidderLog.error(f'StartBidding Process Add Key {ex}')
                    
            elif currentBlsKeysCount > requiredBlsKeysCount:
                keysToRemove = abs(requiredBlsKeysCount - currentBlsKeysCount)
                HmyBidderLog.info(f'Started identifying bls keys to be removed, {keysToRemove} key(s) needs to be removed')
                try:
                    keysRemoved = 0
                    for shardId in range(0, Globals._numberOfShards):
                        shardKey = f'shard{shardId}'
                        if len(currentBlsKeys[shardKey]) > 0:
                            for key in currentBlsKeys[shardKey]:
                                currentBlsKeys[shardKey].remove(key)
                                arrKeysToRemove.append(
                                    {
                                        'key' : key,
                                        'shard_key' : shardKey
                                    }
                                )
                                keysRemoved = keysRemoved + 1                                            
                                if keysToRemove == keysRemoved:
                                    break
                        if keysToRemove == keysRemoved:
                            break
                except Exception as ex:
                    HmyBidderLog.error(f'StartBidding Process Remove Key {ex}')

            for dictKey in arrKeysToAdd:
                key = dictKey['key']
                shardKey = dictKey['shard_key']
                success = HmyClient.addBlsKey(key)
                if success:
                    HmyBidderLog.info(f'blskey {key} added on Shard : {shardKey}')
                else:
                    HmyBidderLog.info(f'Failed to add blskey {key} on Shard : {shardKey}')

            for dictKey in arrKeysToRemove:
                key = dictKey['key']
                shardKey = dictKey['shard_key']                    
                success = HmyClient.removeBlsKey(key)            
                if success:
                    HmyBidderLog.info(f'blskey {key} removed on Shard : {shardKey}')
                else:
                    HmyBidderLog.info(f'Failed to remove blskey {key} on Shard : {shardKey}')

            logString = 'Blskeys : '
            for shardId in range(0, Globals._numberOfShards):
                shardKey = f'shard{shardId}'
                logString = f'{logString} {shardKey}[{len(currentBlsKeys[shardKey])}], '
            HmyBidderLog.info(logString)
    
