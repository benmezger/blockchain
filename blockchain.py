import time
import hashlib
import uuid
import json

class Blockchain(object):
    """
    Responsible for managing the chain. This is where transactions (tx)
    will be stored
    """
    def __init__(self):
        self.chain = []
        self.current_tx = []

        # When the Blockchain() is initiated, we need to seed it with a genesis block.
        # A genesis block is a block with no predecessors.
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof :int, previous_hash=None) -> dict:
       """
       This created a new block in the chain.

       :param proof: <int> Proof of work
       :param previous_hash: <str> Hash of the previous block. If it's the
                             first block (genesis), then it's none.
        """
       block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'tx': self.current_tx,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

       self.current_tx = [] # reset the list of current tx
       self.chain.append(block)
       return block

    def new_tx(self, **kwargs) -> int:
        """
        Creates a new transaction (tx)
        Kwargs expects to have:

        :param kwargs:
            - sender: <str> address (hash) of the sender
            - receiver: <str> address (hash) of a receiver
            - amount: <float> amount the sender is sending to a receiver
        :return: The index of a block that holds this tx
        """
        self.current_tx.append(kwargs)
        return self.last_block['index'] + 1 # return the next block to be mined.

    @staticmethod
    def hash(block :dict) -> str:
        """
        Creates a SHA-256 of a block.

        :param block: <dict> a block
        :return: the sha256 of block.
        """
        block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block).hexdigest()

    def pow(self, last_p :int) -> int:
        """
        Proof of work algorithm.

        - find a number p such that hash(pp') contains leading 4 zeroes, where p
          is the previous p'
        - p is the previous proof, and p' is the new one

        :param: last_p <int>
        :return <int>
        """

        proof = 0
        while self.validate_proof(last_p, proof) is False:
            proof += 1
        return proof

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def validate_proof(last_p :int, p :int) -> bool:
        """
        Validates the proof by asking: does hash(last_p, p) contain 4 leading 0s?

        :param: last_p <int> previous proof
        :param p <int> current proof
        :return <bool> True if ok, false if not.
        """

        # Note: if we want to ajust the difficulty of the algorihm, we could simply
        # modify the number of leading 0s.
        guess = f'{last_p}{p}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
