from blockchain import Blockchain
from uuid import uuid4

from flask import Flask, jsonify, request

app = Flask(__name__)

# unique address for this node
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine():
    """
    This endpoint needs to do 3 things:
    1. calculate pow
    2. reward miner by adding a tx giving 1 "coin"
    3. forge a new block and add it to the chain
    """
    last_block = blockchain.last_block
    last_proof = blockchain.last_block['proof']
    proof = blockchain.pow(last_proof)

    # we now receive a reward for finding the proof
    # sender = 0 means this node has mined a new coin
    blockchain.new_tx(sender="0", receiver=node_identifier, amount=1)

    ## forge a block and add it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New block",
        "index": block['index'],
        "tx": block["tx"],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route("/tx/new", methods=["POST"])
def new_tx():
    values = request.get_json()

    # check if fields are in the POST'ed data
    required = ['sender', 'amount', 'receiver']
    if not all(k in values for k in required):
        return "Missing values", 400
    i = blockchain.new_tx(**values)
    response = {
        "message": f"Transaction added to block {i}"
    }
    return jsonify(response), 201

@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'len': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
