# Module 2 - Create a Cryptocurrency

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain
class Blockchain:
    # Initialize Blockchain
    def __init__(self):
        self.chain = [] # list containing different blocks
        self.transactions = [] # list of transactions
        self.createBlock(proof = 1, previousHash = '0') # Create a genesis block
        self.nodes = set() # set of nodes in the network

    # Create a block in the blockchain
    def createBlock(self, proof, previousHash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'transactions': self.transactions,
                 'previousHash': previousHash}
        self.transactions = []
        self.chain.append(block)
        return block

    # Get previous block
    def getPreviousBlock(self):
        return self.chain[-1]

    # Proof of work
    def proofOfWork(self, previousProof):
        newProof = 1        # we will increment this variable by 1 for each iteration
        checkProof = False
        while checkProof is False:
            ## Should be non symmetrical i.e newProof + previousProof is symmetrical
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()

            ## check first 4 characters
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        return newProof

    # Get the hash of the block
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    # Check the validity of the chain
    def isChainValid(self, chain):
        previousBlock = chain[0]        # first block of the chain
        blockIndex = 1
        while blockIndex < len(chain):
            currentBlock = chain[blockIndex]

            # Check previous hash
            if currentBlock['previousHash'] != self.hash(previousBlock):
                return False

            # Validate Proof
            previousProof = previousBlock['proof']
            currentBlockProof = currentBlock['proof']
            hashOperation = hashlib.sha256(str(currentBlockProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False

            blockIndex += 1
            previousBlock = currentBlock

        return True

    # Adds a transaction to the list
    def addTransaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.transactions.append(transaction)
        previousBlock = self.getPreviousBlock()
        return previousBlock['index'] + 1

    # Adds a new node to the network
    def addNode(self, address):
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netlock)


# Part 2 - Mining our Blockchain

# Creating a WebApp
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine-block', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    newProof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    newBlock = blockchain.createBlock(newProof, previousHash)
    response = {'message': 'Congratulations, you just mined a block!',
                'block': newBlock}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get-chain', methods=['GET'])
def getChain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is-valid', methods=['GET'])
def isValid():
    response = {'isValid': blockchain.isChainValid(blockchain.chain)}
    return jsonify(response), 200

# Running the app
app.run(host='0.0.0.0', port=5000)


# Part 3 - Decentralizing our Blockchain



