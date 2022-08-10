from solcx import compile_standard 


with open("./Storage.sol", "r") as file:
    storage_file = file.read()

    print(storage_file)

compiled= compile_standard(
    {
        "language": "Solidity",
        "sources": {"Storage.sol",{ "content": storage_file}},
        "settings":
        {
            "outputSelection":
            {
                "*": 
                {"*": ["abi","metadata","evm.bytecode","evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.6")
