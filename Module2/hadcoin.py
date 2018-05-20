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
        self.transactions = []  # Empty transactions after adding to the block
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

    # Finds the longest chain in network
    # and updates all the chains to longest chain
    def replaceChain(self):
        network = self.nodes
        longestChain = None
        maxLength = len(self.chain) # Length of current chain
        for node in network: # loop through all nodes in network
            response = requests.get(f'http://{node}/get-chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > maxLength and self.isChainValid(chain):
                    maxLength = length
                    longestChain = chain

        if longestChain:    # if longestChain was updated
            self.chain = longestChain
            return True
        return False


# Part 2 - Mining our Blockchain

# Creating a WebApp
app = Flask(__name__)

# Creating an address for the node on Port on 5000
nodeAddress = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine-block', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    newProof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    blockchain.addTransaction(sender=nodeAddress, receiver='Sid', amount=1)
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

# Checking if a blockchain is valid or not
@app.route('/is-valid', methods=['GET'])
def isValid():
    response = {'isValid': blockchain.isChainValid(blockchain.chain)}
    return jsonify(response), 200

# Adding a new transaction to the blockchain
@app.route('/add-transaction', methods=['POST'])
def addTransaction():
    json = request.get_json()
    transactionKeys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transactionKeys):
        return 'Some elements of the transaction are missing!!', 400
    index = blockchain.addTransaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to block {index}'}
    return jsonify(response), 200


# Part 3 - Decentralizing our Blockchain


# Connecting new nodes


# Running the app
app.run(host='0.0.0.0', port=5000)



