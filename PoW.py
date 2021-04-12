import time
import sys
import hashlib

# Proof of Work
class Proof_of_Work:

    max_nonce = sys.maxsize
    target_bits = 11

    def __init__(self, block):
        self._block = block
        self._target = 1 << (256 - Proof_of_Work.target_bits)

    def _prepare_data(self, nonce):
        data_list = [str(self._block._prev_block_hash),
                     str(self._block._height),
                     self._block._transactions,
                     str(nonce),
                     str(self._block._bits),
                     str(self._block._time)
                    ]
        output_msg = ''.join(data_list)
        return output_msg.encode('utf-8')
    
    def sum256_hex(*args):
        # hashing
        m = hashlib.sha256()
        for arg in args:
            m.update(str(arg).encode('utf-8'))
        return m.hexdigest()

    def validate(self):
        # Validates a block's PoW
        data = self._prepare_data(self._block.nonce)
        hash_hex = self.sum256_hex(data)
        hash_int = int(hash_hex, 16)
        return True if hash_int < self._target else False
    
    def run(self):
        # Performs a proof-of-work
        nonce = 0
        # print basic information
        print('Height: ', self._block._height)
        print('Bits (difficulty): ', self._block._bits)
        print('Timestamp: ', self._block._time)
        print('Transaction: ', self._block._transactions)
        print('Previous block hash: ', self._block._prev_block_hash)
        while nonce < self.max_nonce:
            data = self._prepare_data(nonce)
            hash_hex = self.sum256_hex(data)
            sys.stdout.write("nonce: %d \r" % (nonce))
            # sys.stdout.write("hash_hex: %s \r" % (hash_hex))
            hash_int = int(hash_hex, 16)

            if hash_int < self._target:
                break
            else:
                nonce += 1
        print('\n')
        print('Hash value: ', hash_hex)
        return nonce, hash_hex