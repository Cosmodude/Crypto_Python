from brownie import LotteryV2, accounts, network, config, exceptions
from web3 import Web3
from scripts.deploy_Lottery import deploy
from scripts.helpful_scripts import (
    get_acc,
    fund_with_link,
    get_contract,
    LOCAL_BLOCKCHAINS,
)
import pytest, random

# 0.0319

# Arrange
# Act
# Assert
def test_getEntraceFee():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Local Ganache Blockchain")
    lottery = deploy()
    # Act
    expected_entry_fee = Web3.toWei(50 / 2000, "ether")
    entry_fee = lottery.getEntranceFee()
    # Assert
    assert entry_fee == expected_entry_fee


def test_enter_without_starting_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Local Ganache Blockchain")
    lottery = deploy()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter("Adullah", {"from": get_acc(), "value": lottery.getEntranceFee()})


def test_get_participants():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Local Ganache Blockchain")
    lottery = deploy()
    names = ["Abdullah", "Saif", "Junaid", "Samee", "Panda"]
    address_to_player = []
    # Act
    acc = get_acc()
    lottery.startLottery({"from": acc})
    for i in range(5):
        acc = get_acc(index=i)
        address_to_player.append((acc, names[i]))
        lottery.enter(
            names[i],
            {"from": acc, "value": lottery.getEntranceFee() + 10000},
        )
    # Assert
    assert lottery.getParticipants() == address_to_player


def test_can_choose_winner():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Local Ganache Blockchain")
    lottery = deploy()
    names = ["Abdullah", "Saif", "Junaid", "Samee", "Panda"]
    address_to_player = []
    # Act
    acc = get_acc()
    lottery.startLottery({"from": acc})
    for i in range(5):
        acc = get_acc(index=i)
        address_to_player.append((acc, names[i]))
        lottery.enter(
            names[i],
            {"from": acc, "value": lottery.getEntranceFee() + 10000},
        )
    iniital_balance_of_lottery = lottery.balance()
    STATIC_RANDOM = random.randint(0, 500)
    lottery.chooseWinner(STATIC_RANDOM)
    winner = address_to_player[STATIC_RANDOM % len(address_to_player)]
    winner_addr = winner[0]
    assert winner_addr == lottery.last_winner()
    assert lottery.balance() == 0


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Local Ganache Blockchain")
    lottery = deploy()
    acc = get_acc()
    lottery.startLottery({"from": acc})
    player_name = "Abdullah"
    lottery.enter(
        player_name, {"from": get_acc(), "value": lottery.getEntranceFee() + 10000}
    )
    fund_with_link(lottery)
    lottery.endLottery({"from": acc})
    assert lottery.state() == 2


def test_only_owner_can_start_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Local Ganache Blockchain")
    lottery = deploy()
    not_owner = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.startLottery({"from": not_owner})


def test_winner_gets_all_money():
    pass