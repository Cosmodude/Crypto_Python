from scripts.help_scripts import get_account,get_contract, fund_with_link
from brownie import Lottery,config,network
import time

#acc=get_account()

def deploy_Lottery():
    acc=get_account()
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
    return lot
    
def start_lottery():
    acc=get_account()
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
    acc=get_account()
    lot=Lottery[-1]
    #Fund with Link
    tx =fund_with_link(lot.address)
    tx.wait(1)
    end_trans= lot.finish({"from":acc})
    end_trans.wait(1)
    time.sleep(120)
    print(f"{lot.recentWinner()} is the winner!")

def main():
    deploy_Lottery()
    start_lottery()
    enter_lottery()
    end_Lottery()