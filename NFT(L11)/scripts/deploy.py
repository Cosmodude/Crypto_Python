from this import s
from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

sample_token_URI="https://ipfs.io/ipfs/QmVC5A5F7e6BK4TqF9rmkrp8LFsbN11JWeD9xDhxx1KcmU?filename=jsonvalidator.json"
OpenSea_URL="https://testnets.opensea.io/assets/goerli/{}/{}"

def main():
    acc=get_account()
    simple_collectible=SimpleCollectible.deploy({"from":acc})
    create_tx=simple_collectible.createCollectible(sample_token_URI,{"from":acc})
    create_tx.wait(1)
    print(
        f"You can view your NFT at {OpenSea_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )   
    