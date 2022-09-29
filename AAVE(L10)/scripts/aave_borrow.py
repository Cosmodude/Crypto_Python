from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3
from brownie import (
    network,
    accounts,
    config,
    interface

)
amount = Web3.toWei(0.1, "ether")
print(amount)
def borrow():
    acc=get_account()
    erc20_address= config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lend_pool=get_lending_pool()
    print(lend_pool.address)
    approve_erc20(amount, lend_pool.address, erc20_address, acc)
    print ("Depositing...")
    tx=lend_pool.deposit(erc20_address, amount, acc.address, 0, {"from": acc} )
    tx.wait(1)
    print ("Deposited!")

#Approve sending out ERC20 Tokens
def approve_erc20(amount, spender,erc20_address, account):
    print("proving ERC20 token...")
    erc20= interface.IERC20(erc20_address)
    tx= erc20.approve(spender,amount,{"from":account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def main():
    borrow()