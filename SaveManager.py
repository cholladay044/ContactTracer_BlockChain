import os.path
import json
from Blockchain import Transaction, Block


# Probably do some try catch stuff here to generate the file and ensure each block is different
# Figure out if we want a generic path here too
def save_blockchain(data, pth):
    with open(os.getcwd() + pth, 'w+') as jsonfile:
        json.dump(data, jsonfile)


def save_file(pth, block):
    feeds = load_blockchain(pth)
    with open(os.getcwd() + pth, mode='w', encoding='utf-8') as feedsjson:
        entry = {'index': block.index, 'transactions': json.loads(block.transactToJSON()), 'timestamp': block.timestamp,
                 'previous_hash': block.previous_hash, 'nonce': block.nonce, 'hash': block.hash}
        feeds.append(entry)
        json.dump(feeds, feedsjson)


def init_file(pth):
    with open(os.getcwd() + pth, mode='w', encoding='utf-8') as f:
        json.dump([], f)


# Returns a list of Transaction given json data.
def parse_transactions(tra):
    transactions = []

    for x in tra:
        t = Transaction(x['user_a_id'],
                        x['user_b_id'],
                        x['user_a_location'],
                        x['user_b_location'],
                        x['time_of_contact'])

        transactions.append(t)

    return transactions


def parse_blocks(blocks):
    blocks = [
        Block(b['index'], parse_transactions(b['transactions']), b['timestamp'], b['previous_hash'], b['timestamp'])
        for b in blocks]
    for block in blocks:
        block.compute_hash()


# rewrite
# This is where the data needs to be sent out to be deserialized after loading
def load_blockchain(pth):
    if os.path.exists(os.getcwd() + pth):
        file = open(os.getcwd() + pth)
        out = json.load(file)
        return out
    else:
        return []
