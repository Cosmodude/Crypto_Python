from brownie import Lottery,accounts,config,network,exceptions
from scripts.deploy_lottery import deploy_Lottery
from web3 import Web3
from scripts.help_scripts import Local_Blockchain_Environments, get_account, fund_with_link, get_contract
import pytest

def test_get_entr_fee():
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    #Arrange
    lot=deploy_Lottery()
    #Act
    exp_fee=Web3.toWei(0.025, "ether")
    entr_fee=lot.getEntrFee()
    #Assert
    assert exp_fee== entr_fee

def test_cant_enter_before_start():
    #Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    lot=deploy_Lottery()
    #Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lot.enter({"from":get_account(),"value": lot.getEntrFee()})

def test_can_start_and_enter():
    #Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    lot=deploy_Lottery()
    acc=get_account()
    lot.start({"from": acc})
    #Act
    lot.enter({"from":get_account(),"value": lot.getEntrFee()})
    #Assert
    assert lot.players(0)==acc

def test_can_end():
     #Arrange
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    lot=deploy_Lottery()
    acc=get_account()
    lot.start({"from": acc})
    lot.enter({"from":get_account(),"value": lot.getEntrFee()})
    fund_with_link(lot)
    #Act
    lot.finish({"from":acc})
    assert lot.lot_state()==2

def test_can_pick_winner_loc():
    if network.show_active() not in Local_Blockchain_Environments:
        pytest.skip()
    lot=deploy_Lottery()
    acc=get_account()
    lot.start({"from": acc})
    lot.enter({"from":acc,"value": lot.getEntrFee()})
    lot.enter({"from":get_account(index=1),"value": lot.getEntrFee()})
    lot.enter({"from":get_account(index=2),"value": lot.getEntrFee()})
    fund_with_link(lot)
    tx= lot.finish({"from": acc})
    reqId = tx.events["RequestedRandomness"]["reqId"]
    static_rng=777
    get_contract("vrf_coordinator").callBackWithRandomness(
        reqId,static_rng,lot.address, {"from": acc}
        )
    start_balance_of_acc=acc.balance()
    balance_of_lottery= lot.balance()
    assert lot.recentWinner()==acc
    assert lot.balance()==0
    assert acc.balance()==balance_of_lottery+start_balance_of_acc
    assert acc.balance()!=0