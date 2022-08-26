from brownie import Storage, accounts

def test_deploy():
    #Arrange
    account= accounts[0]
    #Act
    str=Storage.deploy({"from": account})
    val=str.retrieve()
    ex=0
    #Assert
    assert ex==val

def test_update():
    #Arrange
    account= accounts[0]
    str=Storage.deploy({"from": account})
    #Act
    ex=15
    str.str(15,{"from":account})
    #Assert
    assert ex==str.retrieve()
