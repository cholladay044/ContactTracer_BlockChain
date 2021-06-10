from hashlib import sha256
from time import time
import json
import os.path

class Transaction:
    """
    Represents a Transaction that goes into a block within a blockchain.
    """
    
    def __init__(self, user_a_id, user_b_id, user_a_location, user_b_location, time_of_contact):
        """
        Transaction Constructor
        Params:

        user_a_id       -- Unique ID of User A
        user_b_id       -- Unique ID of User B
        user_a_location -- Location of  User A
        user_b_location -- Location of  User B
        time_of_contact -- Unix Timestamp of when the two users made direct contact
        """

        self.user_a_id = user_a_id
        self.user_b_id = user_b_id
        self.user_a_location = user_a_location
        self.user_b_location = user_b_location
        self.time_of_contact = time_of_contact

    def __str__(self):
        return "[ Users: " + str(self.user_a_id) + ", " + str(self.user_b_id) + " --- @ " + str(
            self.time_of_contact) + "]"

    __repr__ = __str__



class Block:
    """
    Represents a block of transactions, a piece of a blockchain.
    """

    def __init__(self, index, transactions, timestamp, previous_hash, nonce, hash=None):
        """
        Block Constructor
        Params:

        index           -- Index of the block.
        transactions    -- A Pandas Series of transaction objects, default: Empty Pandas Series.
        timestamp       -- Unix Timestamp of block creation time.
        previous_hash   -- sha256 digest of the previous block in the blockchain.
        nonce           -- String appended to the block to ensure a unique hash is generated.
        """
        
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.index = index
        self.hash = hash

    def get_transactions_with_user(self, user_id):
        return [t for t in self.transactions if t.user_a_id == user_id or t.user_b_id == user_id]

    def blockToJSON(self):
        return json.dumps(self, default=lambda Block: Block.__dict__)

    def transactToJSON(self):
        return json.dumps(self.transactions, default=lambda transaction: transaction.__dict__)

    def compute_hash(self):
        """
        Computes the sha256 digest from an instance of the Block class (self)
        Side Effect: set self.hash to digest()
        """

        self.hash = self.__hash__()

    def __hash__(self):
        inputs = str(self.nonce) + str(self.previous_hash) + str(self.timestamp) + str(self.transactions) + str(
            self.index)
        inputs = inputs.encode("utf-8")
        return str(sha256(inputs).hexdigest())

    def __str__(self):
        _str = self.hash + ": "
        for transaction in self.transactions:
            _str += "\n\t" + str(transaction)
        return _str

    __repr__ = __str__


class Blockchain:
    """
    Represents the Blockchain where Direct User Contact is stored
    Members:
    chain -- Pandas Series of blocks, chained by hashes
    """

    def __init__(self, chain=None):
        """
        Blockchain Constructor
        Params:
        chain -- Pandas Series of chained Block objects, default: Empty Series
        returns -- Blockchain
        """

        if chain is None:
            chain = []
        self.chain = chain

    def create_genesis_block(self, timestamp=int(time())):
        """
        Creates the first block in the blockchain, allowing future chaining.
        The first block contains a single transaction with a timestamp of NOW
        """

        t = Transaction(-1, -1, 0.0, 0.0, timestamp)
        self.build_block([t])

    def get_last_block(self):
        """
        Returns the last block in the blockchain
        NOTE: The last block in the blockchain will not have a hash until another block is created to calculate the
        previous_hash
        """

        if len(self.chain) == 0:
            return None
        return self.chain[-1]

    def build_block(self, transactions, timestamp=int(time())):
        """
        Builds a block for the blockchain and appends it to the end.
        Params:
        transactions -- Pandas Series of Transaction objects.
        compute_hash -- Should the last block in the chain have its hash calculated as this block is being built?
                        Default: True
        """

        # Create the block, without a previous_hash if it's the genesis block
        b = Block((self.get_last_block().index + 1) if self.get_last_block() is not None else 0, transactions,
                  timestamp, self.get_last_block().hash if self.get_last_block() is not None else 0,
                  timestamp)
        b.compute_hash()
        # Append the block to the blockchain
        self.chain.append(b)

    def get_chain(self):
        """
        Returns the entire blockchain as a Pandas Series
        """

        return self.chain

    def get_user_transactions(self, user_id, start, end):
        blocks = [b for b in self.chain if start <= b.timestamp <= end]
        return [t for b in blocks for t in b.get_transactions_with_user(user_id)]

    def __str__(self):
        _str = ""
        for block in self.chain:
            _str += str(block) + "\n"
        return _str
