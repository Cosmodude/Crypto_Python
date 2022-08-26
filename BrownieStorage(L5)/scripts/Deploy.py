from brownie import accounts, config, Storage,network

def deploy_storage():
    acc=get_account()
    St=Storage.deploy({"from":acc})
    #acc=accounts.load("TestVlad")
    #acc=accounts.add(config ["wallets"]["from_key"])
    print(acc)
    print("trans")
    print(St)
    value = St.retrieve()
    print("value")
    print(value)
    transaction= St.str(15,{"from":acc})
    transaction.wait(1)
    value = St.retrieve()
    print(value)

def get_account():
    if network.show_active()=="development" :
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    print("HI")
    deploy_storage()