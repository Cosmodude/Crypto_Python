from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

sample_token_URI="https://ipfs.io/ipfs/QmQ1TCshR9w22GLwcEkN7VELL5gWwoCMGqVt8iEAhRKW6J?filename=Shawn.JPG"
OpenSea_URL="https://opensea.io/assets/ethereum/{}"

def main():
    acc=get_account()
    simple_collectible=SimpleCollectible.deploy({"from":acc})
    create_tx=simple_collectible.createCollectible(sample_token_URI,{"from":acc})
    create_tx.wait(1)
    print(
        f"You can view your NFT at {OpenSea_URL.format(0x495f947276749ce646f68ac8c248420045cb7b5e/50486160427477088231221254495286489427438047489773215340101789803040542294017)}")

    