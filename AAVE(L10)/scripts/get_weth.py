from scripts.helpful_scripts import get_account
from brownie import interface, network, config


def get_weth():
    #ABI
    #Address
    acc=get_account()
    weth= interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx= weth.deposit({"from": acc, "value": (0.05 * 10 ** 18)})
    tx.wait(1)
    print(f"reseived {weth.allowance} eth")
    return tx

def main():
    get_weth()

