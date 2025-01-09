# 🌐 Blockchain Endpoints API with FastAPI

This project implements a simple yet extensible **blockchain system** using **FastAPI**. It includes core blockchain functionalities like mining, transaction handling, and UTXO tracking while leveraging modern cryptography for transaction validation.

## 🚀 Features

- **Blockchain Basics**:
  - Create a blockchain with a genesis block.
  - Mine new blocks with Proof-of-Work (PoW).
  - Validate and append blocks to the chain.
- **Transactions**:
  - Add transactions with sender, receiver, amount, and digital signatures.
  - Maintain a UTXO pool for tracking unspent transaction outputs.
- **Cryptographic Security**:
  - Generate key pairs (private/public) for signing transactions.
  - Verify transaction authenticity using ECDSA.
- **FastAPI Endpoints**:
  - Interactive API documentation available via Swagger UI and ReDoc.

```

## 📜 Endpoints

### Core Endpoints

| Endpoint              | Method | Description                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------|
| `/new_transaction`    | POST   | Add a new transaction to the pending list.                                  |
| `/mine_block`         | GET    | Mine a new block with pending transactions.                                 |
| `/add_block`          | POST   | Validate and add a received block to the chain.                             |
| `/chain`              | GET    | Retrieve the entire blockchain.                                             |
| `/utxo_pool`          | GET    | Fetch the UTXO pool.                                                        |

### Cryptographic Endpoints

| Endpoint              | Method | Description                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------|
| `/generate_key_pair`  | GET    | Generate a new public/private key pair for cryptography.                    |
| `/verify_transaction` | POST   | Validate a transaction's signature and UTXOs.                               |

---

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- Pip (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/blockchain-endpoints.git
   cd blockchain-endpoints
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   .\venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   uvicorn blockchain_app:app --reload
   ```

5. **Access the API**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Usage Examples

### Add a New Transaction
```bash
curl -X POST "http://127.0.0.1:8000/new_transaction" \
-H "Content-Type: application/json" \
-d '{
  "id": "tx1",
  "sender": "public_key_sender",
  "receiver": "public_key_receiver",
  "amount": 50.0,
  "input_utxos": ["utxo1"],
  "output_utxos": ["utxo2"],
  "signature": "signature_string"
}'
```

### Mine a New Block
```bash
curl -X GET "http://127.0.0.1:8000/mine_block"
```

### Fetch the Blockchain
```bash
curl -X GET "http://127.0.0.1:8000/chain"
```

### Generate Key Pair
```bash
curl -X GET "http://127.0.0.1:8000/generate_key_pair"
```

---

## 📘 API Documentation

The API is documented using **Swagger UI** and **ReDoc**. Access the documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Cryptography

This project uses **ECDSA (Elliptic Curve Digital Signature Algorithm)** for:
- Generating cryptographic keys.
- Signing transaction data.
- Verifying the authenticity of transactions.

### Libraries Used:
- `ecdsa`: For key pair generation and signature handling.
- `hashlib`: For hashing block and transaction data.

---

## 🛡️ Blockchain Features

- **Proof-of-Work**: Secures the network against spam and abuse.
- **Block Validation**: Ensures immutability and prevents tampering.
- **UTXO Model**: Tracks unspent transaction outputs to ensure double-spending protection.

---

## 🧩 Future Enhancements

- Implement **Peer-to-Peer Networking** for decentralized operation.
- Add support for **Merkle Trees** to optimize transaction validation.
- Extend consensus mechanisms (e.g., Proof-of-Stake or Delegated PoS).
- Build a user-friendly front-end interface.

---

## 🧑‍💻 Contributing

Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request.

---

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for its simplicity and speed.
- [Pydantic](https://pydantic-docs.helpmanual.io/) for robust data validation.
- [ECDSA Library](https://github.com/warner/python-ecdsa) for cryptographic utilities.

---
