# Module 1 - Create a Blockchain

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:

    # Initialize Blockchain
    def __init__(self):
        self.chain = [] # list containing different blocks
        self.createBlock(proof = 1, previousHash = '0') # Create a genesis block

    # Create a block in the blockchain
    def createBlock(self, proof, previousHash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previousHash': previousHash}

# Part 2 - Mining our Blockchain