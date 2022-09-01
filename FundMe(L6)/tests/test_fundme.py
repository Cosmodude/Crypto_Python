from brownie import accounts, network,exceptions

import pytest

def test_can_fund_and_withdraw():
    from scripts.Deploy import deploy_fund_me
    from scripts.helpful_scripts import get_account, Local_Blockchain_Environments

    acc=get_account()
    fund_me= deploy_fund_me()
    entr_fee=fund_me.getEntranceFee() +100
    tx=fund_me.fund({"from": acc,"value":entr_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(acc.address)== entr_fee
    tx2 =fund_me.withdraw({"from": acc})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(acc.address)==0

def test_only_owner_can_withdraw():
    from scripts.Deploy import deploy_fund_me
    from scripts.helpful_scripts import get_account, Local_Blockchain_Environments

    if network.show_active()  not in Local_Blockchain_Environments:
        pytest.skip("only for testing env")
    acc=get_account()
    fund_me = deploy_fund_me()
    ba = accounts.add()
    
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": ba})
