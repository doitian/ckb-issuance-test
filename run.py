import sys
from jsonrpcclient import request

ENDPOINT = 'http://127.0.0.1:8114'
DEFAULT_SECONDARY_EPOCH_REWARD = 613_698_63013698
INITIAL_PRIMARY_EPOCH_REWARD = 1_917_808_21917808

target = int(sys.argv[1]) if len(sys.argv) > 1 else 0

epoch = request(ENDPOINT, "get_epoch_by_number", hex(target)).data.result
stop_block_number = int(epoch['start_number'], 0) + int(epoch['length'], 0)

total_miner_primary_rewards = 0
total_miner_secondary_rewards = 0

for block_number in range(stop_block_number):
    if block_number == 0:
        genesis_epoch = request(
            ENDPOINT, "get_epoch_by_number", '0x0').data.result
        length = int(genesis_epoch['length'], 0)
        total_miner_primary_rewards += int(
            INITIAL_PRIMARY_EPOCH_REWARD / length)
        if INITIAL_PRIMARY_EPOCH_REWARD % length > 0:
            total_miner_primary_rewards += 1
    else:
        hash = request(ENDPOINT, "get_block_hash",
                       hex(block_number + 11)).data.result
        rewards = request(
            ENDPOINT, "get_cellbase_output_capacity_details", hash).data.result
        total_miner_primary_rewards += int(rewards['primary'], 0)
        total_miner_secondary_rewards += int(rewards['secondary'], 0)

dao = bytearray.fromhex(request(ENDPOINT, "get_header_by_number", hex(
    stop_block_number - 1)).data.result['dao'][2:])
s = int.from_bytes(dao[16:24], 'little')

print((INITIAL_PRIMARY_EPOCH_REWARD + DEFAULT_SECONDARY_EPOCH_REWARD) * (target + 1))
print(total_miner_primary_rewards + total_miner_secondary_rewards + s)
