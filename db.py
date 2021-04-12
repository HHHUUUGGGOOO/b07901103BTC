import time
import sys
import json
import hashlib
import pickle

# json (可視覺化)
def store_to_db_json(file_name, blockchain):
    data = {}
    data['Block_Chain'] = []
    for i in range(len(blockchain._chain)):
        data['Block_Chain'].append({
            'Height': blockchain._chain[i]._height,
            'Bits (difficulty)': blockchain._chain[i]._bits,
            'Timestamp': blockchain._chain[i]._time,
            'Transaction': blockchain._chain[i]._transactions,
            'Previous block hash': blockchain._chain[i]._prev_block_hash,
            'Nonce': blockchain._chain[i]._nonce,
            'Hash value': blockchain._chain[i]._hash
        })

    with open(file_name, 'w+') as f:
        json.dump(data, f, indent=4)

def store_to_db_pkl(file_name, blockchain):
    with open(file_name, 'wb') as f:
        pickle.dump(blockchain, f)


