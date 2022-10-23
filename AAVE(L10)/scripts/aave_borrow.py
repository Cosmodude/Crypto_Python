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
    deposit_tx=lend_pool.deposit(erc20_address, amount, acc.address, 0, {"from": acc} )
    deposit_tx.wait(1)
    print ("Deposited!")
    borrowable_eth, total_depth= get_borrowable_data(lend_pool,acc)

    print("Let's borrow!")
    #DAI in terms of ETH
    dai_eth_price=get_lending_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
        )
    #borrowable ETH * 0.9 -> borrowable DAI 
    amount_want_to_borrow=(1/dai_eth_price)*(borrowable_eth*0.9)
    print(f"We are going to borrow {amount_want_to_borrow} DAI")
    #Borrowing
    dai_address= config["networks"][network.show_active()]["dai_token"]
    borrow_tx= lend_pool.borrow(
        dai_address,
        Web3.toWei(amount_want_to_borrow, "ether"),
        1,
        0, 
        acc.address,
        {"from":{acc}},
        )
    borrow_tx.wait(1)
    print("We borrowed DAI")
    get_borrowable_data(lend_pool,acc)

    repay_all(amount,lend_pool, acc)
    print("We deposited, borrowed and repaid with Aave, Brownie and Chainlink!")



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
    dai_eth_price_feed= interface.AggregatorV3Interface(price_feed_address)
    latest_price=dai_eth_price_feed.latestRoundData()[1]
    converted_price=Web3.fromWei(latest_price, "ether")
    print( f"DAI/ETH price is {converted_price}" )
    return(float(converted_price))

def repay_all(amount, lend_pool, acc):
    erc20_address= config["networks"][network.show_active()]["weth_token"]
    dai_address= config["networks"][network.show_active()]["dai_token"]
    approve_erc20(
        Web3.toWei(amount,"ether"),
        lend_pool.address,
        erc20_address,
        acc
    )
    repay_tx=lend_pool.repay(
        dai_address,
        amount,
        1,
        acc.address,
        {"from":acc}
    )
    repay_tx.wait(1)
    print("Repayed")
    


def main():
    borrow()