from brownie import Lottery,accounts,config,network,exceptions
import pytest
from scripts.deploy_lottery import deploy_Lottery
from scripts.help_scripts import Local_Blockchain_Environments, get_account, fund_with_link, get_contract
import time

from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3('http://127.0.0.1:8545')
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
def test_can_pick_winner_network():
    if network.show_active() in Local_Blockchain_Environments:
        pytest.skip()
    lot=deploy_Lottery()
    acc=get_account()
    lot.start({"from": acc})
    lot.enter({"from":acc,"value": lot.getEntrFee()})
    lot.enter({"from":acc,"value": lot.getEntrFee()})
    lot.enter({"from":acc,"value": lot.getEntrFee()})
    fund_with_link(lot)
    tx= lot.finish({"from": acc})
    time.sleep(180)
    assert lot.recentWinner()==acc
    assert lot.balance()==0
