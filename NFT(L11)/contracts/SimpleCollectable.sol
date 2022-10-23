// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract SimpleCollectible is ERC721 {
    constructor () public ERC721 ("Shawn", "SH" ){}

    function createCollectible () public returns (uint256) {
        
    }


}