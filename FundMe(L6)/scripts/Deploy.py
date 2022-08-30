from brownie import FundMe,MockV3Aggregator, network,config
from scripts.helpful_scripts import get_account
acc=get_account()

#if we are on persistent network(rinkeby) use associated address
#otherwise, deploy mocks
if network.show_active()!= "development":
    pricefeed_addr=config["networks"][network.show_active()][
        "eth_usd_price_feed"
    ]
else:
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    mock_aggr=MockV3Aggregator.deploy(18, 2000000000000000000,{"from":acc})
    pricefeed_addr=mock_aggr.address


def deploy_fund_me():
    #pass priceFeed address to contract
    fu=FundMe.deploy(pricefeed_addr ,{"from":acc},
    publish_source=config["networks"][network.show_active()].get("verify"))
    print(f"Contract deployed to {fu.address}")

def main():
    deploy_fund_me()