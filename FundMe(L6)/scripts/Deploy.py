from decimal import Decimal
from brownie import FundMe,MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, Local_Blockchain_Environments

if network.show_active() not in Local_Blockchain_Environments:
    pricefeed_addr=config["networks"][network.show_active()][
        "eth_usd_price_feed"
    ]
else:
   deploy_mocks()
   pricefeed_addr=MockV3Aggregator[-1].address

acc=get_account()

def deploy_fund_me():
    #pass priceFeed address to contract
    fu=FundMe.deploy(
    pricefeed_addr ,{"from":acc},
    publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fu.address}")
    return fu

def main():
    deploy_fund_me()