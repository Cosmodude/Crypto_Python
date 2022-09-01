from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

Forked_Local_Environments=["mainnet-fork","mainnet-fork-dev"]
Local_Blockchain_Environments = ["development", "ganache-local"]
Decimals = 8
Start_price = 200000000000


def get_account():
    if network.show_active() in Local_Blockchain_Environments or network.show_active() in Forked_Local_Environments:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            Decimals, Start_price, {"from": get_account()}
        )
    print("Mocks deployed!")
