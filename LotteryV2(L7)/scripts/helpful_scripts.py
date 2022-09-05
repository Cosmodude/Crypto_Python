from brownie import (
    network,
    accounts,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    VRFCoordinatorV2Mock,
    LinkToken,
    interface,
)
import os, time
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
MAINNET_FORK = "mainnet-fork-dev"
LOCAL_BLOCKCHAINS = ["development", "ganache-local"]
contract_to_mock = {
    "eth-usd-priceFeed": MockV3Aggregator,
    "vrf-coordinator": VRFCoordinatorMock,
    "vrf-coordinator-v2": VRFCoordinatorV2Mock,
    "link-token": LinkToken,
}

# id => the account I set up i brownie i.e my custom account
# index => just a account index
def get_acc(id=None, index=None):
    if id:
        return accounts[id]
    elif index:
        return accounts[index]
    elif (
        network.show_active() in LOCAL_BLOCKCHAINS
        or network.show_active() in MAINNET_FORK
    ):
        return accounts[0]
    return accounts.add(os.getenv("priv_key"))  # My MetaMask Account


def get_contract(contract_name):
    """This function will return the contract address form the brownie config if defined,
    otherwise it will deploy and return a mock version of that contract.
    Args:
        contract_name => string
    Returns:
        brownie.network.contract
        e.g MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]
    # contract_type now has MockV3Aggregator address
    if network.show_active() in LOCAL_BLOCKCHAINS:
        if len(contract_type) <= 0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        price_feed_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, price_feed_address, contract_type.abi
        )
    return contract


def deploy_mock(decimals=DECIMALS, start_val=STARTING_PRICE):
    acc = get_acc()
    MockV3Aggregator.deploy(decimals, start_val, {"from": acc})
    link_token_address = LinkToken.deploy({"from": acc})
    VRFCoordinatorMock.deploy(link_token_address, {"from": acc})
    VRFCoordinatorV2Mock.deploy(10, 10, {"from": acc})


LINK_AMOUNT = 3000000000000000000
# 0.4 LINK


def fund_with_link(contract_address, acc=None, link_token=None, amount=LINK_AMOUNT):
    if acc:
        acc = acc
    else:
        acc = get_acc()

    if link_token:
        link_token = link_token
    else:
        link_token = get_contract("link-token")
    # 7.43.48 Interface working example to replace Line 55
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token.transfer(contract_address, amount, {"from": acc})
    tx.wait(1)
    print(f"Contract Funded with Link")
    return tx