from scripts.helpful_scripts import get_account,get_contract
from web3 import Web3
from brownie import (
    My_Token,
    network,
    accounts
    )

init_suply=Web3.toWei(1000,"ether")

def deploy():
    acc=get_account()
    token=My_Token.deploy(init_suply,{"from":acc})
    print(token.name())
    print(token.symbol())
    print(token.totalSupply()/(10**18))


def main():
    deploy()