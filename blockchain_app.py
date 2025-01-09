from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
import hashlib
import json
import time
import ecdsa  # For cryptography
import uuid  # For generating unique transaction IDs

# Initialize FastAPI app
app = FastAPI()

# Blockchain and Transaction Models
class Transaction(BaseModel):
    id: str
    sender: str
    receiver: str
    amount: float
    input_utxos: List[str]
    output_utxos: List[str]
    signature: str

class Block(BaseModel):
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int
    hash: str

# UTXO Model
class UTXO(BaseModel):
    transaction_id: str
    amount: float
    is_spent: bool

# Blockchain
class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.utxo_pool: Dict[str, UTXO] = {}
        self.difficulty: int = 4
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
            nonce=0,
            hash="",
        )
        genesis_block.hash = self.compute_hash(genesis_block)
        self.chain.append(genesis_block)

    def compute_hash(self, block: Block) -> str:
        block_data = {
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": [tx.dict() for tx in block.transactions],
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
        }
        encoded_block = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def mine_block(self) -> Block:
        if not self.pending_transactions:
            raise HTTPException(status_code=400, detail="No transactions to mine.")
        
        last_block = self.chain[-1]
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            transactions=self.pending_transactions[:],
            previous_hash=last_block.hash,
            nonce=0,
            hash="",
        )

        while not new_block.hash.startswith("0" * self.difficulty):
            new_block.nonce += 1
            new_block.hash = self.compute_hash(new_block)

        self.chain.append(new_block)
        self.pending_transactions.clear()
        self.update_utxo_pool(new_block)
        return new_block

    def validate_block(self, block: Block) -> bool:
        if block.hash != self.compute_hash(block):
            return False
        if not block.hash.startswith("0" * self.difficulty):
            return False
        return True

    def update_utxo_pool(self, block: Block):
        for transaction in block.transactions:
            for utxo_id in transaction.input_utxos:
                if utxo_id in self.utxo_pool:
                    self.utxo_pool[utxo_id].is_spent = True
            
            for utxo_id, amount in zip(transaction.output_utxos, [transaction.amount]):
                self.utxo_pool[utxo_id] = UTXO(
                    transaction_id=transaction.id,
                    amount=amount,
                    is_spent=False,
                )

# Instantiate the blockchain
blockchain = Blockchain()

# Utility Functions
def generate_key_pair():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def sign_data(private_key, data: str):
    return private_key.sign(data.encode()).hex()

def verify_signature(public_key, data: str, signature: str):
    try:
        return public_key.verify(bytes.fromhex(signature), data.encode())
    except ecdsa.BadSignatureError:
        return False

# API Endpoints
@app.post("/new_transaction")
async def new_transaction(transaction: Transaction):
    blockchain.pending_transactions.append(transaction)
    return {"message": "Transaction added successfully.", "transaction": transaction}

@app.get("/mine_block")
async def mine_block():
    try:
        new_block = blockchain.mine_block()
        return {"message": "Block mined successfully.", "block": new_block}
    except HTTPException as e:
        raise e

@app.post("/add_block")
async def add_block(block: Block):
    last_block = blockchain.chain[-1]
    
    if block.previous_hash != last_block.hash:
        raise HTTPException(status_code=400, detail="Invalid previous hash.")
    
    if not blockchain.validate_block(block):
        raise HTTPException(status_code=400, detail="Invalid block.")
    
    blockchain.chain.append(block)
    blockchain.update_utxo_pool(block)
    return {"message": "Block added successfully.", "block": block}

@app.get("/chain")
async def get_chain():
    return {"length": len(blockchain.chain), "chain": blockchain.chain}

@app.get("/utxo_pool")
async def get_utxo_pool():
    return blockchain.utxo_pool

@app.get("/generate_key_pair")
async def generate_key():
    private_key, public_key = generate_key_pair()
    return {
        "private_key": private_key.to_string().hex(),
        "public_key": public_key.to_string().hex()
    }

@app.post("/verify_transaction")
async def verify_transaction(transaction: Transaction):
    for utxo_id in transaction.input_utxos:
        if utxo_id not in blockchain.utxo_pool or blockchain.utxo_pool[utxo_id].is_spent:
            raise HTTPException(status_code=400, detail=f"Invalid or spent UTXO: {utxo_id}")
    
    public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(transaction.sender), curve=ecdsa.SECP256k1)
    is_valid = verify_signature(public_key, json.dumps(transaction.dict()), transaction.signature)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid transaction signature.")
    
    return {"message": "Transaction is valid."}
