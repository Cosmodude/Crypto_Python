// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable{
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntrFee;
    AggregatorV3Interface internal EthUsdpricefeed;
    enum state{
        open,closed,calculating
    }
    state public lot_state;
    uint256 public fee;
    bytes32 public keyHash;


    constructor(address _priceFeedAddr,
    address _vrfCoordinator,
    address _link,
    uint256 _fee,
    bytes32 _keyhash
    )
     public VRFConsumerBase(_vrfCoordinator, _link) 
    {
        usdEntrFee=5*(10**18);
        EthUsdpricefeed = AggregatorV3Interface(_priceFeedAddr);
        lot_state=state.closed;
        fee =_fee;
        keyHash=_keyhash;
    }
    function enter() public payable {
        require(lot_state==state.open);
        require(msg.value>= getEntrFee(),"Not enough ETH");
        players.push(msg.sender);
    }
    function getEntrFee() public view returns (uint256) {
        (,int price,,,)=EthUsdpricefeed.latestRoundData();
        uint256 adjPrice= uint256(price)*(10**10);
        uint256 Price = usdEntrFee*(10**18)/adjPrice;
        return Price;
    }

    function start() public onlyOwner{
          require(lot_state==state.closed,"Can't start a new lottery");
          lot_state=state.open;
    }

    function finish() public onlyOwner{
        lot_state=state.calculating;
         bytes32 requestID= requestRandomness(keyHash,fee);
    }

    function fulfillRandomness(bytes32 _requeestId, uint256 _randomness) internal override {
        require(lot_state==state.calculating, "Too early");
        require(_randomness > 0, "Not Random");
        uint256 indexWinner = _randomness % players.length;
        recentWinner=players[indexWinner];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);
        lot_state=state.closed;
        randomness=_randomness;
    }

}