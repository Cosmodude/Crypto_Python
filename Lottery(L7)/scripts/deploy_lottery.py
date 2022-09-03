from scripts.help_scripts import get_account,get_contract
from brownie import Lottery,config,network
acc=get_account(id="TestVlad");

def deploy_lottery():
    #acc=get_account(id="TestVlad");
    lot= Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": acc},
        publish_source=config["networks"][network.show_active()].get("verify",False)
    )
    print("Lottery Deployed")
    
def start_lottery():
    #acc=get_account()
    lot=Lottery[-1]
    start_tx= lot.start({"from": acc})
    start_tx.wait(1)
    print("Lottery Started")

def enter_lottery():
    acc=get_account()
    lot=Lottery[-1]
    value=lot.getEntrFee() + 100000000
    tx= lot.enter({"from": acc, "value": value})
    tx.wait(1)
    print("You entered the Lottery!")

def end_Lottery():
    lot=Lottery[-1]
def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()