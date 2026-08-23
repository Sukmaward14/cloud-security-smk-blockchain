from web3 import Web3

# =========================
# KONEKSI KE GANACHE
# =========================

GANACHE_URL = "http://127.0.0.1:7545"

web3 = Web3(
    Web3.HTTPProvider(GANACHE_URL)
)

# =========================
# CONTRACT ADDRESS
# =========================

CONTRACT_ADDRESS = Web3.to_checksum_address(
    "0xEf25A262b32DC8595Cb986B9cD5A95901f0F084B"
)

# =========================
# ABI SMART CONTRACT
# =========================

CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_documentId",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_documentHash",
                "type": "string"
            }
        ],
        "name": "registerDocument",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_documentId",
                "type": "uint256"
            }
        ],
        "name": "getDocument",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


# =========================
# MEMBUAT OBJECT CONTRACT
# =========================

contract = web3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=CONTRACT_ABI
)

def get_document_from_blockchain(document_id):
    try:
        result = contract.functions.getDocument(
            document_id
        ).call()

        return {
            "document_id": result[0],
            "document_hash": result[1],
            "timestamp": result[2],
            "uploader": result[3]
        }

    except Exception as e:
        print("Blockchain error:", e)
        return None

def register_document_on_blockchain(document_id, document_hash):

    try:

        # Ambil akun pertama dari Ganache
        account = web3.eth.accounts[0]

        # Buat transaksi
        transaction = contract.functions.registerDocument(
            document_id,
            document_hash
        ).transact({
            "from": account
        })

        # Tunggu transaksi selesai
        receipt = web3.eth.wait_for_transaction_receipt(
            transaction
        )

        return receipt["transactionHash"].hex()

    except Exception as e:

        print("Blockchain register error:", e)

        return None