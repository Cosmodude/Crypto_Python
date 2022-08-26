from brownie import FundMe
from scripts.helpful_scripts import get_account

def deploy_fund_me():
    acc=get_account()
    fu=FundMe.deploy({"from":acc})
    print(f"Contract deployed to {fu.address}")

def main():
    deploy_fund_me()