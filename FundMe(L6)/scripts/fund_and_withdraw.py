from brownie import FundMe
from scripts.helpful_scripts import get_account
def fund():
    fund_me= FundMe[-1]
    acc=get_account()
    ent_fee= fund_me.getEntranceFee()
    print(f"the current entry fee is {ent_fee}")
    print("Funding")
    fund_me.fund({"from":acc,"value": ent_fee})

def withdraw():
    fund_me= FundMe[-1]
    acc=get_account()
    fund_me.withdraw({"from":acc})

def main():
    fund()
    withdraw()