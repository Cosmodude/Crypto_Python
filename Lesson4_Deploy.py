from solcx import compile_standard, install_solc
import json
from web3 import Web3 
install_solc("0.6.6")

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

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id=5777
myadress="0x955da76a2E7a87d9D67c6A14969A659c53476f30"
prkey= "04d63be94f9e476f09d26986369e1227b7d67cb1b0c9fae070940409ea83d794"
nonce = w3.eth.getTransactionCount(myadress)

Storage= w3.eth.contract(abi=abi,bytecode=bytecode)

trans= Storage.constructor().buildTransaction({"chainId":chain_id,"from":myadress,"nonce":nonce})

#print(trans)