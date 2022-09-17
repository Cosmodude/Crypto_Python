from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import (
    network,
    accounts,
    config,
    interface

)

def borrow():
    acc=get_account()
    erc20_address= config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lend_pool=get_lending_pool()


def get_lending_pool():
    #Address  
    lend_pool_addr_prov= interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
        )
    lend_pool_addr=lend_pool_addr_prov.getLendingPool()
    #ABI

def main():
    borrow()