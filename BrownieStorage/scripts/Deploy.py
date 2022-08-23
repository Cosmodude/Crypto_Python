from brownie import accounts
import os

def deploy_staorage():
    #acc=accounts.load("TestVlad")
    acc=accounts.add(os.getenv("PRIV_KEY"))
    print(acc)
def main():
    print("HI")
    deploy_staorage()