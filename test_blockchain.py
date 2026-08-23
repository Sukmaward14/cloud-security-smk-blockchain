from web3 import Web3

# Alamat RPC Server dari Ganache
ganache_url = "http://127.0.0.1:7545"

# Membuat koneksi ke Ganache
web3 = Web3(
    Web3.HTTPProvider(ganache_url)
)

# Mengecek koneksi
if web3.is_connected():

    print("================================")
    print("BERHASIL TERHUBUNG KE GANACHE")
    print("================================")

    print("RPC Server:", ganache_url)
    print("Chain ID:", web3.eth.chain_id)
    print("Jumlah Block:", web3.eth.block_number)

else:

    print("================================")
    print("GAGAL TERHUBUNG KE GANACHE")
    print("================================")