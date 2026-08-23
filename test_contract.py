from blockchain import contract

try:
    result = contract.functions.getDocument(1).call()

    print("================================")
    print("BERHASIL MEMBACA CONTRACT")
    print("================================")
    print(result)

except Exception as e:

    print("================================")
    print("GAGAL MEMBACA CONTRACT")
    print("================================")
    print(e)