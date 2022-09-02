from tkinter import W
from brownie import Lottery,accounts,config,network
from web3 import Web3


def test_get_entr_fee():
    acc=accounts[0]
    lottery=Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],
    {"from":acc}
    
)
    assert lottery.getEntrFee() > Web3.toWei(0.003,"ether")
    print(lottery.getEntrFee())
    assert lottery.getEntrFee() < Web3.toWei(0.005,"ether")