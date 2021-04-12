import time
import sys
import os
import hashlib
import json
import pickle
from PoW import Proof_of_Work
from db import store_to_db_json, store_to_db_pkl

# Create block class (para: prevHash, height, transaction)
class Block:
    def __init__(self, prev_block_hash, height, trans):
        self._prev_block_hash = prev_block_hash     # the last block's hash value (in block chain list) 
        self._height = height   # height = prev_block.height + 1 = block chain list's index  
        self._transactions = trans 
        self._nonce = 0   # default = 0
        self._bits = 11     # now no need to change           
        self._time = time.asctime(time.localtime(time.time()))   # Thu Apr 7 10:05:21 2016        
        self.hash_block()   

    def __str__(self):
        return 'Block(timestamp: {0!r},\ntransaction_list: {1!r},\nprev_block_hash={2!r},\nhash={3!r},\nnonce={4!r},\nheight={5!r},\nbits={6!r})'.format(
            self._time, self._transactions, self._prev_block_hash, self._hash, self._nonce, self._height, self._bits
        ) 

    def hash_block(self):   # calculates the hash of the block and update the hash value to see whether it has enough '0' header (difficulty = # of 0 = 20)
        nonce, hash = Proof_of_Work(self).run()
        # self._nonce, self._hash = nonce, hash.encode('utf-8')
        self._nonce, self._hash = nonce, hash

# Create block chain class
class Block_Chain:
    def __init__(self, trans):
        self._trans = trans
        self._chain = []    # a list of Blocks representing the blockchain
        self._dict_with_height = {}     # { '0': block_1, ... }
        self.new_Genesis_Block()    # create a genesis block

    def new_Genesis_Block(self):
        genesis_block = Block('0', 0, self._trans)
        self._chain.append(genesis_block)
        self._dict_with_height[str(genesis_block._height)] = genesis_block

    def add_new_block(self, trans):
        # transaction = 'Block no.' + str(self._chain[-1]._height+1)
        new_block = Block(self._chain[-1]._hash, self._chain[-1]._height+1, trans)
        self._chain.append(new_block)
        self._dict_with_height[str(new_block._height)] = new_block


if __name__ == '__main__':
    while True:
        cmd = input('\nPlease enter the instruction (or use \"-h\" to search instruction, use \"exit\" to stop)\n[Enter]: ')
        # 字串分成三部分
        parse_cmd = cmd.split(' ', 2) 
        if (cmd == '-h'):
            print('Add a block:                   \"addblock -transaction {transaction message}\"')
            print('Print a block chain:           \"printchain\"')
            print('Print height of the chain:     \"printheight\"')
            print('Print specific height block:   \"printblock -height {(int)height}\"')
            print('Exit the execution:            \"exit\" (It will go back to the previous structure.)')
        # "addblock -transaction": 判斷式改用split, 看list[0], list[1]是不是 "addblock", "-transaction"
        elif (len(parse_cmd) == 3) and (parse_cmd[0] == "addblock") and (parse_cmd[1] == "-transaction"):
            count = 1
            trans = parse_cmd[2]
            if (len(os.listdir('database')) == 0):
                print('Mining the Genesis block...')
                genesis = Block_Chain(trans)
                print('Finish mining a block...\n')
            else:
                print('Mining a new block...')
                with open('database/Block_Chain.pkl', 'rb') as f:
                    genesis = pickle.load(f)
                block = Block_Chain.add_new_block(genesis, trans)
                count += 1
                print('Finish mining a block...\n')
            while True:
                mine = input('Do you want to mine a block ?\n[y/n]: ')
                if (mine in ['n', 'N']):
                    print('Totally mine %d blocks !' % count)
                    break
                elif (mine in ['y', 'Y']):
                    trans = input('\nPlease enter your transaction message: ')
                    print('Mining a new block...')
                    block = Block_Chain.add_new_block(genesis, trans)
                    count += 1
                    print('Finish mining a block...\n')
                    continue
                elif (mine not in ['y', 'n', 'Y', 'N']): 
                    continue
            # store to database_json
            file_name_json = 'database/Block_Chain.json'
            store_to_db_json(file_name_json, genesis)
            # store to database_json
            file_name_pickle = 'database/Block_Chain.pkl'
            store_to_db_pkl(file_name_pickle, genesis)
        # 印出目前有哪些編號的block chain, 請他選一個, 再問他要不要印出特定高度
        elif (cmd == "printchain"):    
            block_name = 'database/Block_Chain.json'
            with open(block_name, 'r') as f:
                json_data = json.load(f)
            print(json.dumps(json_data, indent=2))
        elif (cmd == "printheight"):
            block_name = 'database/Block_Chain.json'
            with open(block_name, 'r') as f:
                json_data = json.load(f)
            print(len(json_data['Block_Chain']))
        elif (len(parse_cmd) == 3) and (parse_cmd[0] == "printblock") and (parse_cmd[1] == "-height") and (parse_cmd[2].isdigit() == True):
            h = parse_cmd[2]
            block_name = 'database/Block_Chain.json'
            with open(block_name, 'r') as f:
                json_data = json.load(f)
            h_bound = len(json_data['Block_Chain'])
            if (0 <= eval(h) < h_bound):
                print(json.dumps(json_data['Block_Chain'][eval(h)], indent=2))
            else: 
                print('h must be between 0 to %d' % (h_bound-1))
        elif (cmd == "exit"):
            break
        else:
            continue


# sha = hashlib.sha256()
# sha.update(pre_data).encode()
# return sha.hexdigest()

# SQLite --> database
# PoW --> # 把所有block資訊轉成str, join起來, 存成data list, 做encode成bytes, nonce一直跑, 丟進sha hash產生並update(), 用hexhash提出hash值, 去看前面有沒有20個0, 有就找到了, 用int16去比較她跟target的大小, 要比target小

