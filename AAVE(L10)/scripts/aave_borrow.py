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
    borrowable_eth, total_depth= get_borrowable_data(lend_pool,acc)

    print("Let's borrow!")
    #DAI in terms of ETH
    dai_eth_price=get_lending_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
        )

#Approve sending out ERC20 Tokens
def approve_erc20(amount, spender,erc20_address, account):
    print("proving ERC20 token...")
    erc20= interface.IERC20(erc20_address)
    tx= erc20.approve(spender,amount,{"from":account})
    tx.wait(1)
    print("Approved!")
    return tx

def get_borrowable_data(lending_pool,account):
    (
    total_collateral_ETH,
    total_depth_ETH, 
    available_borrow_ETH, 
    current_liquidation_threshold, 
    ltv, 
    health_factor
    )=lending_pool.getUserAccountData(account.address)
    available_borrow_ETH= Web3.fromWei(available_borrow_ETH,"ether")
    total_collateral_ETH=Web3.fromWei(total_collateral_ETH,"ether")
    total_depth_ETH= Web3.fromWei(total_depth_ETH,"ether")
    print(f"You have {total_collateral_ETH} ETH deposited...")
    print(f"You have {total_depth_ETH} ETH borrowed...")
    print(f"You can borrow {available_borrow_ETH} ETH...")

    return (float(available_borrow_ETH),float(total_depth_ETH))

def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def get_lending_price(price_feed_address):
    #ABI
    #Adress
    dai_eth_price_feed= interface.AggregatorV3Interface

def main():
    borrow()