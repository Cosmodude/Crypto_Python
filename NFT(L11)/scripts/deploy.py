from this import s
from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

sample_token_URI="https://ipfs.io/ipfs/QmQ1TCshR9w22GLwcEkN7VELL5gWwoCMGqVt8iEAhRKW6J?filename=Shawn.JPG"
OpenSea_URL="https://testnets.opensea.io/assets/goerli/{}/{}"

def main():
    acc=get_account()
    simple_collectible=SimpleCollectible.deploy({"from":acc})
    create_tx=simple_collectible.createCollectible(sample_token_URI,{"from":acc})
    create_tx.wait(1)
    print(
        f"You can view your NFT at {OpenSea_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )   
    