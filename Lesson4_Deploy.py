from solcx import compile_standard, install_solc
import json
from web3 import Web3 
from dotenv import load_dotenv
import os
install_solc("0.6.6")

load_dotenv()

with open("./Storage.sol", "r") as file:
    storage_file = file.read()

    #print(storage_file)

compiled= compile_standard(
    {
        "language": "Solidity",
        "sources": {"Storage.sol":{ "content": storage_file}},
        "settings":
        {
            "outputSelection":
            {
                "*": 
                {"*": ["abi","metadata","evm.bytecode","evm.sourceMap"]}
            }
        },
    },
    #solc_version="0.6.6"
)
  
with open("compiled_code.json","w") as file:
    json.dump(compiled,file)

#get bytecode
bytecode= compiled["contracts"]["Storage.sol"]["Storage"]["evm"][
    "bytecode"
]["object"]

#get abi
abi=compiled["contracts"]["Storage.sol"]["Storage"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7986"))
chain_id=1337
myadress="0x443345069D0a30C9c6FC35eD5FE7426FfF3BB07F"
prkey= os.getenv("PRIV_KEY")
nonce = w3.eth.getTransactionCount(myadress)

Storage= w3.eth.contract(abi=abi,bytecode=bytecode)

trans= Storage.constructor().buildTransaction({"chainId":chain_id,"from":myadress,"gasPrice": w3.eth.gas_price,"nonce":nonce})

#print(trans)

signed=w3.eth.account.sign_transaction(trans,private_key=prkey)
Thash = w3.eth.send_raw_transaction(signed.rawTransaction)
Treceipt =w3.eth.wait_for_transaction_receipt(Thash)

#Work with the contract

Contract = w3.eth.contract(address=Treceipt.contractAddress, abi=abi)
print(Contract.functions.retrieve().call())
storetransaction = Contract.functions.str(15).build_transaction({"chainId":chain_id,"gasPrice": w3.eth.gas_price,
"from":myadress,"nonce":nonce+1})
print(Contract.functions.retrieve().call())
#print(trans)
signed_contract= w3.eth.account.sign_transaction(storetransaction, private_key =prkey )
Tr_send= w3.eth.send_raw_transaction(signed_contract.rawTransaction)
Tr_receipt= w3.eth.wait_for_transaction_receipt(Tr_send)
print(Contract.functions.retrieve().call())

