from brownie import LotteryV2, accounts, network, config, exceptions
from web3 import Web3
from scripts.deploy_Lottery import deploy
from scripts.deploy_myVRF import get_random
from scripts.helpful_scripts import (
    get_acc,
    fund_with_link,
    get_contract,
    LOCAL_BLOCKCHAINS,
)
import pytest, random, time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Testnets")
    lottery = deploy()
    acc = get_acc()
    names = ["Abdullah", "Saif", "Junaid", "Samee", "Panda"]
    lottery.startLottery({"from": acc})
    for i in range(5):
        lottery.enter(
            names[i],
            {"from": acc, "value": lottery.getEntranceFee() + 10000},
        )
    random_num = get_random()
    lottery.chooseWinner(random_num)
    winner_name = names[random_num % len(names)]
    winner_addr = acc.address

    assert winner_addr == lottery.last_winner()
    assert lottery.address_to_name(winner_addr) == winner_name
    assert lottery.balance() == 0