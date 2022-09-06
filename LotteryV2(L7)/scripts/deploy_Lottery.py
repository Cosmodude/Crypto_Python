from brownie import LotteryV2, network, accounts, config
from scripts.helpful_scripts import get_acc, get_contract, fund_with_link
from scripts.deploy_myVRF import get_random
import time


def deploy():
    #acc=get_acc(id="TestVlad");
    acc = get_acc()
    contract = LotteryV2.deploy(
        get_contract("eth-usd-priceFeed").address,
        {"from": acc},
        # publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery Deployed!!")
    return contract


def start_lottery():
    acc = get_acc()
    lottery = LotteryV2[-1]
    tx = lottery.startLottery({"from": acc})
    tx.wait(1)
    print("Lottery Started!")


def enter_lottery(name):
    acc = get_acc()
    lottery = LotteryV2[-1]
    entrance_fee = lottery.getEntranceFee() + 100000
    for i in range(len(name)):
        tx = lottery.enter(name[i], {"from": acc, "value": entrance_fee})
        tx.wait(1)
        print(f"{name[i]} entered the Lottery!")


def end_lottery():
    acc = get_acc()
    lottery = LotteryV2[-1]
    print(f"Balance of this contract before funding: {lottery.balance()}")
    random_num = get_random()
    print(f"Random num: {random_num}")
    tx = lottery.chooseWinner(random_num, {"from": acc})
    tx.wait(1)
    winner_address = lottery.last_winner()
    winner_name = lottery.address_to_name(winner_address)
    print(f"Winner Address is: {winner_address} with Name: {winner_name}")


def main():
    names = ["Abdullah", "Saif", "Junaid"]
    deploy()
    start_lottery()
    enter_lottery(names)
    end_lottery()