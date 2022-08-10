pragma solidity ^0.6.6;

contract Storage{

    int favnum;

    struct man{
        string name;
        int money;
    }
    man[] public men;
    mapping(string => int ) public name_money;

    function StoreP(string memory name, int money) public {
            men.push(man(name,money));
    }
     function retrieve() public view returns(int) {
        return favnum;
    }
    function str(int num) public{
        favnum=num;
    }
}