// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./MyVRFv2.sol";

contract LotteryV2 is Ownable {
    mapping(address => string) public address_to_name;

    struct Players {
        address payable players_address;
        string name;
    }

    Players[] public peeps;

    uint256 internal minUSD;
    address payable public last_winner;
    AggregatorV3Interface public price_feed;
    enum LOTTERY_STATE {
        open,
        close,
        running
    }
    LOTTERY_STATE public state;

    constructor(address _price_feed) {
        price_feed = AggregatorV3Interface(_price_feed);
        minUSD = 5 * (10**18);
        state = LOTTERY_STATE.close;
    }

    function getEntranceFee() public view returns (uint256) {
        //IF entry fee = 50 and eth price is 1000
        // 50/1000 ==> this cannot be done as solidity doesn't deal in decimals
        // 50*(10**18)/1000
        uint256 price = getPrice();
        uint256 EntranceCost = (minUSD * (10**18)) / price;
        return EntranceCost;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = price_feed.latestRoundData();
        return uint256(answer * 10**10); //18 decimals
    }

    function enter(string memory name) public payable {
        require(state == LOTTERY_STATE.open, "Lottery hasn't started yet!");
        require(msg.value > getEntranceFee(), "Please send more ETH to enter!");

        peeps.push(Players(payable(msg.sender), name));
        address_to_name[msg.sender] = name;
    }

    function startLottery() public onlyOwner {
        require(state == LOTTERY_STATE.close, "Lottery already running!");
        state = LOTTERY_STATE.open;
    }

    function getParticipants() public view returns (Players[] memory) {
        return peeps;
    }

    function chooseWinner(uint256 rand) public onlyOwner {
        state = LOTTERY_STATE.running;
        require(state == LOTTERY_STATE.running, "Still working!");
        require(rand > 0, "Random Number not Returned");

        uint256 winner_index = rand % peeps.length;
        last_winner = peeps[winner_index].players_address;
        last_winner.transfer(address(this).balance);
        endLottery();
    }

    function endLottery() internal {
        //Lottery Reset
        //peeps = new Players[](0);
        state = LOTTERY_STATE.close;
    }
}
