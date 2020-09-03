from builtins import object


class NetworkInfo(object):
    def __init__(self, epoch_last_block, median_raw_staking, block_number, blocks_to_next_epoch):
        self.epoch_last_block = epoch_last_block
        self.median_raw_staking = median_raw_staking
        self.block_number = block_number
        self.blocks_to_next_epoch = blocks_to_next_epoch

    def to_dict(self):
        return dict(
            epoch_last_block = self.epoch_last_block,
            median_raw_staking = self.median_raw_staking,
            block_number = self.block_number,
            blocks_to_next_epoch = self.blocks_to_next_epoch
        )

    @classmethod
    def from_dict(cls, data):
        return NetworkInfo(data["epoch_last_block"],
                         data["median_raw_staking"],
                         data["block_number"],
                         data["blocks_to_next_epoch"])
    
class BlsKey(object):
    def __init__(self, blskey, shardId):
        self.blskey = blskey
        self.shardId = shardId

    def to_dict(self):
        return dict(
            blskey = self.blskey,
            shardId = self.shardId
        )

    @classmethod
    def from_dict(cls, data):
        return BlsKey(data["blskey"],
                         data["shardId"])

class ValidatorInfo(object):
    def __init__(self, active_status, epos_status, total_delegation, blsKeys):
        self.active_status = active_status
        self.epos_status = epos_status
        self.total_delegation = total_delegation
        self.blsKeys = blsKeys

    def to_dict(self):
        return dict(
            active_status = self.active_status,
            epos_status = self.epos_status,
            total_delegation = self.total_delegation,
            blsKeys = self.blsKeys
        )

    @classmethod
    def from_dict(cls, data):
        return ValidatorInfo(data["active_status"],
                         data["epos_status"],
                         data["total_delegation"],
                         data["blsKeys"])