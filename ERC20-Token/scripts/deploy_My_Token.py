from scripts.helpful_scripts import get_account,get_contract
from brownie import (
    My_Token,
    network,
    accounts
    )

def deploy():
    acc=get_account()
    token=My_Token.deploy(10**20,{"from":acc})
    print(token.totalSupply())


def main():
    deploy()