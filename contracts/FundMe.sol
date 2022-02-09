// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    // array of addresses who deposited
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address __priceFeed) public {
        priceFeed = AggregatorV3Interface(__priceFeed);
        owner = msg.sender;
    }

    function getVersion() public view returns (uint256) {
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(
        //     0x8A753747A1Fa494EC906cE90E9f37563A8AF630e //this address is of rinkbey testnets
        // );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // 274648929177
        return uint256(answer * 10**10);
    }

    function getConversion(uint256 ethAmount) public view returns (uint256) {
        uint256 price = getPrice();
        //244228000000
        uint256 ethAmontInUSD = (price * ethAmount) / (10**18);
        //249758928896000
        return ethAmontInUSD;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function fund() public payable {
        uint256 minimumUSD = 10 * 10**18;
        require(
            getConversion(msg.value) >= minimumUSD,
            "You have to spend minimum of 10 USD"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        // payable(msg.sender).transfer(address(this).balance);
        msg.sender.transfer(address(this).balance);
        //iterate through all the mappings and make them 0
        //since all the deposited amount has been withdrawn
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        funders = new address[](0);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precesion = 1 * 10**18;
        return (minimumUSD * precesion) / price;
    }
}
