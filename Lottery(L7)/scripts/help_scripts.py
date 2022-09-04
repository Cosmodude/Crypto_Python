from brownie import (network, config, accounts,MockV3Aggregator,Contract, VRFCoordinatorMock,
LinkToken, interface)
from web3 import Web3

Forked_Local_Environments=["mainnet-fork","mainnet-fork-dev"]
Local_Blockchain_Environments = ["development", "ganache-local"]

Decimals = 8
Start_price = 20000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in Local_Blockchain_Environments or network.show_active() in Forked_Local_Environments:
        return accounts[0]
        
    return accounts.add(config["wallets"]["from_key"])


contr_to_mock = { "eth_usd_price_feed" : MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock,"link_token": LinkToken }

def get_contract(contr_name):
    """This function will grab addresses from config, otherwise will deploy mock contract
    Args:contract name (string),
    Return: contract (brownie.network.contract.ProjectContract: latest)
    """
    contr_type= contr_to_mock[contr_name]
    if network.show_active() in Local_Blockchain_Environments:
        if len(contr_type)<=0:
            #MockV3Aggregator.length
            deploy_mocks()
        contract= contr_type[-1]
    else:
        contr_address=config["networks"][network.show_active()][contr_name]
        contract = Contract.from_abi(contr_type._name, contr_address,contr_type.abi)
    return contract


def deploy_mocks(Decimals=Decimals,Start_price=Start_price):
    acc=get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    mock_price_feed=MockV3Aggregator.deploy(
            Decimals, Start_price, {"from": acc}
        )
    link_token=LinkToken.deploy({"from": acc})
    VRFCoordinatorMock.deploy(link_token.address,{"from":acc})
    print("Mocks deployed!")

def fund_with_link(contr_addr, acc=None, link_token=None, amount=1000000000000000000):
    acc=acc if acc else get_account()
    link_token= link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contr_addr,amount, {"from":acc})
    """  link_token_interface= interface.LinkTokenInterface(link_token.address)
    tx= link_token_interface.transfer(contr_addr,amount, {"from":acc}) """
    tx.wait(1)
    print("Fund contract!")
    return tx
